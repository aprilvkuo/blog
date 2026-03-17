# 04-多 Agent 协作实践

> 实现多个 Agent 之间的消息传递和协作

---

## 🎯 学习目标

- 理解多 Agent 协作的基本模式
- 掌握主持人 - 参与者模式
- 实现群聊消息流

---

## 📝 代码实现

创建文件 `learning_samples/04_multi_agent_collab.py`：

```python
"""
多 Agent 协作示例 - 演示主持人 - 参与者模式

这个示例展示：
1. 多个 Agent 之间的消息传递
2. 主持人控制讨论流程
3. 轮流发言机制
"""

from dataclasses import dataclass
from typing import List
from autogen_core import (
    RoutedAgent,
    SingleThreadedAgentRuntime,
    MessageContext,
    message_handler,
    TopicId,
    TypeSubscription,
    AgentId,
    DefaultTopicId,
)


# 1. 定义消息类型
@dataclass
class ChatMessage:
    """聊天消息"""
    content: str
    sender: str
    turn: int  # 轮次


# 2. 参与者 Agent
class SpeakerAgent(RoutedAgent):
    """参与者 Agent，收到消息后会发言"""

    def __init__(self, description: str, topic: str):
        super().__init__(description)
        self.topic = topic
        self.messages_sent = 0
        self.messages_received = 0

    @message_handler
    async def on_message(self, message: ChatMessage, ctx: MessageContext) -> None:
        """收到消息后发言"""
        self.messages_received += 1
        print(f"[{self.id}] 收到来自 {message.sender} 的消息：{message.content}")

        # 生成响应
        self.messages_sent += 1
        response = ChatMessage(
            content=f"我是 {self.id.type}，我同意你的观点。第 {message.turn} 轮",
            sender=self.id.type,
            turn=message.turn + 1
        )

        # 发布到群聊主题，让其他 Agent 收到
        await self.publish_message(
            response,
            topic_id=DefaultTopicId(self.topic)
        )


# 3. 主持人 Agent
class ModeratorAgent(RoutedAgent):
    """主持人 Agent，控制讨论流程"""

    def __init__(self, description: str, topic: str, participants: List[str]):
        super().__init__(description)
        self.topic = topic
        self.participants = participants
        self.current_turn = 0
        self.max_turns = 3  # 每人最多发言 3 次

    @message_handler
    async def on_start(self, message: ChatMessage, ctx: MessageContext) -> None:
        """开始讨论"""
        print(f"[主持人] 开始讨论：{message.content}")
        await self._next_turn(message.content)

    @message_handler
    async def on_response(self, message: ChatMessage, ctx: MessageContext) -> None:
        """收到响应后继续"""
        print(f"[主持人] 收到 {message.sender} 的发言：{message.content}")

        # 检查是否达到最大轮次
        if message.turn >= self.max_turns * len(self.participants):
            print(f"[主持人] 讨论结束，共 {self.current_turn} 轮")
            return

        await self._next_turn(message.content)

    async def _next_turn(self, context: str):
        """轮到下一个参与者发言"""
        if self.current_turn >= self.max_turns:
            print("[主持人] 已达到最大轮次限制")
            return

        # 计算当前应该是哪个参与者发言
        speaker_index = self.current_turn % len(self.participants)
        speaker = self.participants[speaker_index]
        speaker_id = AgentId(speaker, "default")

        print(f"[主持人] 请 {speaker} 发言 (第 {self.current_turn + 1} 轮)")
        self.current_turn += 1

        # 发送消息给下一个参与者
        await self.send_message(
            ChatMessage(
                content=context,
                sender="moderator",
                turn=self.current_turn
            ),
            recipient=speaker_id
        )


# 4. 主函数
async def main():
    topic = "discussion"
    participants = ["speaker1", "speaker2", "speaker3"]

    runtime = SingleThreadedAgentRuntime()

    # 注册主持人
    await ModeratorAgent.register(
        runtime,
        "moderator",
        lambda: ModeratorAgent("主持人", topic, participants)
    )

    # 注册发言者
    for i, participant in enumerate(participants):
        await SpeakerAgent.register(
            runtime,
            participant,
            lambda p=participant, idx=i: SpeakerAgent(f"{p}的描述", topic)
        )

    # 添加订阅
    await runtime.add_subscription(TypeSubscription(topic, "moderator"))
    for participant in participants:
        await runtime.add_subscription(TypeSubscription(topic, participant))

    runtime.start()

    # 开始讨论
    print("=== 开始多 Agent 协作 ===\n")
    await runtime.publish_message(
        ChatMessage(
            content="今天我们讨论 AI 的未来发展",
            sender="user",
            turn=0
        ),
        topic_id=DefaultTopicId(topic)
    )

    # 等待处理完成
    await runtime.stop_when_idle()

    # 统计
    print("\n=== 统计 ===")
    moderator = await runtime.try_get_underlying_agent_instance(
        AgentId("moderator", "default"),
        type=ModeratorAgent
    )
    print(f"主持人组织了 {moderator.current_turn} 轮发言")

    for participant in participants:
        agent = await runtime.try_get_underlying_agent_instance(
            AgentId(participant, "default"),
            type=SpeakerAgent
        )
        print(f"{participant}: 发言 {agent.messages_sent} 次，收到 {agent.messages_received} 条消息")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 🔍 关键概念解析

### 1. 主持人 - 参与者模式

```
                    ┌─────────────┐
                    │  Moderator  │
                    │  (主持人)    │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ↓                 ↓                 ↓
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Speaker1 │     │ Speaker2 │     │ Speaker3 │
   └──────────┘     └──────────┘     └──────────┘
