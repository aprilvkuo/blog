# 01-HelloAgent 实践

> 你的第一个 AutoGen Agent

---

## 🎯 学习目标

- 理解 Agent 的基本结构
- 掌握 Runtime 的使用方法
- 理解消息的发送和接收

---

## 📝 代码实现

创建文件 `learning_samples/01_hello_agent.py`：

```python
"""
HelloAgent 示例 - 演示最基本的 Agent 使用

这个示例展示：
1. 如何定义消息类型
2. 如何创建 Agent
3. 如何注册到 Runtime
4. 如何发送和接收消息
"""

from dataclasses import dataclass
from autogen_core import (
    RoutedAgent,
    SingleThreadedAgentRuntime,
    MessageContext,
    message_handler,
    TopicId,
    TypeSubscription,
    AgentId,
)


# 1. 定义消息类型
@dataclass
class GreetingMessage:
    """问候消息"""
    content: str
    sender: str


@dataclass
class ResponseMessage:
    """响应消息"""
    content: str
    responder: str


# 2. 创建 Agent
class HelloAgent(RoutedAgent):
    """一个简单的 Agent，收到问候会回复"""

    def __init__(self, description: str):
        super().__init__(description)
        self.message_count = 0

    @message_handler
    async def on_greeting(self, message: GreetingMessage, ctx: MessageContext) -> ResponseMessage:
        """处理问候消息"""
        self.message_count += 1
        print(f"[{self.id}] 收到来自 {message.sender} 的消息：{message.content}")

        # 返回响应
        return ResponseMessage(
            content=f"你好，{message.sender}！我是 {self.id.type}，这是我的第 {self.message_count} 条消息",
            responder=self.id.type
        )


# 3. 主函数
async def main():
    # 创建运行时
    runtime = SingleThreadedAgentRuntime()

    # 注册 Agent 工厂
    await HelloAgent.register(
        runtime,
        "hello_agent",
        lambda: HelloAgent("一个问候 Agent")
    )

    # 添加订阅
    await runtime.add_subscription(
        TypeSubscription("greetings", "hello_agent")
    )

    # 启动运行时
    runtime.start()

    # 发送 RPC 消息（期待响应）
    agent_id = AgentId("hello_agent", "default")
    response = await runtime.send_message(
        GreetingMessage(content="你好！", sender="User"),
        recipient=agent_id
    )
    print(f"响应：{response.content}")

    # 再次发送消息
    response2 = await runtime.send_message(
        GreetingMessage(content="再问一次", sender="User"),
        recipient=agent_id
    )
    print(f"响应 2: {response2.content}")

    # 等待所有消息处理完成
    await runtime.stop_when_idle()

    # 获取 Agent 实例并检查状态
    agent = await runtime.try_get_underlying_agent_instance(
        agent_id,
        type=HelloAgent
    )
    print(f"Agent 总共处理了 {agent.message_count} 条消息")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 🔍 关键概念解析

### 1. 消息类型定义

使用 `@dataclass` 定义消息类型：

```python
@dataclass
class GreetingMessage:
    content: str
    sender: str
```

### 2. Agent 定义

继承 `RoutedAgent` 并使用 `@message_handler` 装饰器：

```python
class HelloAgent(RoutedAgent):
    @message_handler
    async def on_greeting(self, message: GreetingMessage, ctx: MessageContext):
        # 处理逻辑
        return ResponseMessage(...)
```

### 3. 注册 Agent

```python
await HelloAgent.register(
    runtime,
    "hello_agent",  # 类型名称
    lambda: HelloAgent("description")  # 工厂函数
)
```

### 4. 添加订阅

```python
await runtime.add_subscription(
    TypeSubscription(
        topic_type="greetings",      # 主题类型
        agent_type="hello_agent"     # Agent 类型
    )
)
```

### 5. 发送消息

```python
# RPC 消息（期待响应）
response = await runtime.send_message(
    message,
    recipient=agent_id
)
```

---

## 🏃 运行方法

```bash
cd /path/to/autogen/python
source .venv/bin/activate

# 运行示例
python learning_samples/01_hello_agent.py
```

---

## 📊 预期输出

```
[hello_agent/default] 收到来自 User 的消息：你好！
响应：你好，User！我是 hello_agent，这是我的第 1 条消息
[hello_agent/default] 收到来自 User 的消息：再问一次
响应 2: 你好，User！我是 hello_agent，这是我的第 2 条消息
Agent 总共处理了 2 条消息
```

---

## 💡 练习建议

1. **修改 Agent 的响应内容**：让它返回不同的消息
2. **添加新的消息类型**：如 `FarewellMessage`
3. **添加计数器**：统计收到的消息类型
4. **尝试广播消息**：使用 `publish_message`

---

## 🔗 相关链接

- [00-Core 核心概念总览](00-Core 核心概念总览.md)
- [01-Agent 和 Runtime](01-Agent 和 Runtime.md)
- [02-发布订阅](02-发布订阅.md) - 下一个示例
