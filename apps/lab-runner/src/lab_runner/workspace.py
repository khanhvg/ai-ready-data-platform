"""Private workspace generations encoded as deterministic tar archives."""
from __future__ import annotations
import os, pathlib, stat, tarfile
from .archive import extract_tar, inspect_tar


class Workspace:
    def __init__(self, root: pathlib.Path):
        self.root=root; root.mkdir(mode=0o700,parents=True,exist_ok=True); os.chmod(root,0o700)
        (root/"generations").mkdir(mode=0o700,exist_ok=True)

    def input_archive(self, revision: int, output: pathlib.Path) -> None:
        root_fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY)
        try:
            try: pointer=os.readlink("current",dir_fd=root_fd)
            except FileNotFoundError: pointer=None
            if pointer is not None:
                parts=pathlib.PurePosixPath(pointer).parts
                if len(parts)!=2 or parts[0]!="generations" or len(parts[1])!=24 or not parts[1].endswith(".tar") or not parts[1][:-4].isdigit():
                    raise RuntimeError("RUNNER_WORKSPACE_POINTER_INVALID")
                source_fd=os.open(pointer,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0),dir_fd=root_fd)
                try:
                    observed=os.fstat(source_fd)
                    if not stat.S_ISREG(observed.st_mode) or observed.st_nlink!=1: raise RuntimeError("RUNNER_WORKSPACE_POINTER_INVALID")
                    target_fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,"O_NOFOLLOW",0),0o600)
                    try:
                        while chunk:=os.read(source_fd,1024*1024): os.write(target_fd,chunk)
                        os.fsync(target_fd)
                    finally: os.close(target_fd)
                finally: os.close(source_fd)
                return
        finally: os.close(root_fd)
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
