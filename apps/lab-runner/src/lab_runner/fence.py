"""Runner-wide lock and monotonic fence epochs."""
from __future__ import annotations
import fcntl, os, pathlib
from dataclasses import dataclass


@dataclass(slots=True)
class Fence:
    fd: int
    epoch: int

    def close(self) -> None:
        fcntl.flock(self.fd, fcntl.LOCK_UN)
        os.close(self.fd)

    def __enter__(self) -> "Fence":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def acquire(root: pathlib.Path) -> Fence:
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(root, 0o700)
    path = root / "runner.lock"
    fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX)
    epoch_path = root / "fence.epoch"
    try:
        current = int(epoch_path.read_text()) if epoch_path.exists() else 0
    except ValueError:
        os.close(fd)
        raise RuntimeError("RUNNER_FENCE_CORRUPT")
    epoch = current + 1
    tmp = root / f".fence.{os.getpid()}.tmp"
    tmp.write_text(f"{epoch}\n")
    os.chmod(tmp, 0o600)
    os.replace(tmp, epoch_path)
    dir_fd = os.open(root, os.O_RDONLY)
    try: os.fsync(dir_fd)
    finally: os.close(dir_fd)
    return Fence(fd, epoch)
