---
title: Super Agent Harness
type: concept
---

# Super Agent Harness

> **定义**: 不仅是"框架"（Framework），而是"框架 + 基础设施 + 工具"的开箱即用系统，"电池已安装"，Agent 可以直接开始工作。

## 核心要点

- **Framework vs Harness**：Framework 提供组件，Harness 提供完整运行环境
- **开箱即用**：沙箱、记忆、技能、工具链全部内置
- **基础设施**：执行环境、文件系统、持久化存储
- **可扩展**：仍支持定制和二次开发

## 类比

| 类型 | 类比 | 特点 |
|------|------|------|
| **Framework** | 乐高积木 | 有组件，需自己搭建 |
| **Harness** | 预组装机器人 | 组件已安装，可直接使用 |

## 对比表

| 维度 | Framework | Harness |
|------|-----------|---------|
| 执行环境 | 需自己搭建 | ✅ 内置沙箱 |
| 记忆系统 | 需自己实现 | ✅ 内置 Memory |
| 技能库 | 需自己定义 | ✅ 内置 Skills |
| 工具链 | 需自己集成 | ✅ 内置 Tools |
| 部署难度 | 高 | 低（开箱即用） |
| 定制灵活性 | 高 | 高（仍可定制） |

## 代表项目

| 项目 | 类型 | 说明 |
|------|------|------|
| LangChain | Framework | 组件超市，需自己拼 |
| LangGraph | Framework | 工作流编排引擎 |
| **DeerFlow 2.0** | **Harness** | 框架 + 基础设施 + 技能 |
| OpenHands | Harness（部分） | 有沙箱和工具，但无记忆和丰富技能 |

## 相关论文

- [[DeerFlow]]: 首次明确提出 "Super Agent Harness" 定位

## 相关概念

- [[Skills技能系统]]: Harness 的能力扩展机制
- [[Sandbox]]: Harness 的执行环境基础