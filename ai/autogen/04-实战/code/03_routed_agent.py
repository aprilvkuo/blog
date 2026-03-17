"""
消息路由示例 - 演示条件匹配和路由

这个示例展示：
1. 使用 match 参数进行条件路由
2. 优先级消息处理
3. 显式 @rpc 和 @event 装饰器
"""

from dataclasses import dataclass
from autogen_core import (
    RoutedAgent,
    SingleThreadedAgentRuntime,
    MessageContext,
    message_handler,
    event,
    rpc,
    TopicId,
    TypeSubscription,
    AgentId,
)


# 1. 定义消息类型
@dataclass
class TaskMessage:
    """任务消息"""
    priority: str  # "critical", "high", "normal", "low"
    content: str


# 2. 优先级 Agent - 根据优先级路由
class PriorityAgent(RoutedAgent):
    """根据优先级处理消息的 Agent"""

    def __init__(self, description: str):
        super().__init__(description)
        self.critical_count = 0
        self.high_count = 0
        self.normal_count = 0
        self.low_count = 0

    @message_handler(match=lambda msg, ctx: msg.priority == "critical")
    async def on_critical(self, message: TaskMessage, ctx: MessageContext) -> None:
        """处理紧急任务"""
        self.critical_count += 1
        print(f"[紧急] 处理任务：{message.content}")

    @message_handler(match=lambda msg, ctx: msg.priority == "high")
    async def on_high_priority(self, message: TaskMessage, ctx: MessageContext) -> None:
        """处理高优先级任务"""
        self.high_count += 1
        print(f"[高优先级] 处理任务：{message.content}")

    @message_handler(match=lambda msg, ctx: msg.priority == "normal")
    async def on_normal(self, message: TaskMessage, ctx: MessageContext) -> None:
        """处理普通任务"""
        self.normal_count += 1
        print(f"[普通] 处理任务：{message.content}")

    @message_handler(match=lambda msg, ctx: msg.priority == "low")
    async def on_low_priority(self, message: TaskMessage, ctx: MessageContext) -> None:
        """处理低优先级任务"""
        self.low_count += 1
        print(f"[低优先级] 处理任务：{message.content}")


# 3. 显式路由 Agent - 使用 @rpc 和 @event
class ExplicitRouteAgent(RoutedAgent):
    """显式声明路由类型的 Agent"""

    def __init__(self, description: str):
        super().__init__(description)
        self.rpc_count = 0
        self.event_count = 0

    @rpc  # 显式声明为 RPC 消息
    async def on_rpc_task(self, message: TaskMessage, ctx: MessageContext) -> str:
        """RPC 消息处理器"""
        self.rpc_count += 1
        return f"RPC 处理完成：{message.content}"

    @event  # 显式声明为事件消息
    async def on_event_task(self, message: TaskMessage, ctx: MessageContext) -> None:
        """事件消息处理器"""
        self.event_count += 1
        print(f"[事件] 处理：{message.content}")


# 4. 主函数
async def demo_priority_agent():
    print("=== 演示 1: 条件路由 ===")
    runtime = SingleThreadedAgentRuntime()

    await PriorityAgent.register(
        runtime,
        "priority_agent",
        lambda: PriorityAgent("优先级 Agent")
    )
    await runtime.add_subscription(TypeSubscription("tasks", "priority_agent"))

    runtime.start()

    agent_id = AgentId("priority_agent", "default")

    # 发送不同优先级的消息
    await runtime.send_message(
        TaskMessage(priority="critical", content="紧急任务！系统故障"),
        recipient=agent_id
    )
    await runtime.send_message(
        TaskMessage(priority="high", content="高优先级任务：代码审查"),
        recipient=agent_id
    )
    await runtime.send_message(
        TaskMessage(priority="normal", content="普通任务：编写文档"),
        recipient=agent_id
    )
    await runtime.send_message(
        TaskMessage(priority="low", content="低优先级任务：整理文件"),
        recipient=agent_id
    )

    await runtime.stop_when_idle()

    agent = await runtime.try_get_underlying_agent_instance(
        agent_id,
        type=PriorityAgent
    )
    print(f"\n统计：紧急={agent.critical_count}, 高={agent.high_count}, "
          f"普通={agent.normal_count}, 低={agent.low_count}\n")


async def demo_explicit_routing():
    print("=== 演示 2: 显式路由 ===")
    runtime = SingleThreadedAgentRuntime()

    await ExplicitRouteAgent.register(
        runtime,
        "route_agent",
        lambda: ExplicitRouteAgent("路由 Agent")
    )
    await runtime.add_subscription(TypeSubscription("explicit", "route_agent"))

    agent_id = AgentId("route_agent", "default")

    runtime.start()

    # RPC 消息（期待响应）
    print("发送 RPC 消息...")
    response = await runtime.send_message(
        TaskMessage(priority="normal", content="RPC 任务"),
        recipient=agent_id
    )
    print(f"RPC 响应：{response}")

    # 发布事件消息（不期待响应）
    print("发送事件消息...")
    await runtime.publish_message(
        TaskMessage(priority="normal", content="事件消息 1"),
        topic_id=TopicId("explicit", "default")
    )
    await runtime.publish_message(
        TaskMessage(priority="normal", content="事件消息 2"),
        topic_id=TopicId("explicit", "default")
    )

    await runtime.stop_when_idle()

    agent = await runtime.try_get_underlying_agent_instance(
        agent_id,
        type=ExplicitRouteAgent
    )
    print(f"\n统计：RPC={agent.rpc_count}, 事件={agent.event_count}\n")


async def main():
    await demo_priority_agent()
    await demo_explicit_routing()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
