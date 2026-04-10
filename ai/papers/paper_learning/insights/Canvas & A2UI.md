---
title: Canvas & A2UI
type: concept
---

# Canvas & A2UI

> **定义**: OpenClaw 的实时可视化工作区，Agent 可以推送交互式 UI 元素到 Canvas。

## Canvas 架构

```
Agent (推理)
    │
    ▼ push UI elements
┌─────────────────────────────────┐
│           Canvas                 │
│   (macOS/iOS/Android/WebChat)   │
│                                 │
│  ┌─────┐ ┌─────┐ ┌─────────┐   │
│  │按钮│ │表单│ │  图表   │   │
│  └─────┘ └─────┘ └─────────┘   │
│                                 │
│  A2UI: Agent-to-UI Protocol    │
└─────────────────────────────────┘
    │
    ▼ user interaction
Agent (接收反馈)
```

## A2UI Protocol

- **Agent-to-UI**: Agent 推送 UI 元素
- **双向交互**: 用户点击 → Agent 响应
- **动态更新**: 实时刷新内容

## 支持元素

- 按钮、表单、图表
- 文本、图片、列表
- 自定义组件

## 与 DeerFlow 对比

| 维度 | OpenClaw Canvas | DeerFlow |
|------|-----------------|----------|
| **可视化** | ✅ 实时 Canvas | ❌ |
| **交互** | ✅ A2UI 双向 | ❌ |
| **平台** | macOS/iOS/Android/Web | CLI only |

## 使用场景

- 📊 数据可视化展示
- 📝 表单填写辅助
- 🎮 游戏式交互

## 相关概念

- [[Agent架构对比]]: 框架对比分析