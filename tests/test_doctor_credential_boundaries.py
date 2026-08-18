"""Doctor must not claim a login-gated channel is usable without live checks."""

from __future__ import annotations

from unittest.mock import Mock, patch

from agent_reach.channels.reddit import RedditChannel
from agent_reach.channels.xiaohongshu import XiaoHongShuChannel


def _opencli(installed=True, broken=False, ready=True, hint=""):
    return Mock(installed=installed, broken=broken, ready=ready, hint=hint)


def test_reddit_doctor_does_not_claim_usable_without_live_verification():
    """OpenCLI bridge connected is still only 'warn' — never 'ok'."""
    channel = RedditChannel()
    with patch(
        "agent_reach.backends.opencli_status",
        return_value=_opencli(ready=True),
    ):
        status, message = channel.check()

    assert status == "warn"
    assert "未实时验证" in message
    assert channel.active_backend is None


def test_xiaohongshu_doctor_does_not_claim_usable_without_live_verification():
    """OpenCLI bridge connected is still only 'warn' — never 'ok'."""
    channel = XiaoHongShuChannel()
    with patch(
        "agent_reach.backends.opencli_status",
        return_value=_opencli(ready=True),
    ):
        status, message = channel.check()

    assert status == "warn"
    assert "未实时验证" in message
    assert channel.active_backend is None
