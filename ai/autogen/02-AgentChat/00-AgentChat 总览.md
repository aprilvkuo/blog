# AgentChat 总览

> 高层 API，简化多智能体协作

---

## 📖 概述

`autogen-agentchat` 是基于 `autogen-core` 构建的高层 API，提供了更简单的接口来实现常见的多智能体模式。

---

## 核心组件

### 1. Agents (智能体)

| Agent | 用途 |
|-------|------|
| [01-AssistantAgent](01-AssistantAgent.md) | 通用助手，支持工具调用 |
| [UserProxyAgent](01-AssistantAgent.md) | 用户代理，需要人工输入 |
| `CodeExecutorAgent` | 代码执行代理 |

### 2. Teams (团队)

| 模式 | 类 | 说明 |
|------|-----|------|
| [ RoundRobinGroupChat](02-群聊模式 .md) | 轮询发言 |
| [ SelectorGroupChat](02-群聊模式 .md) | 动态选择下一个发言人 |
| [ SwarmGroupChat](02-群聊模式 .md) | 基于 handoff 的群体协作 |

### 3. Conditions (终止条件)

| 条件 | 说明 |
|------|------|
| `MaxMessageTermination` | 达到最大消息数 |
| `TextMentionTermination` | 包含特定文本 |
| `TimeoutTermination` | 超时终止 |

---

## 快速开始

### 单个 Agent

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

model = OpenAIChatCompletionClient(model="gpt-4")
agent = AssistantAgent("assistant", model_client=model)
result = await agent.run(task="说你好")
print(result.messages[-1].content)
```

### 多 Agent 轮询

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat

agent1 = AssistantAgent("agent1", model_client=model)
agent2 = AssistantAgent("agent2", model_client=model)
team = RoundRobinGroupChat([agent1, agent2], max_turns=5)
result = await team.run(task="讨论 AI 的未来")
```

---

## 消息类型

```python
from autogen_agentchat.messages import (
    TextMessage,           # 文本消息
    ToolCallRequestEvent,  # 工具调用请求
    ToolCallExecutionEvent,# 工具调用执行
    HandoffMessage,        # 交接消息
)
```

---

## 流式处理

```python
# 流式运行
async for message in agent.run_stream(task="任务"):
    print(message)
```

---

## 与 Core 的关系

```
AgentChat (高层 API)
    ↓
Core (底层实现)
    ↓
Ext (扩展实现)
```

---

## 📝 下一步

- [01-AssistantAgent](01-AssistantAgent.md) - 深入学习 AssistantAgent
- [02-群聊模式](02-群聊模式.md) - 学习多 Agent 协作
- [03-终止条件](03-终止条件.md) - 学习如何控制流程

---

## 🔗 相关链接

- [../01-Core 核心概念/00-Core 核心概念总览](../01-Core 核心概念/00-Core 核心概念总览.md)
- [../03-Ext 扩展机制/01-模型客户端](../03-Ext 扩展机制/01-模型客户端.md)
