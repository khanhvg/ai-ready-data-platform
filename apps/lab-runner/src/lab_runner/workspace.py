"""Private workspace generations encoded as deterministic tar archives."""
from __future__ import annotations
import io, os, pathlib, tarfile, tempfile
from .archive import extract_tar, inspect_tar


class Workspace:
    def __init__(self, root: pathlib.Path):
        self.root=root; root.mkdir(mode=0o700,parents=True,exist_ok=True); os.chmod(root,0o700)
        (root/"generations").mkdir(mode=0o700,exist_ok=True)

    def input_archive(self, revision: int, output: pathlib.Path) -> None:
        current=self.root/"current"
        if current.is_symlink():
            source=(self.root/current.readlink()).resolve()
            if source.parent != (self.root/"generations").resolve(): raise RuntimeError("RUNNER_WORKSPACE_POINTER_INVALID")
            output.write_bytes(source.read_bytes()); return
        with tarfile.open(output,"w"):
            pass
        os.chmod(output,0o600)

    def commit(self, archive: pathlib.Path, revision: int) -> pathlib.Path:
        inspect_tar(archive)
        generation=self.root/"generations"/f"{revision:020d}.tar"
        if generation.exists():
            if generation.read_bytes()!=archive.read_bytes(): raise RuntimeError("RUNNER_WORKSPACE_GENERATION_CONFLICT")
        else:
            tmp=self.root/"generations"/f".{revision}.{os.getpid()}.tmp"
            tmp.write_bytes(archive.read_bytes()); os.chmod(tmp,0o600)
            fd=os.open(tmp,os.O_RDONLY); os.fsync(fd); os.close(fd); os.replace(tmp,generation)
        link_tmp=self.root/f".current.{os.getpid()}"
        try: link_tmp.symlink_to(pathlib.Path("generations")/generation.name); os.replace(link_tmp,self.root/"current")
        finally:
            if link_tmp.exists() or link_tmp.is_symlink(): link_tmp.unlink()
        dfd=os.open(self.root,os.O_RDONLY); os.fsync(dfd); os.close(dfd)
        return generation
