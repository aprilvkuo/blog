---
title: Skills 技能系统
type: concept
---

# Skills 技能系统

> **定义**: 以 Markdown 格式定义的 Agent 专业技能模块，包含工作流程、最佳实践和工具依赖，支持渐进式加载。

## 核心要点

- **Markdown 定义**：低门槛，开发者/研究者可轻松定制
- **渐进加载**：按需激活，不一次性塞进上下文
- **可组合**：一个技能可调用其他技能
- **可扩展**：支持 `.skill` 归档安装，含版本/作者/兼容性元数据

## 结构示例

```markdown
# SKILL.md

---
version: 1.0
author: deerflow-team
compatibility: deerflow-2.0+
---

## 技能名称
research - 深度研究技能

## 工作流程
1. 信息收集 → 2. 信息整理 → 3. 报告生成

## 最佳实践
- 并行搜索多个关键词
- 结构化整理信息
- 生成带引用的报告

## 工具依赖
- web-search
- web-fetch
- file-ops
```

## 文件结构

```
/mnt/skills/
├── public/              # 内置技能
│   ├── research/SKILL.md
│   ├── report-generation/SKILL.md
│   ├── slide-creation/SKILL.md
│   └── web-page/SKILL.md
│
└── custom/              # 自定义技能
    └── your-skill/SKILL.md
```

## 设计理念

| 问题 | 解决方案 |
|------|----------|
| Agent 从零学习成本高 | 提供成熟工作流程 |
| 一次性加载所有技能撑爆上下文 | 渐进式加载，按需激活 |
| 技能不可组合 | 支持技能间调用 |

## 相关论文

- [[DeerFlow]]: 提出 Skills 系统概念

## 相关概念

- [[AgentSkills]]: OpenHands 的工具函数库（基础工具，非工作流）
- [[Context Engineering]]: 渐进加载是上下文管理的一部分