"""Closed archive admission for private workspace and container output."""
from __future__ import annotations
import hashlib, json, os, pathlib, shutil, stat, tarfile, tempfile
from dataclasses import dataclass


class ArchiveError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class Limits:
    total_bytes: int = 268_435_456
    file_bytes: int = 134_217_728
    files: int = 4096


def _parts(name: str) -> tuple[str,...]:
    if not isinstance(name,str) or not name or "\x00" in name or "\\" in name or name.startswith("/"):
        raise ArchiveError("RUNNER_ARCHIVE_PATH_INVALID")
    try:raw_name=name.encode("ascii","strict")
    except UnicodeEncodeError as exc:raise ArchiveError("RUNNER_ARCHIVE_PATH_INVALID") from exc
    p=pathlib.PurePosixPath(name)
    if any(x in ("",".","..") for x in p.parts) or len(raw_name)>512:
        raise ArchiveError("RUNNER_ARCHIVE_PATH_INVALID")
    return p.parts


MANIFEST_NAME=".runner-output-manifest.json"


def inspect_tar(path: pathlib.Path, *, limits: Limits=Limits(), require_manifest: bool=False) -> list[dict[str,object]]:
    seen=set(); folded=set(); total=0; count=0; rows=[];manifest=None
    try:
        tf=tarfile.open(path,"r:*")
    except (tarfile.TarError,OSError) as exc: raise ArchiveError("RUNNER_ARCHIVE_INVALID") from exc
    with tf:
        for item in tf:
            parts=_parts(item.name)
            key="/".join(parts)
            collision=key.casefold()
            if key in seen or collision in folded: raise ArchiveError("RUNNER_ARCHIVE_DUPLICATE")
            seen.add(key);folded.add(collision);count+=1
            if count>limits.files:raise ArchiveError("RUNNER_ARCHIVE_QUOTA")
            if not (item.isdir() or item.isreg()) or item.issparse():
                raise ArchiveError("RUNNER_ARCHIVE_TYPE_INVALID")
            if item.uid != 65532 or item.gid != 65532:
                raise ArchiveError("RUNNER_ARCHIVE_OWNER_INVALID")
            expected_mode=0o700 if item.isdir() else 0o600
            if item.mode & 0o777 != expected_mode:raise ArchiveError("RUNNER_ARCHIVE_MODE_INVALID")
            if item.isreg():
                total+=item.size
                if item.size>limits.file_bytes or total>limits.total_bytes:
                    raise ArchiveError("RUNNER_ARCHIVE_QUOTA")
                source=tf.extractfile(item)
                if source is None:raise ArchiveError("RUNNER_ARCHIVE_INVALID")
                raw=source.read(limits.file_bytes+1)
                if len(raw)!=item.size:raise ArchiveError("RUNNER_ARCHIVE_INVALID")
                if key==MANIFEST_NAME:
                    try:manifest=json.loads(raw)
                    except json.JSONDecodeError as exc:raise ArchiveError("RUNNER_ARCHIVE_MANIFEST_INVALID") from exc
                    continue
                digest=hashlib.sha256(raw).hexdigest()
            else:digest=None
            rows.append({"path":key,"type":"directory" if item.isdir() else "file","size":item.size,"mode":item.mode & 0o777,"sha256":digest})
    if require_manifest:
        expected={"schemaVersion":"runner-output-manifest-v1","entries":rows}
        if manifest!=expected:raise ArchiveError("RUNNER_ARCHIVE_MANIFEST_INVALID")
    return rows


def extract_tar(path: pathlib.Path, destination: pathlib.Path, *, limits: Limits=Limits()) -> list[dict[str,object]]:
    rows=inspect_tar(path,limits=limits)
    if destination.exists(): raise ArchiveError("RUNNER_ARCHIVE_DESTINATION_EXISTS")
    destination.mkdir(mode=0o700,parents=True)
    try:
        with tarfile.open(path,"r:*") as tf:
            for item in tf:
                target=destination.joinpath(*_parts(item.name))
                if item.name==MANIFEST_NAME:
                    source=tf.extractfile(item)
                    if source is None:raise ArchiveError("RUNNER_ARCHIVE_INVALID")
                    target.write_bytes(source.read());os.chmod(target,0o600);continue
                target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
                if item.isdir():
                    target.mkdir(mode=0o700,exist_ok=True)
                else:
                    source=tf.extractfile(item)
                    if source is None: raise ArchiveError("RUNNER_ARCHIVE_INVALID")
                    fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,"O_NOFOLLOW",0),0o600)
                    with os.fdopen(fd,"wb") as out: shutil.copyfileobj(source,out,1024*1024)
                    os.chmod(target,0o600)
    except Exception:
        shutil.rmtree(destination,ignore_errors=True); raise
    return rows


def sha256(path: pathlib.Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