```

### 2. 消息流

```
1. User → Moderator: 开始话题
2. Moderator → Speaker1: 请发言
3. Speaker1 → Moderator: 发言内容
4. Moderator → Speaker2: 请发言
5. Speaker2 → Moderator: 发言内容
...
```

### 3. 轮流发言逻辑

```python
# 计算当前应该是哪个参与者发言
speaker_index = self.current_turn % len(self.participants)
speaker = self.participants[speaker_index]
```

---

## 🏃 运行方法

```bash
cd /path/to/autogen/python
source .venv/bin/activate

python learning_samples/04_multi_agent_collab.py
```

---

## 📊 预期输出

```
=== 开始多 Agent 协作 ===

[主持人] 开始讨论：今天我们讨论 AI 的未来发展
[主持人] 请 speaker1 发言 (第 1 轮)
[speaker1/default] 收到来自 moderator 的消息：今天我们讨论 AI 的未来发展
[speaker1/default] 发布：我是 speaker1，我同意你的观点。第 1 轮
[主持人] 收到 speaker1 的发言：我是 speaker1，我同意你的观点。第 1 轮
[主持人] 请 speaker2 发言 (第 2 轮)
[speaker2/default] 收到来自 moderator 的消息：今天我们讨论 AI 的未来发展
[speaker2/default] 发布：我是 speaker2，我同意你的观点。第 2 轮
...

=== 统计 ===
主持人组织了 9 轮发言
speaker1: 发言 3 次，收到 3 条消息
speaker2: 发言 3 次，收到 3 条消息
speaker3: 发言 3 次，收到 3 条消息
```

---

## 💡 练习建议

1. **修改发言顺序**：让主持人根据特定规则选择下一个发言人
2. **添加终止条件**：当某个条件满足时提前结束讨论
3. **实现话题转换**：支持在讨论中切换到新话题
4. **添加 Observer**：添加只观察不发言的 Agent

---

## 🔗 相关链接

- [03-消息路由](03-消息路由) - 上一个示例
- [../02-AgentChat 高层 API/02-群聊模式](../02-AgentChat 高层 API/02-群聊模式) - AgentChat 的群聊实现
- [02-消息传递机制](02-消息传递机制) - 消息传递理论

---

## 🎓 进阶挑战

尝试实现以下功能：

1. **自由讨论模式**：参与者可以主动发言，不需要主持人邀请
2. **投票机制**：参与者可以对议题进行投票
3. **角色分工**：不同参与者扮演不同角色（如正方、反方）
