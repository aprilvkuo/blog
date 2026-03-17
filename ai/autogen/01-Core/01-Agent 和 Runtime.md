# Agent 和 Runtime

> Agent 是智能体，Runtime 是运行环境

---

## 📖 概述

AutoGen Core 的核心是两个关键抽象：

1. **Agent** - 处理消息的智能体
2. **Runtime** - 消息传递的基础设施

---

## 1. Agent 基类

### RoutedAgent

```python
from autogen_core import RoutedAgent, message_handler, MessageContext

class MyAgent(RoutedAgent):
    def __init__(self, description: str):
        super().__init__(description)
        # 初始化逻辑

    @message_handler
    async def on_message(self, message: MessageType, ctx: MessageContext):
        # 处理消息
        return response
```

**关键属性**：
- `self.id` - AgentId，唯一标识
- `self.runtime` - 运行时引用
- `self.metadata` - 元数据

**关键方法**：
- `send_message()` - 发送 RPC 消息
- `publish_message()` - 发布广播消息
- `save_state()` / `load_state()` - 状态持久化

---

## 2. Runtime 协议

### AgentRuntime

```python
# 发送消息（期待响应）
response = await runtime.send_message(
    message,
    recipient=agent_id,
    sender=sender_id,  # 可选
    cancellation_token=token  # 可选
)

# 发布消息（不期待响应）
await runtime.publish_message(
    message,
    topic_id=topic_id,
    sender=sender_id  # 可选
)
```

### SingleThreadedAgentRuntime

单线程实现，适合本地开发和测试。

```python
runtime = SingleThreadedAgentRuntime()

# 注册 Agent
await MyAgent.register(runtime, "name", factory)

# 添加订阅
await runtime.add_subscription(subscription)

# 启动
runtime.start()

# 等待处理完成
await runtime.stop_when_idle()
```

---

## 3. Agent 生命周期

```
1. 创建工厂函数
       ↓
2. 注册到 Runtime
       ↓
3. 添加订阅 (Subscription)
       ↓
4. 启动 Runtime
       ↓
5. 接收和处理消息
       ↓
6. 停止 Runtime
```

---

## 4. 代码示例

### 简单的问候 Agent

```python
from dataclasses import dataclass
from autogen_core import (
    RoutedAgent, message_handler, MessageContext,
    SingleThreadedAgentRuntime, AgentId, TypeSubscription
)

@dataclass
class Greeting:
    content: str

class HelloAgent(RoutedAgent):
    @message_handler
    async def on_greeting(self, message: Greeting, ctx: MessageContext):
        print(f"收到：{message.content}")
        return Greeting(content="你好！")

async def main():
    runtime = SingleThreadedAgentRuntime()
    await HelloAgent.register(runtime, "hello", lambda: HelloAgent("问候 Agent"))
    await runtime.add_subscription(TypeSubscription("default", "hello"))

    runtime.start()
    response = await runtime.send_message(
        Greeting("你好"),
        recipient=AgentId("hello", "default")
    )
    await runtime.stop_when_idle()
    print(f"响应：{response.content}")
```

---

## 5. 关键点

### 消息处理上下文

`MessageContext` 包含：
- `cancellation_token` - 取消令牌
- `is_rpc` - 是否是 RPC 消息
- `sender` - 发送者 ID

### 类型安全

使用 `try_get_underlying_agent_instance` 获取 Agent 实例：

```python
agent = await runtime.try_get_underlying_agent_instance(
    agent_id,
    type=HelloAgent
)
print(f"消息计数：{agent.message_count}")
```

---

## 📝 练习

参考 [01-HelloAgent](01-HelloAgent.md) 示例代码进行实践。

---

## 🔗 相关链接

- [00-Core 核心概念总览](00-Core 核心概念总览.md)
- [02-消息传递机制](02-消息传递机制.md)
- [04-路由和匹配](04-路由和匹配.md)
