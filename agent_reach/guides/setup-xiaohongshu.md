# 小红书配置指南

## 功能说明
读取和搜索小红书笔记。小红书只保留 OpenCLI 后端（xhs-cli 与
xiaohongshu-mcp 已作为高风险后端移除）。

## 前置条件
- OpenCLI：用户已经存在且明确控制的 Chrome 小红书会话

## 认证边界

Agent Reach 不替用户执行小红书登录，也不读取浏览器 Cookie。

OpenCLI 只使用用户已经存在且明确控制的 Chrome 会话。
`agent-reach configure` 不会把 Cookie 注入 OpenCLI 或 Chrome。
如果没有现成会话，不要自动登录。

## 使用示例

```bash
# 搜索笔记
opencli xiaohongshu search "关键词" -f yaml

# 读笔记（用搜索结果里的完整 URL，含 xsec_token）
opencli xiaohongshu note "NOTE_URL" -f yaml

# 评论
opencli xiaohongshu comments NOTE_ID -f yaml
```

## 常见问题

**Q: 小红书提示 IP 风险？**
A: 推荐使用住宅代理：`export HTTP_PROXY="http://user:pass@ip:port"`。

**Q: 没有现成登录会话？**
A: 先在 Chrome 里登录 xiaohongshu.com，保持浏览器打开，再运行命令。
