# Reddit 配置指南

## 功能说明

Reddit 封锁了几乎所有非浏览器的直接访问（包括数据中心和 ISP 代理 IP），JSON API 返回 403。

Agent Reach 通过 **OpenCLI**（复用用户真实 Chrome 会话）实现 Reddit 的搜索和阅读：
- **搜索**：`opencli reddit search "关键词" -f yaml`
- **阅读完整帖子+评论**：`opencli reddit read POST_ID -f yaml`

需要桌面 Chrome + OpenCLI 扩展，浏览器里登录过 reddit.com。
rdt-cli 已作为高风险后端移除。

## Agent 可自动完成的步骤

一键安装 OpenCLI：

```bash
agent-reach install --env=auto --system --channels=opencli
```

## 使用示例

```bash
opencli reddit search "python best practices" -f yaml
opencli reddit read POST_ID -f yaml
```

## Fallback：Exa 搜索

如果你已经配置了 Exa（通过 mcporter），也可以通过 Exa 搜索 Reddit 内容：

```bash
mcporter call exa.web_search_exa query="site:reddit.com python best practices" numResults=5
```
