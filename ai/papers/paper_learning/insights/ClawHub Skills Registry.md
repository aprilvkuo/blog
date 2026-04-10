---
title: ClawHub Skills Registry
type: concept
---

# ClawHub Skills Registry

> **定义**: OpenClaw 的技能注册中心，包含 5400+ 预构建技能，按类别组织，可一键安装。

## 核心特点

1. **规模**: 5,400+ 技能，官方筛选和分类
2. **位置**: ~/.openclaw/workspace/skills/<skill>/SKILL.md
3. **格式**: Markdown 定义，无需编程
4. **来源**: 社区贡献 + 官方审核

## 技能结构

```
~/.openclaw/workspace/skills/
├── productivity/
│   ├── calendar/SKILL.md
│   ├── reminders/SKILL.md
│   └── notes/SKILL.md
├── automation/
│   ├── cron-jobs/SKILL.md
│   ├── webhooks/SKILL.md
│   └── gmail/SKILL.md
├── communication/
│   ├── email/SKILL.md
│   ├── sms/SKILL.md
│   └── notifications/SKILL.md
└── development/
    ├── browser/SKILL.md
    ├── canvas/SKILL.md
    └── system/SKILL.md
```

## 与 DeerFlow Skills 的区别

| 维度 | OpenClaw ClawHub | DeerFlow Skills |
|------|------------------|-----------------|
| **数量** | 5400+ | 用户自定义 |
| **来源** | 社区贡献 | 本地编写 |
| **发现** | 自动搜索 (ClawHub.com) | 手动加载 |
| **审核** | 官方筛选 | 无 |

## 使用方式

```bash
# Agent 自动搜索技能
# ClawHub enabled 时，Agent 会自动搜索并拉取所需技能

# 或手动浏览
https://clawhub.com
```

## 相关概念

- [[Skills技能系统]]: DeerFlow 的技能机制
- [[Agent架构对比]]: 框架对比分析