"""Explicit, loopback-only web runtime configuration."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from pathlib import Path

from assessment.storage.limits import MAX_ARCHIVE_BYTES, MAX_FILE_BYTES


def _is_loopback(host: str) -> bool:
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@dataclass(frozen=True)
class WebConfig:
    engagement_root: Path
    runtime_root: Path
    host: str = "127.0.0.1"
    port: int = 8765
    allow_unsupported_non_loopback: bool = False
    max_upload_bytes: int = MAX_ARCHIVE_BYTES
    max_evidence_bytes: int = MAX_FILE_BYTES

    def __post_init__(self) -> None:
        if not _is_loopback(self.host) and not self.allow_unsupported_non_loopback:
            raise ValueError(
                "assessment web host must be a literal loopback address; "
                "the unsupported development override is required otherwise"
            )
        if not 1 <= self.port <= 65535:
            raise ValueError("assessment web port must be from 1 to 65535")
        if self.max_upload_bytes <= 0 or self.max_evidence_bytes <= 0:
            raise ValueError("assessment upload limits must be positive")

    @classmethod
    def for_roots(
        cls,
        engagement_root: Path,
        runtime_root: Path,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
        allow_unsupported_non_loopback: bool = False,
    ) -> WebConfig:
        return cls(
            engagement_root=engagement_root.absolute(),
            runtime_root=runtime_root.absolute(),
            host=host,
            port=port,
            allow_unsupported_non_loopback=allow_unsupported_non_loopback,
        )

    @property
    def allowed_hosts(self) -> list[str]:
        hosts = [self.host]
        if _is_loopback(self.host):
            hosts.extend(["127.0.0.1", "::1"])
        return sorted(set(hosts))

    @property
    def allowed_origins(self) -> frozenset[str]:
        origins: set[str] = set()
        for host in self.allowed_hosts:
            formatted = f"[{host}]" if ":" in host else host
            origins.add(f"http://{formatted}")
            origins.add(f"http://{formatted}:{self.port}")
        return frozenset(origins)
