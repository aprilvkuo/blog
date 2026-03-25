# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 命令

```bash
# 安装依赖
pnpm install

# 本地开发（启动 VitePress 开发服务器）
pnpm run docs:dev

# 构建生产版本
pnpm run docs:build

# 预览生产构建
pnpm run docs:preview

# 部署到 Cloudflare Pages
pnpm run pages:deploy
```

## 架构和结构

- **VitePress 驱动的知识库网站** - 基于 Vue 3 的静态网站生成器
- **开发服务器** - `pnpm run docs:dev` 启动 VitePress dev server，默认端口 5173
- **构建输出** - `pnpm run docs:build` 生成到 `.vitepress/dist` 目录
- **部署目标** - Cloudflare Pages（通过 `wrangler pages deploy`）

### 目录结构

```
.
├── ai/                      # AI 相关笔记（机器学习、AutoGen 等）
├── coding/                  # 编程相关笔记（JavaScript、TypeScript 等）
├── finance/                 # 金融相关笔记（资产配置、量化交易等）
├── stock-analysis/          # 股票分析报告（由脚本自动生成）
├── about/                   # 关于页面
├── .vitepress/              # VitePress 配置
│   ├── config.mts           # 主配置文件（站点配置、主题、侧边栏）
│   └── theme/
│       ├── index.js         # 主题入口（扩展 DefaultTheme）
│       └── custom.css       # 自定义样式
├── index.md                 # 首页
├── scripts/                 # 工具脚本
│   └── sync-stocks.py       # 股票分析报告同步脚本（Python）
└── package.json
```

### 配置

- **配置文件**: `.vitepress/config.mts` - 定义站点标题、导航、侧边栏、搜索、SEO 等
- **侧边栏**: 在 `config.mts` 中通过 `sidebarAi()`, `sidebarCoding()`, `sidebarFinance()` 函数定义
- **主题**: `.vitepress/theme/index.js` 扩展 `DefaultTheme`，可添加自定义 Vue 组件

### 新增笔记

1. 在对应分类目录下创建 `.md` 文件（如 `ai/new-topic.md`）
2. 在文件开头添加 Frontmatter:
   ```markdown
   ---
   title: 笔记标题
   description: 简短描述
   ---
   ```
3. 在 `.vitepress/config.mts` 中更新对应侧边栏函数

## Git 提交规范

项目使用 Conventional Commits 规范，详见 `.gitmessage`：

```bash
# 设置 commit template
git config commit.template .gitmessage

# 示例：feat(ai): 添加神经网络笔记
```

常见 type: `feat`, `fix`, `docs`, `refactor`, `chore`
scope: `ai`, `coding`, `finance`, `about`, `config`, `deps`, `stocks`

## 股票分析集成

股票分析报告由 TradingAgents 系统生成，自动同步到 `stock-analysis/` 目录。

### 同步报告

```bash
# 手动同步股票分析报告（默认同步历史报告）
python3 scripts/sync-stocks.py

# 仅同步最新报告（不生成历史记录）
SYNC_HISTORY=false python3 scripts/sync-stocks.py
```

### 目录结构

```
stock-analysis/
├── index.md                 # 股票分析主页
├── {SYMBOL}/                # 每只股票的目录
│   ├── index.md             # 股票导航页
│   └── latest/              # 最新报告（复制自 TradingAgents）
│       ├── complete_report.md
│       ├── final_trade_decision.md
│       ├── 1_analysts/      # 分析师报告
│       ├── 2_research/      # 研究报告
│       ├── 3_trading/       # 交易计划
│       ├── 4_risk/          # 风险评估
│       └── 5_portfolio/     # 投资决策
```

### GitHub Action 自动同步

- **时间**: 每天北京时间 00:00（UTC 16:00）
- **Workflow**: `.github/workflows/daily-stock-sync.yml`
- **触发**: 定时任务或手动触发（workflow_dispatch）
