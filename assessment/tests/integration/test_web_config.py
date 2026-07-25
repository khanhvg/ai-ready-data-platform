from __future__ import annotations

from pathlib import Path

import pytest

from assessment.web.config import WebConfig


def test_web_config_defaults_to_loopback_and_rejects_hosted_binding(tmp_path: Path) -> None:
    config = WebConfig.for_roots(tmp_path / "engagements", tmp_path / "runtime")
    assert config.host == "127.0.0.1"
    assert config.port == 8765

    with pytest.raises(ValueError, match="loopback"):
        WebConfig.for_roots(
            tmp_path / "engagements",
            tmp_path / "runtime",
            host="0.0.0.0",  # noqa: S104 -- rejection fixture
        )


def test_non_loopback_override_is_explicitly_unsupported(tmp_path: Path) -> None:
    config = WebConfig.for_roots(
        tmp_path / "engagements",
        tmp_path / "runtime",
        host="0.0.0.0",  # noqa: S104 -- explicit unsupported override fixture
        allow_unsupported_non_loopback=True,
    )
    assert config.host == "0.0.0.0"  # noqa: S104 -- asserted fixture value
    assert config.allow_unsupported_non_loopback is True
