# 股票分析功能配置指南

## 概述

此功能允许用户通过网站提交股票分析请求，请求会通过 Cloudflare Pages Functions 发送到任务队列，本地 Python 脚本轮询并执行分析。

**⚠️ 注意：当前版本无认证机制，建议仅在私有站点或可信环境中使用。**

## 架构

```
用户 → Cloudflare Pages (API) → KV 存储 → 本地轮询脚本 → TradingAgents → Git 推送
```

## 配置步骤

### 1. 创建 Cloudflare KV Namespace

```bash
# 使用 wrangler 创建 KV namespace
wrangler kv:namespace create "stock-analysis-tasks"
```

运行后会输出：
```
✨ Success! Created namespace "stock-analysis-tasks" with ID "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**记下这个 ID**，后面会用到。

### 2. 运行设置脚本（可选）

```bash
python3 scripts/setup-stock-analysis.py
```

脚本会自动：
- 创建 KV namespace
- 更新 `wrangler.toml`
- 提供环境变量配置提示

### 3. 配置本地环境变量

在你的机器上（运行轮询脚本的机器）设置：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export CLOUDFLARE_API_TOKEN="your_cloudflare_api_token"
export CLOUDFLARE_ACCOUNT_ID="your_account_id"
export KV_NAMESPACE_ID="your_kv_namespace_id"
```

**获取 Cloudflare API Token**:
1. 访问 https://dash.cloudflare.com/profile/api-tokens
2. 创建新的 API Token
3. 权限：`Account.Account Holdings` 和 `Workers.KV Storage`

**获取 Account ID**:
1. 访问 Cloudflare Dashboard
2. 右侧显示 Account ID

### 4. 部署到 Cloudflare Pages

```bash
pnpm run pages:deploy
```

### 5. 运行轮询脚本

在你的机器上：

```bash
cd /Users/egg/Project/blog
python3 scripts/poll-tasks.py
```

建议使用 `tmux` 或 `screen` 后台运行：

```bash
# 创建 tmux 会话
tmux new -s stock-poller

# 运行脚本
python3 scripts/poll-tasks.py

# 按 Ctrl+B 然后 D 分离会话
```

## 使用流程

1. 用户在网站 `/finance/analyze` 提交分析请求
2. Cloudflare API 接收请求并存入 KV
3. 轮询脚本检测到新任务
4. 执行 `python -m cli.main -t {股票}`
5. 复制报告到 `stock-analysis/` 目录
6. Git 提交并推送
7. 前端显示完成状态和报告链接

## 前端组件使用

在任何页面中使用 `<StockAnalyzer />` 组件：

```markdown
---
title: 我的页面
---

# 股票分析

<StockAnalyzer />
```

## 环境变量参考

| 变量名 | 说明 | 来源 |
|--------|------|------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API Token | Cloudflare Dashboard |
| `CLOUDFLARE_ACCOUNT_ID` | Account ID | Cloudflare Dashboard |
| `KV_NAMESPACE_ID` | KV Namespace ID | `wrangler kv:namespace create` |

## 故障排查

### API 返回 404
- 确认 Functions 已部署：`pnpm run pages:deploy`
- 检查 Cloudflare Pages 后台是否有 functions

### 轮询脚本无法连接 KV
- 检查 API Token 权限
- 确认 Account ID 和 Namespace ID 正确

### 任务一直处于 pending
- 确认轮询脚本正在运行
- 检查脚本日志输出

### Git 推送失败
- 确认机器上有 git 配置
- 检查 SSH key 或 token 权限

## 安全考虑

⚠️ **当前版本禁用认证，存在以下风险：**

1. **任何人可以提交分析请求** - 可能导致滥用
2. **消耗你的机器资源** - 每次分析会运行 Python 脚本
3. **消耗 Cloudflare KV 配额** - 免费额度有限

**建议的缓解措施：**
- 在可信环境部署（内网、密码保护）
- 添加简单的请求频率限制（在 Pages Function 中）
- 监控 KV 使用量
- 未来可以添加用户登录系统
