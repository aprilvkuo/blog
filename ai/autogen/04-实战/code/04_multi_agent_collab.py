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
