"""Private HTTP admission independent of the later portal/BFF."""
from __future__ import annotations
import ctypes, http.server, json, os, pathlib, secrets, socket, socketserver, struct, sys, tempfile
from collections import Counter
from .registry import validate_request

BODY_LIMIT = 16_384
HOST = "runner.local"


class TransportError(ValueError):
    pass


def admit(*, method: str, headers: list[tuple[str, str]], body: bytes, bearer: str, csrf: str, peer_uid: int, effective_uid: int, expected_host: str=HOST) -> dict[str, object]:
    normalized = [(k.lower(), v) for k, v in headers]
    counts = Counter(k for k, _ in normalized)
    if any(v > 1 for v in counts.values()):
        raise TransportError("RUNNER_HEADER_AMBIGUOUS")
    h = dict(normalized)
    if peer_uid != effective_uid:
        raise TransportError("RUNNER_PEER_FORBIDDEN")
    if method != "POST":
        raise TransportError("RUNNER_METHOD_FORBIDDEN")
    if h.get("host") != expected_host:
        raise TransportError("RUNNER_HOST_FORBIDDEN")
    if h.get("origin", "") or "cookie" in h or "sec-fetch-site" in h or "access-control-request-method" in h:
        raise TransportError("RUNNER_BROWSER_REQUEST_FORBIDDEN")
    if h.get("authorization") != f"Bearer {bearer}" or h.get("x-runner-csrf") != csrf:
        raise TransportError("RUNNER_ADMISSION_SECRET_INVALID")
    if h.get("content-type") != "application/json":
        raise TransportError("RUNNER_CONTENT_TYPE_INVALID")
    if "transfer-encoding" in h or "content-length" not in h:
        raise TransportError("RUNNER_FRAMING_INVALID")
    allowed={"host","authorization","x-runner-csrf","content-type","content-length"}
    if set(h)!=allowed:
        raise TransportError("RUNNER_HEADER_FORBIDDEN")
    try:
        length = int(h["content-length"])
    except ValueError as exc:
        raise TransportError("RUNNER_FRAMING_INVALID") from exc
    if length != len(body) or length > BODY_LIMIT:
        raise TransportError("RUNNER_BODY_TOO_LARGE")
    try:
        value = json.loads(body.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TransportError("RUNNER_JSON_INVALID") from exc
    return validate_request(value)


def serve_loopback(service: object, control_file: pathlib.Path) -> None:
    bearer=secrets.token_urlsafe(32); csrf=secrets.token_urlsafe(32)
    class Handler(http.server.BaseHTTPRequestHandler):
        server_version=""; sys_version=""
        def setup(self)->None:
            super().setup();self.connection.settimeout(5)
        def do_OPTIONS(self)->None:self._reject(403,"RUNNER_BROWSER_REQUEST_FORBIDDEN")
        def do_GET(self)->None:self._reject(405,"RUNNER_METHOD_FORBIDDEN")
        def do_POST(self)->None:
            try:
                raw_length=self.headers.get("Content-Length")
                if raw_length is None or not raw_length.isdigit() or int(raw_length)>BODY_LIMIT:
                    raise TransportError("RUNNER_BODY_TOO_LARGE")
                body=self.rfile.read(int(raw_length))
                if len(body)!=int(raw_length):raise TransportError("RUNNER_FRAMING_INVALID")
                expected=f"127.0.0.1:{self.server.server_port}"
                request=admit(method="POST",headers=list(self.headers.raw_items()),body=body,bearer=bearer,csrf=csrf,peer_uid=os.geteuid(),effective_uid=os.geteuid(),expected_host=expected)
                result=service.run(request)
                self._json(200,result)
            except Exception as exc:self._reject(400,str(exc))
        def _reject(self,status:int,code:str)->None:self._json(status,{"status":"fail","failureCode":code[:128]})
        def _json(self,status:int,value:dict[str,object])->None:
            raw=json.dumps(value,sort_keys=True,separators=(",",":")).encode()+b"\n"
            self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(raw)));self.send_header("Cache-Control","no-store");self.end_headers();self.wfile.write(raw)
        def log_message(self,*_:object)->None:return
    server=http.server.HTTPServer(("127.0.0.1",0),Handler)
    server.socket.settimeout(5)
    value={"schemaVersion":"runner-private-control-v1","host":f"127.0.0.1:{server.server_port}","bearer":bearer,"csrf":csrf}
    control_file.parent.mkdir(mode=0o700,parents=True,exist_ok=True);control_file.write_text(json.dumps(value,sort_keys=True,separators=(",",":"))+"\n");os.chmod(control_file,0o600)
    try:server.serve_forever(poll_interval=.1)
    finally:server.server_close();control_file.unlink(missing_ok=True)


