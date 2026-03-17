# AutoGen 学习笔记

> 学习路径：Core 核心 → AgentChat 高层 → Ext 扩展 → 实战

---

## 📚 学习路径

### 1. [ Core 核心概念](01-Core 核心概念/00-Core 核心概念总览)
理解 AutoGen 的底层架构

- [01-Agent 和 Runtime](01-Core 核心概念/01-Agent 和 Runtime)
- [02-消息传递机制](01-Core 核心概念/02-消息传递机制)
- [03-订阅和主题](01-Core 核心概念/03-订阅和主题)
- [04-路由和匹配](01-Core 核心概念/04-路由和匹配)

### 2. [ AgentChat 高层 API](02-AgentChat 高层 API/00-AgentChat 总览)
掌握常用的多智能体模式

- [01-AssistantAgent](02-AgentChat 高层 API/01-AssistantAgent)
- [02-群聊模式](02-AgentChat 高层 API/02-群聊模式)
- [03-终止条件](02-AgentChat 高层 API/03-终止条件)

### 3. [ Ext 扩展机制](03-Ext 扩展机制/00-Ext 扩展机制总览)
学习如何集成新模型和工具

- [01-模型客户端](03-Ext 扩展机制/01-模型客户端)
- [02-工具和工作台](03-Ext 扩展机制/02-工具和工作台)
- [03-MCP 集成](03-Ext 扩展机制/03-MCP 集成)

### 4. [ 实战示例](04-实战示例/00-实战示例总览)
通过代码实践学习

- [01-HelloAgent](04-实战示例/01-HelloAgent)
- [02-发布订阅](04-实战示例/02-发布订阅)
- [03-消息路由](04-实战示例/03-消息路由)
- [04-多 Agent 协作](04-实战示例/04-多 Agent 协作)

---

## 🔧 环境设置

```bash
cd python
uv sync --all-extras
source .venv/bin/activate

# 运行检查
poe format
poe lint
poe test
```

---

## 📝 关键概念速查

| 概念 | 说明 | 文档 |
|------|------|------|
| Agent | 智能体基类 | [01-Core 核心概念/01-Agent 和 Runtime](01-Core 核心概念/01-Agent 和 Runtime) |
| Runtime | 消息运行时 | [01-Core 核心概念/01-Agent 和 Runtime](01-Core 核心概念/01-Agent 和 Runtime) |
| Topic | 消息主题 | [01-Core 核心概念/03-订阅和主题](01-Core 核心概念/03-订阅和主题) |
| Subscription | 订阅规则 | [01-Core 核心概念/03-订阅和主题](01-Core 核心概念/03-订阅和主题) |
| RPC 消息 | 期待响应的消息 | [01-Core 核心概念/02-消息传递机制](01-Core 核心概念/02-消息传递机制) |
| 事件消息 | 不期待响应的消息 | [01-Core 核心概念/02-消息传递机制](01-Core 核心概念/02-消息传递机制) |

---

## 📊 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    AutoGen 架构                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │           autogen-agentchat (高层 API)           │   │
│  │  AssistantAgent | GroupChat | Termination       │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │             autogen-core (核心层)                │   │
│  │  Agent | Runtime | Topic | Subscription | Tool  │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │             autogen-ext (扩展层)                 │   │
│  │  OpenAI | Anthropic | Ollama | MCP | CodeExec   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 学习目标检查清单

### Core 核心
- [ ] 理解 Agent 的生命周期
- [ ] 掌握消息传递机制（RPC vs 广播）
- [ ] 理解 Topic 和 Subscription 的关系
- [ ] 能够自定义消息路由规则

### AgentChat
- [ ] 能够创建 AssistantAgent
- [ ] 理解群聊模式（RoundRobin、Selector、Swarm）
- [ ] 能够设置终止条件
- [ ] 能够使用工具调用

### Ext 扩展
- [ ] 理解模型客户端接口
- [ ] 能够添加工具
- [ ] 理解 MCP 协议
- [ ] 能够集成第三方工具

### 实战示例
- [ ] 完成 HelloAgent 示例
- [ ] 完成发布订阅示例
- [ ] 完成消息路由示例
- [ ] 完成多 Agent 协作示例

---

## 📖 推荐学习顺序

1. 先看 [01-Core 核心概念/00-Core 核心概念总览](01-Core 核心概念/00-Core 核心概念总览)
2. 实践 [HelloAgent 示例](04-实战示例/01-HelloAgent)
3. 学习 [02-AgentChat 高层 API/00-AgentChat 总览](02-AgentChat 高层 API/00-AgentChat 总览)
4. 尝试 [04-实战示例/00-实战示例总览](04-实战示例/00-实战示例总览) 中的更多示例
5. 深入了解 [03-Ext 扩展机制/00-Ext 扩展机制总览](03-Ext 扩展机制/00-Ext 扩展机制总览)

---

## 🔗 外部资源

- [官方文档 (dev)](https://microsoft.github.io/autogen/dev/)
- [GitHub 仓库](https://github.com/microsoft/autogen)
- [Discord 社区](https://aka.ms/autogen-discord)
