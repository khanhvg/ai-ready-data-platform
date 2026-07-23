"""Durable CAS, idempotency and insert-only audit state."""
from __future__ import annotations
import hashlib, json, os, pathlib, sqlite3, time
from dataclasses import dataclass
from .audit import chained


class StateError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class Admission:
    run_id: str
    fence: int
    replay: dict[str, object] | None


class Store:
    def __init__(self, root: pathlib.Path):
        root.mkdir(mode=0o700, parents=True, exist_ok=True); os.chmod(root, 0o700)
        self.path = root / "runner.sqlite3"
        self.anchor_path = root / "audit-anchor.json"
        self.pending_anchor_path = root / "audit-anchor.pending.json"
        self.db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS workspaces(id TEXT PRIMARY KEY, revision INTEGER NOT NULL, fence INTEGER NOT NULL);
        INSERT OR IGNORE INTO workspaces VALUES('promotion-trust',0,0);
        CREATE TABLE IF NOT EXISTS runs(
          run_id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE NOT NULL, request_sha256 TEXT NOT NULL,
          operation_id TEXT NOT NULL, requested_revision INTEGER NOT NULL, fence INTEGER NOT NULL,
          status TEXT NOT NULL, container_id TEXT, image_digest TEXT, result_json TEXT,
          created_ns INTEGER NOT NULL, updated_ns INTEGER NOT NULL, daemon_identity TEXT);
        CREATE TABLE IF NOT EXISTS audit(
          sequence INTEGER PRIMARY KEY, previous_sha256 TEXT NOT NULL, payload BLOB NOT NULL,
          entry_sha256 TEXT UNIQUE NOT NULL);
        CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit BEGIN SELECT RAISE(ABORT,'AUDIT_IMMUTABLE'); END;
        CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit BEGIN SELECT RAISE(ABORT,'AUDIT_IMMUTABLE'); END;
        """)
        if "daemon_identity" not in {row[1] for row in self.db.execute("PRAGMA table_info(runs)")}:
            self.db.execute("ALTER TABLE runs ADD COLUMN daemon_identity TEXT")
        os.chmod(self.path, 0o600)
        if self.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]==0:
            if self.pending_anchor_path.exists():
                pending=self._read_pending()
                if self.anchor_path.exists() or pending["previous"] is not None:raise StateError("RUNNER_AUDIT_TAMPERED")
                self.pending_anchor_path.unlink();self._fsync_parent()
            if self.anchor_path.exists():raise StateError("RUNNER_AUDIT_TAMPERED")
            self.db.execute("BEGIN IMMEDIATE")
            self._append({"kind":"genesis"})
            self._prepare_anchor();self.db.execute("COMMIT");self._finalize_anchor()
        self.verify_audit()

    def verify_audit(self) -> None:
        previous="0"*64; expected_sequence=1;committed={}
        for sequence,stored_previous,payload,entry_digest in self.db.execute("SELECT sequence,previous_sha256,payload,entry_sha256 FROM audit ORDER BY sequence"):
            if sequence!=expected_sequence or stored_previous!=previous or hashlib.sha256(payload).hexdigest()!=entry_digest:
                raise StateError("RUNNER_AUDIT_TAMPERED")
            try:value=json.loads(payload)
            except (TypeError,json.JSONDecodeError) as exc: raise StateError("RUNNER_AUDIT_TAMPERED") from exc
            if value.get("sequence")!=sequence or value.get("previousSha256")!=previous or set(value)!={"sequence","previousSha256","event"}:
                raise StateError("RUNNER_AUDIT_TAMPERED")
            event=value["event"]
            if not isinstance(event,dict):raise StateError("RUNNER_AUDIT_TAMPERED")
            if event.get("kind")=="committed":
                run_id=event.get("runId");result_sha=event.get("resultSha256")
                if not isinstance(run_id,str) or run_id in committed or not isinstance(result_sha,str) or len(result_sha)!=64:raise StateError("RUNNER_AUDIT_TAMPERED")
                committed[run_id]=result_sha
            previous=entry_digest;expected_sequence+=1
        anchor=None
        if self.anchor_path.exists():
            try:anchor=json.loads(self.anchor_path.read_text())
            except (OSError,json.JSONDecodeError) as exc:raise StateError("RUNNER_AUDIT_TAMPERED") from exc
        observed={"schemaVersion":"runner-audit-anchor-v1","sequence":expected_sequence-1,"entrySha256":previous}
        pending=self._read_pending() if self.pending_anchor_path.exists() else None
        if anchor==observed:
            if pending is not None:
                if pending["previous"]!=anchor and pending["next"]!=anchor:raise StateError("RUNNER_AUDIT_TAMPERED")
                self.pending_anchor_path.unlink();self._fsync_parent()
            self._verify_committed_results(committed);return
        if pending is not None and pending["previous"]==anchor and pending["next"]==observed:
            self._write_document(self.anchor_path,observed);self.pending_anchor_path.unlink();self._fsync_parent();self._verify_committed_results(committed);return
        raise StateError("RUNNER_AUDIT_TAMPERED")

    def _verify_committed_results(self,committed:dict[str,str])->None:
        observed={}
        for run_id,result in self.db.execute("SELECT run_id,result_json FROM runs WHERE status='committed'"):
            if not isinstance(result,str):raise StateError("RUNNER_AUDIT_TAMPERED")
            observed[str(run_id)]=hashlib.sha256(result.encode()).hexdigest()
        if observed!=committed:raise StateError("RUNNER_AUDIT_TAMPERED")

    def _read_pending(self)->dict[str,object]:
        try:value=json.loads(self.pending_anchor_path.read_text())
        except (OSError,json.JSONDecodeError) as exc:raise StateError("RUNNER_AUDIT_TAMPERED") from exc
        if set(value)!={"schemaVersion","previous","next"} or value.get("schemaVersion")!="runner-audit-pending-v1":raise StateError("RUNNER_AUDIT_TAMPERED")
        for anchor in (value["previous"],value["next"]):
            if anchor is None:continue
            if not isinstance(anchor,dict) or set(anchor)!={"schemaVersion","sequence","entrySha256"} or anchor.get("schemaVersion")!="runner-audit-anchor-v1" or type(anchor.get("sequence")) is not int or anchor["sequence"]<1 or not isinstance(anchor.get("entrySha256"),str) or len(anchor["entrySha256"])!=64:raise StateError("RUNNER_AUDIT_TAMPERED")
        if value["next"] is None:raise StateError("RUNNER_AUDIT_TAMPERED")
        return value

    def _write_document(self,path:pathlib.Path,value:dict[str,object])->None:
        raw=json.dumps(value,sort_keys=True,separators=(",",":")).encode()+b"\n";temporary=path.with_name(f".{path.name}.{os.getpid()}.tmp")
        fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        try:os.write(fd,raw);os.fsync(fd)
        finally:os.close(fd)
        os.replace(temporary,path);self._fsync_parent()

    def _fsync_parent(self)->None:
        parent=os.open(self.anchor_path.parent,os.O_RDONLY)
        try:os.fsync(parent)
        finally:os.close(parent)

    def _prepare_anchor(self)->None:
        rows=list(self.db.execute("SELECT sequence,entry_sha256 FROM audit ORDER BY sequence DESC LIMIT 2"))
        if not rows:raise StateError("RUNNER_AUDIT_TAMPERED")
        next_value={"schemaVersion":"runner-audit-anchor-v1","sequence":rows[0][0],"entrySha256":rows[0][1]}
        previous={"schemaVersion":"runner-audit-anchor-v1","sequence":rows[1][0],"entrySha256":rows[1][1]} if len(rows)==2 else None
        if self.anchor_path.exists():
            if json.loads(self.anchor_path.read_text())!=previous:raise StateError("RUNNER_AUDIT_TAMPERED")
        elif previous is not None:raise StateError("RUNNER_AUDIT_TAMPERED")
        self._write_document(self.pending_anchor_path,{"schemaVersion":"runner-audit-pending-v1","previous":previous,"next":next_value})

    def _finalize_anchor(self)->None:
        pending=self._read_pending();self._write_document(self.anchor_path,pending["next"]);self.pending_anchor_path.unlink();self._fsync_parent()

    @staticmethod
    def digest(request: dict[str, object]) -> str:
        raw=json.dumps(request,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
        return hashlib.sha256(raw).hexdigest()

    def admit(self, request: dict[str, object], fence: int) -> Admission:
        self.verify_audit()
        digest=self.digest(request); key=str(request["idempotencyKey"]); now=time.time_ns()
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row=self.db.execute("SELECT run_id,request_sha256,status,result_json FROM runs WHERE idempotency_key=?",(key,)).fetchone()
            if row:
                if row[1] != digest: raise StateError("RUNNER_CONFLICT")
                if row[2] == "committed":
                    self.db.execute("COMMIT")
                    return Admission(row[0],fence,json.loads(row[3]))
                raise StateError("RUNNER_CONFLICT")
            ws=self.db.execute("SELECT revision FROM workspaces WHERE id='promotion-trust'").fetchone()
            if ws[0] != request["workspaceRevision"]: raise StateError("RUNNER_CONFLICT")
            run_id=hashlib.sha256(f"{key}:{digest}:{fence}".encode()).hexdigest()[:32]
            self.db.execute("INSERT INTO runs(run_id,idempotency_key,request_sha256,operation_id,requested_revision,fence,status,container_id,image_digest,result_json,created_ns,updated_ns,daemon_identity) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(run_id,key,digest,request["operationId"],request["workspaceRevision"],fence,"admitted",None,None,None,now,now,None))
            self._append({"kind":"admitted","runId":run_id,"operationId":request["operationId"],"fence":fence})
            self._prepare_anchor();self.db.execute("COMMIT");self._finalize_anchor(); return Admission(run_id,fence,None)
        except Exception:
            if self.db.in_transaction:self.db.execute("ROLLBACK")
            if self.pending_anchor_path.exists():self.verify_audit()
            raise

    def transition(self, run_id: str, fence: int, status: str, *, container_id: str|None=None, image_digest: str|None=None, daemon_identity:str|None=None) -> None:
        self.verify_audit()
        now=time.time_ns()
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row=self.db.execute("SELECT status FROM runs WHERE run_id=? AND fence=?",(run_id,fence)).fetchone()
            allowed={
                "admitted":{"creating","failed"},
                "creating":{"created","failed"},
                "created":{"started-awaiting-input","removed","failed"},
                "started-awaiting-input":{"executing","removed","failed"},
                "executing":{"removed","failed"},
                "removed":{"failed"},
            }
            if not row: raise StateError("RUNNER_STALE_IDENTITY")
            if status not in allowed.get(str(row[0]),set()): raise StateError("RUNNER_ILLEGAL_TRANSITION")
            cur=self.db.execute("UPDATE runs SET status=?,container_id=COALESCE(?,container_id),image_digest=COALESCE(?,image_digest),daemon_identity=COALESCE(?,daemon_identity),updated_ns=? WHERE run_id=? AND fence=?",(status,container_id,image_digest,daemon_identity,now,run_id,fence))
            if cur.rowcount != 1: raise StateError("RUNNER_STALE_IDENTITY")
            self._append({"kind":"transition","runId":run_id,"status":status,"fence":fence})
            self._prepare_anchor();self.db.execute("COMMIT");self._finalize_anchor()
        except Exception:
            if self.db.in_transaction:self.db.execute("ROLLBACK")
            if self.pending_anchor_path.exists():self.verify_audit()
            raise

    def commit(self, run_id: str, fence: int, result: dict[str, object], new_revision: int) -> None:
        self.verify_audit()
        now=time.time_ns(); encoded=json.dumps(result,sort_keys=True,separators=(",",":"))
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row=self.db.execute("SELECT status FROM runs WHERE run_id=? AND fence=?",(run_id,fence)).fetchone()
            if not row or row[0] != "removed": raise StateError("RUNNER_STALE_IDENTITY")
            cur=self.db.execute("UPDATE workspaces SET revision=?,fence=? WHERE id='promotion-trust' AND fence<?",(new_revision,fence,fence))
            if cur.rowcount != 1: raise StateError("RUNNER_STALE_IDENTITY")
            self.db.execute("UPDATE runs SET status='committed',result_json=?,updated_ns=? WHERE run_id=?",(encoded,now,run_id))
            self._append({"kind":"committed","runId":run_id,"fence":fence,"revision":new_revision,"resultSha256":hashlib.sha256(encoded.encode()).hexdigest()})
            self._prepare_anchor();self.db.execute("COMMIT");self._finalize_anchor()
        except Exception:
            if self.db.in_transaction:self.db.execute("ROLLBACK")
            if self.pending_anchor_path.exists():self.verify_audit()
            raise

    def _append(self, event: dict[str, object]) -> None:
        row=self.db.execute("SELECT sequence,entry_sha256 FROM audit ORDER BY sequence DESC LIMIT 1").fetchone()
        sequence=(row[0]+1) if row else 1; previous=row[1] if row else "0"*64
        payload,digest=chained(previous,sequence,event)
        self.db.execute("INSERT INTO audit VALUES(?,?,?,?)",(sequence,previous,payload,digest))

    def record_event(self,event:dict[str,object])->None:
        self.verify_audit()
        if event.get("kind") not in ("rollback-started","rollback-completed"):raise StateError("RUNNER_AUDIT_EVENT_INVALID")
        self.db.execute("BEGIN IMMEDIATE")
        try:self._append(event);self._prepare_anchor();self.db.execute("COMMIT");self._finalize_anchor()
        except Exception:
            if self.db.in_transaction:self.db.execute("ROLLBACK")
            if self.pending_anchor_path.exists():self.verify_audit()
            raise

    def current_revision(self) -> int:
        return int(self.db.execute("SELECT revision FROM workspaces WHERE id='promotion-trust'").fetchone()[0])

    def fail_if_safe(self,run_id:str,fence:int)->bool:
        row=self.db.execute("SELECT status FROM runs WHERE run_id=? AND fence=?",(run_id,fence)).fetchone()
        if not row:raise StateError("RUNNER_STALE_IDENTITY")
        if row[0] not in ("admitted","removed"):return False
        self.transition(run_id,fence,"failed");return True

    def incomplete(self) -> list[tuple[str,str,str|None,str|None,int,str|None]]:
        return list(self.db.execute("SELECT run_id,status,container_id,image_digest,fence,daemon_identity FROM runs WHERE status NOT IN ('committed','failed')"))

    def committed(self)->list[tuple[str,dict[str,object]]]:
        self.verify_audit()
        return [(run_id,json.loads(result)) for run_id,result in self.db.execute("SELECT run_id,result_json FROM runs WHERE status='committed' ORDER BY created_ns")]