def _peer_uid(connection: socket.socket) -> int:
    if sys.platform == "darwin":
        uid=ctypes.c_uint();gid=ctypes.c_uint()
        libc=ctypes.CDLL(None,use_errno=True)
        if libc.getpeereid(connection.fileno(),ctypes.byref(uid),ctypes.byref(gid))!=0:
            raise TransportError("RUNNER_PEER_FORBIDDEN")
        return int(uid.value)
    if hasattr(socket,"SO_PEERCRED"):
        raw=connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,struct.calcsize("3i"))
        return int(struct.unpack("3i",raw)[1])
    raise TransportError("RUNNER_PEER_UNOBSERVABLE")


def serve_uds(service: object, control_file: pathlib.Path) -> None:
    bearer=secrets.token_urlsafe(32);csrf=secrets.token_urlsafe(32)
    control_file.parent.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(control_file.parent,0o700)
    socket_root=pathlib.Path(tempfile.mkdtemp(prefix=f"ai-ready-runner-{os.geteuid()}-",dir=tempfile.gettempdir()));os.chmod(socket_root,0o700);socket_path=socket_root/"control.sock"
    class Handler(http.server.BaseHTTPRequestHandler):
        server_version="";sys_version=""
        def setup(self)->None:super().setup();self.connection.settimeout(5)
        def do_OPTIONS(self)->None:self._json(403,{"status":"fail","failureCode":"RUNNER_BROWSER_REQUEST_FORBIDDEN"})
        def do_GET(self)->None:self._json(405,{"status":"fail","failureCode":"RUNNER_METHOD_FORBIDDEN"})
        def do_POST(self)->None:
            try:
                raw_length=self.headers.get("Content-Length")
                if raw_length is None or not raw_length.isdigit() or int(raw_length)>BODY_LIMIT:raise TransportError("RUNNER_BODY_TOO_LARGE")
                body=self.rfile.read(int(raw_length))
                request=admit(method="POST",headers=list(self.headers.raw_items()),body=body,bearer=bearer,csrf=csrf,peer_uid=_peer_uid(self.connection),effective_uid=os.geteuid())
                self._json(200,service.run(request))
            except Exception as exc:self._json(400,{"status":"fail","failureCode":str(exc)[:128]})
        def _json(self,status:int,value:dict[str,object])->None:
            raw=json.dumps(value,sort_keys=True,separators=(",",":")).encode()+b"\n";self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(raw)));self.send_header("Cache-Control","no-store");self.end_headers();self.wfile.write(raw)
        def log_message(self,*_:object)->None:return
    server=socketserver.UnixStreamServer(str(socket_path),Handler);os.chmod(socket_path,0o600)
    value={"schemaVersion":"runner-private-control-v1","transport":"unix","socket":str(socket_path),"bearer":bearer,"csrf":csrf}
    control_file.write_text(json.dumps(value,sort_keys=True,separators=(",",":"))+"\n");os.chmod(control_file,0o600)
    try:server.serve_forever(poll_interval=.1)
    finally:server.server_close();socket_path.unlink(missing_ok=True);control_file.unlink(missing_ok=True);socket_root.rmdir()
