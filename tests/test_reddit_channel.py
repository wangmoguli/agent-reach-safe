# -*- coding: utf-8 -*-
"""Dedicated tests for Reddit's read-only OpenCLI health check."""

from unittest.mock import Mock, patch

from agent_reach.channels.reddit import RedditChannel


def test_can_handle_matches_reddit_hosts():
    channel = RedditChannel()
    for url in [
        "https://reddit.com/r/python",
        "https://www.reddit.com/r/python/comments/abc/title/",
        "https://old.reddit.com/r/python",
        "https://redd.it/abc123",
        "HTTPS://REDDIT.COM/r/Python",
    ]:
        assert channel.can_handle(url) is True, url


def test_can_handle_rejects_non_reddit():
    channel = RedditChannel()
    for url in ["https://example.com/r/python", "https://x.com/u", ""]:
        assert channel.can_handle(url) is False, url


def _opencli(installed=True, broken=False, ready=True, hint=""):
    return Mock(installed=installed, broken=broken, ready=ready, hint=hint)


def test_check_opencli_not_installed_is_none():
    with patch(
        "agent_reach.backends.opencli_status",
        return_value=_opencli(installed=False),
    ):
        assert RedditChannel()._check_opencli() is None


def test_check_opencli_broken_is_error():
    with patch(
        "agent_reach.backends.opencli_status",
        return_value=_opencli(broken=True, hint="reinstall opencli"),
    ):
        status, message = RedditChannel()._check_opencli()
    assert status == "error"
    assert message == "reinstall opencli"


def test_check_opencli_bridge_ready_is_unverified():
    with patch(
        "agent_reach.backends.opencli_status",
        return_value=_opencli(ready=True),
    ):
        status, message = RedditChannel()._check_opencli()
    assert status == "warn"
    assert "桥接已连接" in message
    assert "登录态和实际命令未实时验证" in message


def test_check_opencli_installed_not_ready_is_warn():
    with patch(
        "agent_reach.backends.opencli_status",
        return_value=_opencli(ready=False, hint="connect the extension"),
    ):
        status, message = RedditChannel()._check_opencli()
    assert status == "warn"
    assert message == "connect the extension"


def test_check_no_backend_installed_is_off():
    channel = RedditChannel()
    with patch.object(channel, "_check_opencli", return_value=None):
        status, message = channel.check()

    assert status == "off"
    assert "零配置" in message
    assert channel.active_backend is None


def test_check_opencli_unverified_is_warn_without_active_backend():
    channel = RedditChannel()
    with patch.object(
        channel, "_check_opencli", return_value=("warn", "not ready")
    ):
        status, message = channel.check()

    assert status == "warn"
    assert message == "not ready"
    assert channel.active_backend is None
