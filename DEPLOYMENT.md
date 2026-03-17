# egguo.com 部署指南 - Cloudflare Pages

## 部署方式

有两种部署方式，推荐使用 **方式一（GitHub 自动部署）**。

---

## 方式一：GitHub 自动部署（推荐）

### 1. 推送代码到 GitHub

```bash
# 初始化 Git（如果还没有）
git init
git add .
git commit -m "feat: 初始版本"

# 创建 GitHub 仓库并推送
git branch -M main
git remote add origin https://github.com/yourusername/egguo-blog.git
git push -u origin main
```

### 2. 在 Cloudflare 创建 Pages 项目

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 **Workers & Pages** → **Create application** → **Pages**
3. 点击 **Connect to Git**
4. 选择你的 `egguo-blog` 仓库
5. 配置构建设置：
   - **Framework preset**: None
   - **Build command**: `pnpm run docs:build`
   - **Build output directory**: `.vitepress/dist`
   - **Root directory**: `/`
6. 点击 **Save and Deploy**

### 3. 配置自定义域名

1. 进入 Pages 项目 **Settings** → **Custom domains**
2. 点击 **Add custom domain**
3. 输入 `egguo.com`
4. Cloudflare 会自动配置 DNS

### 4. 自动部署

之后每次 push 到 main 分支，Cloudflare 会自动构建并部署。

---

## 方式二：命令行直接部署

### 1. 登录 Cloudflare

```bash
pnpm exec wrangler login
```

会打开浏览器，授权登录。

### 2. 创建 Pages 项目

```bash
pnpm exec wrangler pages project create egguo-blog \
  --production-branch=main \
  --build-command="pnpm run docs:build" \
  --build-output-directory=".vitepress/dist"
```

### 3. 部署

```bash
# 构建
pnpm run docs:build

# 部署
pnpm run pages:deploy
```

或直接使用命令：

```bash
pnpm exec wrangler pages deploy .vitepress/dist --project-name=egguo-blog
```

### 4. 绑定自定义域名

```bash
pnpm exec wrangler pages project update egguo-blog \
  --production-branch=main \
  --domains=egguo.com
```

或者在 Cloudflare Dashboard 中操作：
- 进入 **Workers & Pages** → 选择 `egguo-blog` → **Settings** → **Custom domains**
- 点击 **Add custom domain**，输入 `egguo.com`

---

## DNS 配置

Cloudflare Pages 会自动配置 DNS，无需手动设置。

如果想手动配置，可以添加以下 DNS 记录：

| 类型 | 名称 | 内容 | TTL |
|------|------|------|-----|
| CNAME | @ | `egguo-blog.pages.dev` | Auto |
| CNAME | www | `egguo-blog.pages.dev` | Auto |

---

## 预览部署

每次推送到非 main 分支，Cloudflare 会创建预览部署：

```bash
# 创建新分支
git checkout -b feature/new-note
git push origin feature/new-note

# 在 Cloudflare Dashboard 查看预览链接
```

---

## 查看部署状态

- **Dashboard**: https://dash.cloudflare.com/
- **项目页面**: Workers & Pages → egguo-blog
- **部署历史**: 查看每次构建状态和日志

---

## 环境变量（如需要）

在 Cloudflare Dashboard 中设置：

1. 进入 Pages 项目
2. **Settings** → **Environment variables**
3. 添加变量
4. 重新部署

---

## 免费额度

Cloudflare Pages 免费套餐：

| 资源 | 额度 |
|------|------|
| 网站数量 | 无限 |
| 带宽 | 无限 |
| 请求数 | 无限 |
| 构建时间 | 500 分钟/月 |
| 自定义域名 | ✅ 免费 |
| HTTPS | ✅ 免费 |

---

## 故障排查

### 构建失败

检查构建日志，常见原因：
- Node 版本不匹配（配置中已设置 NODE_VERSION = "20"）
- 依赖安装失败
- Markdown 语法错误

### 部署后页面空白

- 检查 `.vitepress/dist` 目录是否正确生成
- 查看浏览器控制台错误

### 自定义域名不生效

- 检查 DNS 是否生效：`dig egguo.com`
- 清除 Cloudflare 缓存：**Caching** → **Configuration** → **Purge Everything**

---

## 回滚到旧版本

在 Cloudflare Dashboard：

1. 进入 **Deployment** 标签
2. 找到要回滚的版本
3. 点击 **...** → **Roll back to this deployment**
