# Core 核心概念总览

> AutoGen 的核心架构基于**事件驱动**和**发布/订阅**模式

---

## 🎯 核心概念

### 1. Agent (智能体)

Agent 是 AutoGen 的基本单元，负责接收消息、处理逻辑、发送响应。

```python
from autogen_core import RoutedAgent, message_handler, MessageContext

class MyAgent(RoutedAgent):
    @message_handler
    async def on_message(self, message: MyType, ctx: MessageContext):
        # 处理消息
        return response
```

**关键文件**：
- [_agent.py](01-Agent 和 Runtime.md) - Agent 协议定义
- [_base_agent.py](01-Agent 和 Runtime.md) - 基类实现
- [_routed_agent.py](01-Agent 和 Runtime.md) - 路由 Agent

---

### 2. Runtime (运行时)

Runtime 负责消息的传递和调度。

**核心接口**：
```python
# 发送消息（RPC，期待响应）
await runtime.send_message(message, recipient=agent_id)

# 发布消息（广播，不期待响应）
await runtime.publish_message(message, topic_id=topic_id)

# 注册 Agent
await MyAgent.register(runtime, "name", factory)
```

**关键文件**：[_agent_runtime.py](01-Agent 和 Runtime.md)

---

### 3. Topic 和 Subscription (主题和订阅)

Topic 是消息的逻辑通道，Subscription 决定哪些 Agent 接收哪些消息。

```python
# 定义主题
topic_id = TopicId(type="news.tech", source="default")

# 添加订阅
await runtime.add_subscription(
    TypeSubscription(topic_type="news.tech", agent_type="tech_subscriber")
)

# 发布消息
await runtime.publish_message(message, topic_id=topic_id)
```

**详细**：[03-订阅和主题](03-订阅和主题.md)

---

### 4. Message Routing (消息路由)

通过 `@message_handler` 装饰器实现条件路由。

```python
class PriorityAgent(RoutedAgent):
    @message_handler(match=lambda msg, ctx: msg.priority == "high")
    async def on_high_priority(self, message: TaskMessage, ctx):
        # 只处理高优先级消息
        pass

    @message_handler(match=lambda msg, ctx: msg.priority == "low")
    async def on_low_priority(self, message: TaskMessage, ctx):
        # 只处理低优先级消息
        pass
```

**详细**：[04-路由和匹配](04-路由和匹配.md)

---

## 📊 架构图

```
┌──────────────────────────────────────────────────┐
│                  Agent Runtime                    │
│                                                   │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │ Agent A │ ←→ │ Agent B │ ←→ │ Agent C │      │
│  └────┬────┘    └────┬────┘    └────┬────┘      │
│       │             │              │             │
│       └─────────────┴──────────────┘             │
│                     ↓                            │
│            ┌────────────────┐                    │
│            │  Subscriptions │                    │
│            └────────────────┘                    │
└──────────────────────────────────────────────────┘
         ↑                    ↑
    send_message      publish_message
    (RPC)               (Broadcast)
```

---

## 🔑 关键设计模式

### 1. 工厂模式
Agent 通过工厂函数创建，而不是直接实例化。

```python
await MyAgent.register(runtime, "name", lambda: MyAgent("description"))
```

### 2. 依赖注入
通过 `AgentInstantiationContext` 注入 Runtime 和 AgentId。

### 3. 装饰器模式
使用 `@message_handler`、`@event`、`@rpc` 装饰器声明消息处理器。

---

## 📝 实践代码

查看以下示例代码：
- [01-HelloAgent](01-HelloAgent.md) - 最简单的 Agent 示例
- [02-发布订阅](02-发布订阅.md) - 发布/订阅模式
- [03-消息路由](03-消息路由.md) - 条件路由
- [04-多 Agent 协作](04-多 Agent 协作.md) - 多 Agent 协作

---

## 🔗 相关链接

- [02-消息传递机制](02-消息传递机制.md) - 深入了解消息传递
- [03-订阅和主题](03-订阅和主题.md) - 深入了解订阅机制
- [01-Agent 和 Runtime](01-Agent 和 Runtime.md) - Agent 和 Runtime 详解
