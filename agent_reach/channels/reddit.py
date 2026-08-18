# -*- coding: utf-8 -*-
"""Reddit — OpenCLI backend only (reuses the user's real browser session).

Login is mandatory: there is no zero-config path. Anonymous .json endpoints
are blocked (403 anti-bot), and the official API closed self-service
registration in 2025-11. The rdt-cli cookie-scraping backend was removed as a
high ban-risk path — OpenCLI reuses the user's already-logged-in Chrome
session instead, which keeps Reddit access in the low/moderate-risk tier.
"""

from .base import Channel


class RedditChannel(Channel):
    name = "reddit"
    description = "Reddit 帖子和评论"
    backends = ["OpenCLI"]
    tier = 1  # no zero-config path exists — see module docstring

    def can_handle(self, url: str) -> bool:
        from agent_reach.utils.url import host_matches

        return host_matches(url, "reddit.com", "redd.it")

    def check(self, config=None):
        """Probe OpenCLI; never claim "ok" without a live login check."""
        self.active_backend = None

        result = self._check_opencli()
        if result is None:
            return "off", (
                "未安装 Reddit 后端。注意：Reddit 没有零配置路径"
                "（匿名 .json 已被封，官方 API 需人工审批），必须用登录态。推荐：\n"
                "  桌面：agent-reach install --system --channels opencli\n"
                "       （复用 Chrome 登录态，登录过 reddit.com 即可用）\n"
                "中国大陆访问 Reddit 需要代理"
            )
        status, message = result
        if status == "ok":
            self.active_backend = "OpenCLI"
        return status, message

    def _check_opencli(self):
        """OpenCLI candidate. None = not installed."""
        from agent_reach.backends import opencli_status

        st = opencli_status()
        if not st.installed:
            return None
        if st.broken:
            return "error", st.hint
        if st.ready:
            return "warn", (
                "OpenCLI 桥接已连接，但 Reddit 登录态和实际命令未实时验证；"
                "Doctor 不执行平台命令，因此当前不标记为可用。"
            )
        return "warn", st.hint
