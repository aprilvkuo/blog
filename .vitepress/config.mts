import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  // 站点级配置
  title: 'Egg Guo 的知识库',
  titleTemplate: ':title | egguo.com',
  description: '一个基于 VitePress 的个人知识库 - AI、编程、金融',
  lastUpdated: true,

  // 站点 URL 配置（用于 SEO 和 RSS）
  srcDir: '.',
  cleanUrls: true,

  // SEO 相关配置
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico', type: 'image/png' }],
    ['meta', { name: 'keywords', content: '笔记，知识库，技术博客，AI，编程，金融，egguo' }],
    ['meta', { name: 'author', content: 'Egg Guo' }],
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ['meta', { property: 'og:title', content: 'Egg Guo 的知识库' }],
    ['meta', { property: 'og:description', content: '一个基于 VitePress 的个人知识库 - AI、编程、金融' }],
    ['meta', { property: 'og:url', content: 'https://egguo.com' }],
    ['meta', { property: 'og:site_name', content: 'egguo.com' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    ['meta', { name: 'twitter:title', content: 'Egg Guo 的知识库' }],
    ['meta', { name: 'twitter:description', content: '一个基于 VitePress 的个人知识库 - AI、编程、金融' }],
  ],

  // 主题级配置
  themeConfig: {
    // 网站标题（左上角）
    siteTitle: 'egguo.com',

    // 导航栏
    nav: [
      { text: '首页', link: '/' },
      { text: 'AI', link: '/ai/' },
      { text: '编程', link: '/coding/' },
      { text: '金融', link: '/finance/' },
      { text: '关于', link: '/about/' },
    ],

    // 侧边栏 - 配置为根据目录结构自动生成
    sidebar: {
      '/ai/': { base: '/ai/', items: sidebarAi() },
      '/coding/': { base: '/coding/', items: sidebarCoding() },
      '/finance/': { base: '/finance/', items: sidebarFinance() },
      '/about/': { base: '/about/', items: sidebarAbout() },
    },

    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/aprilvkuo' },
    ],

    // 页脚
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026-present Egg Guo @ egguo.com',
    },

    // 搜索配置 - 使用 VitePress 内置搜索
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索',
                buttonAriaLabel: '搜索文档',
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                },
              },
            },
          },
        },
      },
    },

    // 暗黑模式支持（默认开启）
    colorMode: 'auto',

    // 文档编辑链接
    editLink: {
      pattern: 'https://github.com/yourusername/yourrepo/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页面',
    },

    // 返回顶部
    returnToTop: true,

    // 大纲配置
    outline: {
      label: '页面导航',
      level: [2, 3],
    },

    // 上/下一篇
    docFooter: {
      prev: '上一页',
      next: '下一页',
    },
  },

  // Markdown 配置
  markdown: {
    // 代码高亮主题
    theme: {
      light: 'github-light',
      dark: 'github-dark',
    },
    // 行号
    lineNumbers: true,
  },

  // 忽略死链检查
  ignoreDeadLinks: true,

  // Vite 配置
  vite: {
    // 自定义 Vite 配置
  },
})

