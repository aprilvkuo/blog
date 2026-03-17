# egguo.com - 知识库网站

基于 VitePress 构建的个人知识库网站，部署在 https://egguo.com

## 🚀 快速开始

### 前置要求

- Node.js >= 18 (推荐使用最新 LTS 版本)
- pnpm >= 8

### 安装依赖

```bash
pnpm install
```

### 本地开发

```bash
pnpm run docs:dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
pnpm run docs:build
```

### 预览生产构建

```bash
pnpm run docs:preview
```

## 🚢 部署到 Cloudflare Pages

### 方式一：GitHub 自动部署（推荐）

1. 将代码推送到 GitHub

```bash
git add .
git commit -m "feat: 初始版本"
git push origin main
```

2. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
3. 进入 **Workers & Pages** → **Create application** → **Pages**
4. 连接 GitHub 仓库
5. 配置构建设置：
   - Build command: `pnpm run docs:build`
   - Output directory: `.vitepress/dist`
6. 添加自定义域名 `egguo.com`

### 方式二：命令行部署

```bash
# 登录 Cloudflare
pnpm exec wrangler login

# 部署
pnpm run pages:deploy
```

详见 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📁 项目结构

```
.
├── ai/                      # AI 相关笔记
│   ├── index.md
│   └── ml-basics.md
├── coding/                  # 编程相关笔记
│   ├── index.md
│   ├── javascript.md
│   └── typescript.md
├── finance/                 # 金融相关笔记
│   ├── index.md
│   └── asset-allocation.md
├── about/                   # 关于页面
│   └── index.md
├── .vitepress/              # VitePress 配置
│   ├── config.mts           # 主配置文件
│   └── theme/
│       ├── index.js         # 主题入口
│       └── custom.css       # 自定义样式
├── index.md                 # 首页
├── package.json
├── vercel.json              # Vercel 部署配置
└── README.md
```

## ✨ 功能特性

- ✅ 多级目录分类（AI / 编程 / 金融）
- ✅ 自动生成侧边栏
- ✅ 全文搜索（支持中文）
- ✅ 代码高亮（GitHub 主题）
- ✅ 暗黑模式支持
- ✅ 响应式设计
- ✅ SEO 优化
- ✅ 页面标题自动生成

## 📝 添加新笔记

1. 在对应分类目录下创建 `.md` 文件
2. 在文件开头添加 Frontmatter：

```markdown
---
title: 笔记标题
description: 简短描述
---

# 标题

内容...
```

3. 在 `.vitepress/config.mts` 中更新侧边栏配置

## 🚢 部署到 Vercel

### 方法一：Vercel CLI

```bash
# 安装 Vercel CLI
pnpm add -g vercel

# 登录
vercel login

# 部署
vercel

# 生产环境部署
vercel --prod
```

### 方法二：GitHub 集成（推荐）

1. 将代码推送到 GitHub

```bash
git commit -m "feat: 初始版本"
git push origin main
```

2. 访问 [Vercel](https://vercel.com)
3. 点击 "New Project"
4. 导入 GitHub 仓库
5. Vercel 会自动检测 VitePress 并配置
6. 点击 "Deploy"

### 方法三：使用 vercel.json

本项目已包含 `vercel.json` 配置文件，部署时会自动识别。

## 🔧 配置说明

### 网站信息

编辑 `.vitepress/config.mts`：

```typescript
export default defineConfig({
  title: '我的知识库',
  description: '一个基于 VitePress 的个人知识库',
  // ...
})
```

### 导航栏

```typescript
nav: [
  { text: '首页', link: '/' },
  { text: 'AI', link: '/ai/' },
  // ...
]
```

### 侧边栏

侧边栏在 `config.mts` 中配置，支持多级目录：

```typescript
sidebar: {
  '/ai/': {
    base: '/ai/',
    items: sidebarAi()
  },
  // ...
}
```

## 📐 Git 提交规范

本项目使用 Conventional Commits 规范，详见 [.gitmessage](./.gitmessage)

```bash
# 设置 commit template
git config commit.template .gitmessage

# 示例提交
git commit -m "feat(ai): 添加神经网络笔记"
```

## 🎨 自定义样式

编辑 `.vitepress/theme/custom.css` 来自定义主题样式。

## 📦 依赖

- [VitePress](https://vitepress.dev/) - 静态网站生成器
- [Vue](https://vuejs.org/) - 渐进式 JavaScript 框架

## 📄 License

MIT
