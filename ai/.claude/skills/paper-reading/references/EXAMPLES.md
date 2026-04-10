# 示例笔记

完整的论文笔记示例，展示最佳实践。

---

## 大白话版本示例

参见现有笔记：`papers/paper_learning/notes/OpenDevin_大白话.md`

关键要素：

```markdown
> **一句话**: 让 AI 像程序员一样干活

## 这项目是干嘛的？

想象你有一个"虚拟程序员"，它能：
- 写代码、改 bug
- 运行命令、查文档
- 打开浏览器搜索解决方案

这就是 OpenHands —— 一个让 AI 真正"动手干活"的平台。

## 为什么需要它？

| 现有方案 | 缺陷 |
|----------|------|
| ChatGPT | 只能聊天，不能执行代码 |
| AutoGPT | 功能单一，没有浏览器 |

**痛点**: AI 只能"嘴上说"，不能"手上做"

## 怎么工作的？

```
用户 ──> Agent ──> Docker沙箱 ──> 执行代码
         │              │
         └─ 浏览器 ────┘
```

| 组件 | 作用 |
|------|------|
| **Agent** | 大脑，做决策 |
| **Docker** | 手脚，执行代码 |
| **浏览器** | 眼睛，查资料 |

## 效果如何？

| 场景 | 效果 |
|------|------|
| GitHub issue 修复 | 26% 成功率 |
| 网页操作 | 15.5% 成功率 |

## 优缺点

✅ 开源免费 | ❌ 成功率还不够高
✅ 安全沙箱 | ❌ Token 消耗大
```

---

## 深入版本示例

参见现有笔记：`papers/paper_learning/notes/OpenDevin_深入.md`

关键要素：

```markdown
## What - 核心定义

OpenHands 是一个开源 AI 智能体平台，采用 Event Stream 架构，
让 Agent 通过代码、命令行、浏览器与环境交互。

### 技术架构

```
┌─────────────────────────────────────────┐
│              User Interface              │
└─────────────────────┬───────────────────┘
                      │
┌─────────────────────▼───────────────────┐
│             Event Stream                 │
│  [Action] → [Observation] → [Action]    │
└─────────────────────┬───────────────────┘
                      │
┌─────────────────────▼───────────────────┐
│              Agent Layer                 │
│  CodeActAgent | BrowsingAgent | ...     │
└─────────────────────┬───────────────────┘
                      │
┌─────────────────────▼───────────────────┐
│            Docker Runtime                │
│  Terminal | IPython | Browser            │
└─────────────────────────────────────────┘
```

### 核心组件

| 组件 | 功能 | 设计理由 |
|------|------|----------|
| **Event Stream** | 时间序列化 Action-Observation | 支持回放、中断、恢复 |
| **Docker Runtime** | 隔离执行环境 | AI 代码不破坏宿主 |

## Who - 作者与生态

| 维度 | 信息 |
|------|------|
| **作者** | UIUC/CMU + 社区 188+ 贡献者 |
| **用户** | 研究者、开发者、企业 |
| **生态位** | 对比 SWE-Agent（专用）、AutoGen（对话） |

## When - 技术演进

```
2024.03 ──── CodeAct 论文（前身）
2024.07 ──── OpenDevin 发布
2024.09 ──── 改名 OpenHands
2025.05 ──── ICLR 2025 发表
```

## Why - 研究缺口

| 缺口 | 本文方案 |
|------|----------|
| 功能单一 | 集成代码+命令行+浏览器 |
| 安全风险 | Docker 沙箱隔离 |
| 评估分散 | 整合 15 个基准测试 |

**核心贡献**: 首个通用 AI 软件工程师平台

## How - 技术实现

### 关键技术：Event Stream

```python
class Event:
    action: Action      # Agent 发出的动作
    observation: Observation  # 环境返回的结果
    timestamp: datetime  # 时间戳
```

**设计理念**: 解耦 Agent 与执行，支持异步

### 评估结果

| Agent | SWE-Bench | WebArena |
|-------|-----------|----------|
| SWE-Agent | 18.0% | - |
| **CodeActAgent** | **26.0%** | **15.5%** |

## TODO - 深度思考

### 理解检验

- [ ] **Q1**: 为什么选择"代码执行"而非"工具调用"？
- [ ] **Q2**: Event Stream 与消息队列的区别？

### 批判性思考

- 26% 成功率是否足够实用？

### 实践任务

| 难度 | 任务 |
|------|------|
| Level 1 | 本地运行，修复简单 bug |
| Level 2 | 实现 Micro Agent |
| Level 3 | 添加新 Skill |

---

## 理解程度: ████████░░ 80%
```

---

## 原子概念示例

```markdown
---
title: Event Stream
type: concept
---

# Event Stream

> **定义**: 时序化的 Action-Observation 记录，是 Agent 系统的核心数据结构。

## 核心要点

- Action = Agent 的输出（命令、代码、消息）
- Observation = 环境的反馈（结果、错误、状态）
- 时间戳记录顺序，支持回放和恢复

## 示例

```python
events = [
    Event(action=CmdRunAction("ls"), observation=CmdOutput("file1.txt")),
    Event(action=MessageAction("查看文件"), observation=UserMessage("好的")),
]
```

## 相关论文

- [[OpenDevin]]: 核心架构
- [[AgentScope]]: 类似的消息机制

## 相关概念

- [[Action]]: Agent 的输出类型
- [[Observation]]: 环境的反馈类型
```