// 侧边栏配置函数 - 可以根据需要手动或使用工具生成
function sidebarAi() {
  return [
    {
      text: 'AI 基础',
      collapsed: false,
      items: [
        { text: '概述', link: 'index' },
        { text: '机器学习基础', link: 'ml-basics' },
      ],
    },
    {
      text: 'AutoGen 学习笔记',
      collapsed: true,
      items: [
        { text: '索引', link: 'autogen/index' },
        {
          text: 'Core 核心概念',
          collapsed: true,
          items: [
            { text: '总览', link: 'autogen/01-Core/00-Core 核心概念总览' },
            { text: 'Agent 和 Runtime', link: 'autogen/01-Core/01-Agent 和 Runtime' },
            { text: '消息传递机制', link: 'autogen/01-Core/02-消息传递机制' },
            { text: '订阅和主题', link: 'autogen/01-Core/03-订阅和主题' },
            { text: '路由和匹配', link: 'autogen/01-Core/04-路由和匹配' },
          ],
        },
        {
          text: 'AgentChat 高层 API',
          collapsed: true,
          items: [
            { text: '总览', link: 'autogen/02-AgentChat/00-AgentChat 总览' },
            { text: 'AssistantAgent', link: 'autogen/02-AgentChat/01-AssistantAgent' },
            { text: '群聊模式', link: 'autogen/02-AgentChat/02-群聊模式' },
            { text: '终止条件', link: 'autogen/02-AgentChat/03-终止条件' },
          ],
        },
        {
          text: 'Ext 扩展机制',
          collapsed: true,
          items: [
            { text: '总览', link: 'autogen/03-Ext/00-Ext 扩展机制总览' },
            { text: '模型客户端', link: 'autogen/03-Ext/01-模型客户端' },
            { text: '工具和工作台', link: 'autogen/03-Ext/02-工具和工作台' },
            { text: 'MCP 集成', link: 'autogen/03-Ext/03-MCP 集成' },
          ],
        },
        {
          text: '实战示例',
          collapsed: true,
          items: [
            { text: '总览', link: 'autogen/04-实战/00-实战示例总览' },
            { text: 'HelloAgent', link: 'autogen/04-实战/01-HelloAgent' },
            { text: '发布订阅', link: 'autogen/04-实战/02-发布订阅' },
            { text: '消息路由', link: 'autogen/04-实战/03-消息路由' },
            { text: '多 Agent 协作', link: 'autogen/04-实战/04-多 Agent 协作' },
          ],
        },
      ],
    },
  ]
}

function sidebarCoding() {
  return [
    {
      text: '前端开发',
      collapsed: false,
      items: [
        { text: '概述', link: 'index' },
        { text: 'JavaScript', link: 'javascript' },
        { text: 'TypeScript', link: 'typescript' },
      ],
    },
    {
      text: '后端开发',
      collapsed: true,
      items: [
        { text: 'Node.js', link: 'nodejs' },
        { text: '数据库', link: 'database' },
      ],
    },
  ]
}

function sidebarFinance() {
  return [
    {
      text: '投资基础',
      collapsed: false,
      items: [
        { text: '概述', link: 'index' },
        { text: '资产配置', link: 'asset-allocation' },
      ],
    },
    {
      text: '量化交易',
      collapsed: true,
      items: [
        { text: '策略基础', link: 'strategy-basics' },
        { text: '回测方法', link: 'backtesting' },
      ],
    },
    {
      text: '股票分析',
      collapsed: true,
      items: [
        { text: '总览', link: '/stock-analysis/' },
        { text: '000001.SS 平安银行', link: '/stock-analysis/000001.SS/' },
        { text: '0700.HK 腾讯控股', link: '/stock-analysis/0700.HK/' },
        { text: '300750.SZ 宁德时代', link: '/stock-analysis/300750.SZ/' },
        { text: '300760.SZ 迈瑞医疗', link: '/stock-analysis/300760.SZ/' },
        { text: '600036.SS 招商银行', link: '/stock-analysis/600036.SS/' },
        { text: '600519.SS 贵州茅台', link: '/stock-analysis/600519.SS/' },
        { text: 'BABA 阿里巴巴', link: '/stock-analysis/BABA/' },
        { text: 'DIS 迪士尼', link: '/stock-analysis/DIS/' },
        { text: 'HK 香港', link: '/stock-analysis/HK/' },
        { text: 'MSFT 微软', link: '/stock-analysis/MSFT/' },
        { text: 'PDD 拼多多', link: '/stock-analysis/PDD/' },
        { text: 'QQQ 纳斯达克 ETF', link: '/stock-analysis/QQQ/' },
        { text: 'SPY 标普 500ETF', link: '/stock-analysis/SPY/' },
      ],
    },
  ]
}

function sidebarAbout() {
  return [
    {
      text: '关于',
      items: [
        { text: '关于本站', link: 'index' },
      ],
    },
  ]
}
