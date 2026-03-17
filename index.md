---
layout: home
hero:
  name: egguo.com
  text: 记录学习与思考
  tagline: AI · 编程 · 金融
  image:
    src: /hero.png
    alt: VitePress
  actions:
    - theme: brand
      text: 开始浏览
      link: /ai/
    - theme: alt
      text: 关于本站
      link: /about/

features:
  - icon: 🤖
    title: 人工智能
    details: 机器学习、深度学习、大语言模型等 AI 相关笔记
    link: /ai/
    linkText: 探索 AI
  - icon: 💻
    title: 编程开发
    details: 前端、后端、工具链、架构设计等技术总结
    link: /coding/
    linkText: 查看编程
  - icon: 📈
    title: 金融投资
    details: 投资理论、量化交易、市场分析等金融知识
    link: /finance/
    linkText: 学习金融
---

<script setup>
import { VPTeamMembers } from 'vitepress/theme'

const members = [
  {
    avatar: 'https://www.github.com/github.png',
    name: 'Egg',
    title: 'Creator',
    links: [
      { icon: 'github', link: 'https://github.com/yourusername' },
      { icon: 'twitter', link: 'https://twitter.com/yourusername' }
    ]
  }
]
</script>

## 最近更新

<!-- 这里可以手动或通过脚本生成最近更新列表 -->

- 2026-03-17: 网站正式上线
- 2026-03-16: 添加 Transformer 笔记
- 2026-03-15: 完成 JavaScript 基础整理

## 关于本站

本站使用 [VitePress](https://vitepress.dev/) 构建，这是一个静态网站生成器，专为文档和知识库设计。

<VPTeamMembers size="small" :members="members" />
