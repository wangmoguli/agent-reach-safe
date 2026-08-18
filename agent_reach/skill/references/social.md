# 社交媒体 & 社区

小红书、B站、V2EX、Reddit、Facebook、Instagram。

## 小红书 / XiaoHongShu（OpenCLI）

小红书只保留 OpenCLI 后端（xhs-cli 与 xiaohongshu-mcp 已作为高风险后端移除）。
先跑 `agent-reach doctor --json` 看 xiaohongshu 的 `active_backend`。

```bash
# 搜索笔记
opencli xiaohongshu search "query" -f yaml

# 读笔记正文+互动数据（用搜索结果里的完整 URL，含 xsec_token）
opencli xiaohongshu note "NOTE_URL" -f yaml

# 评论（支持楼中楼）
opencli xiaohongshu comments NOTE_ID -f yaml

# 首页推荐 feed
opencli xiaohongshu feed -f yaml

# 用户主页公开笔记
opencli xiaohongshu user USER_ID -f yaml
```

> 要求 Chrome 打开且装了 OpenCLI 扩展。OpenCLI 只使用用户已经存在且明确控制
> 的 Chrome 会话；Agent Reach 不替用户登录，也不读取浏览器 Cookie。
> `agent-reach configure` 不会把 Cookie 注入 OpenCLI。
> 如果没有现成会话，不要自动登录。

### 通用注意事项

> **认证边界**: Agent Reach 不得替用户执行小红书登录，也不得读取浏览器
> Cookie。OpenCLI 只能使用用户已有且明确控制的 Chrome 会话。
>
> **xsec_token 限制**: 小红书强制 xsec_token 机制，**不能直接用裸 note_id 去读**。正确流程：先搜索/feed 拿结果，再用结果中的完整 URL/ID 去读。
>
> **频率控制**: 高频请求（批量搜索、深翻评论）会触发验证码，平台限制无法绕过。每次操作间隔 2-3 秒。
>
> **写操作（发帖/评论/点赞）**: 建议只读。

## B站 / Bilibili

> ⚠️ **不要用 yt-dlp 读 B站**（风控已全面 412 拦截，实测无解）。用 bili-cli / OpenCLI。

```bash
# 搜索 / 热门 / 视频详情（bili-cli，只读无需登录）
bili search "query" --type video -n 5
bili hot -n 10
bili video BVxxx

# 字幕（OpenCLI，需桌面 Chrome）
opencli bilibili subtitle BVxxx
```

> 详细命令（音频转写、API 直连兜底）见 [references/video.md](video.md)。

## V2EX (公开 API)

无需认证，直接调用公开 API。

### 热门主题

```bash
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
```

### 节点主题

```bash
# node_name 如: python, tech, jobs, qna, programmers
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"
```

### 主题详情

```bash
# topic_id 从 URL 获取，如 https://www.v2ex.com/t/1234567
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
```

### 主题回复

```bash
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

### 用户信息

```bash
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

### Python 调用示例

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# 获取热门帖子
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} 回复)")

# 获取节点帖子
node_topics = ch.get_node_topics("python", limit=5)

# 获取帖子详情 + 回复
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])

# 获取用户信息
user = ch.get_user("Livid")
```

> **节点列表**: https://www.v2ex.com/planes

## Reddit（OpenCLI，必须登录态）

**Reddit 没有零配置路径**：匿名 `.json` 端点已被封（403），官方 API 自 2025-11 起人工审批基本不批。Reddit 只保留 OpenCLI 后端（rdt-cli 已作为高风险后端移除）。先跑 `agent-reach doctor --json` 看 reddit 的 `active_backend`。中国大陆访问需代理。

```bash
# 搜索帖子
opencli reddit search "query" -f yaml

# 读帖子全文 + 评论
opencli reddit read POST_ID -f yaml

# 浏览 subreddit / 热门 / Popular
opencli reddit subreddit LocalLLaMA -f yaml
opencli reddit hot -f yaml
opencli reddit popular -f yaml

# subreddit 元信息（订阅数、简介）
opencli reddit subreddit-info LocalLLaMA -f yaml
```

> 要求 Chrome 打开且浏览器里登录过 reddit.com。

### 高级选项：官方 API + PRAW（仅限已有凭证的用户）

2025-11 前注册过 Reddit script app（持有 client_id/client_secret）的用户可以用 PRAW 走官方 API（100 QPM 免费）。新申请需人工审批且个人项目基本不批，**不要推荐新用户走这条路**。

## Facebook（OpenCLI，必须登录态）

Facebook 走 OpenCLI，复用用户 Chrome 里的 facebook.com 登录态。先跑 `agent-reach doctor --json` 看 facebook 的 `active_backend`，正常应为 `OpenCLI`。不要推荐 Jina/Exa/Graph API 作为默认路径。

```bash
# 搜索用户 / 主页 / 帖子
opencli facebook search "query" -f yaml

# 用户或主页信息
opencli facebook profile zuck -f yaml

# 当前账号 News Feed
opencli facebook feed --limit 10 -f yaml

# 当前账号可见的群组列表/最近动态
opencli facebook groups --limit 20 -f yaml
```

> 要求 Chrome 打开且装了 OpenCLI 扩展，并已登录 facebook.com。Facebook Groups 当前只承诺读取当前账号可见的群组列表/最近动态，不承诺任意群帖子和评论 API。

## Instagram（OpenCLI，必须登录态）

Instagram 走 OpenCLI，复用用户 Chrome 里的 instagram.com 登录态。先跑 `agent-reach doctor --json` 看 instagram 的 `active_backend`，正常应为 `OpenCLI`。不要默认恢复 instaloader；历史上 cookies/401/429 不稳定。

```bash
# 搜索用户（不是全站帖子关键词搜索）
opencli instagram search "query" -f yaml

# 用户 Profile
opencli instagram profile nasa -f yaml

# 用户最近帖子
opencli instagram user nasa --limit 12 -f yaml

# Explore / Discover
opencli instagram explore --limit 20 -f yaml

# 当前账号收藏
opencli instagram saved --limit 20 -f yaml
```

> 要求 Chrome 打开且装了 OpenCLI 扩展，并已登录 instagram.com。`instagram search` 是用户搜索；读帖子需要先确定 username，再用 `instagram user USERNAME`。若出现 429 / login required，先让用户在 Chrome 里重新登录并降低频率。
