"""
发布/订阅模式示例 - 演示广播消息的使用

这个示例展示：
1. 如何发布广播消息
2. 多个订阅者如何接收消息
3. Topic 类型匹配规则
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
    DefaultTopicId,
)


# 1. 定义消息类型
@dataclass
class NewsMessage:
    """新闻消息"""
    category: str
    headline: str


# 2. 创建订阅者 Agent
class NewsSubscriberAgent(RoutedAgent):
    """新闻订阅者 Agent"""

    def __init__(self, description: str, subscribed_categories: list[str]):
        super().__init__(description)
        self.subscribed_categories = subscribed_categories
        self.received_news = []

    @message_handler
    async def on_news(self, message: NewsMessage, ctx: MessageContext) -> None:
        """处理新闻消息（广播消息，不返回响应）"""
        if message.category in self.subscribed_categories:
            self.received_news.append(message)
            print(f"[{self.id}] 收到新闻 [{message.category}]: {message.headline}")


# 3. 主函数
async def main():
    runtime = SingleThreadedAgentRuntime()

    # 注册多个订阅者
    await NewsSubscriberAgent.register(
        runtime,
        "tech_subscriber",
        lambda: NewsSubscriberAgent("科技新闻订阅者", ["tech", "ai", "science"])
    )

    await NewsSubscriberAgent.register(
        runtime,
        "finance_subscriber",
        lambda: NewsSubscriberAgent("财经新闻订阅者", ["finance", "stock", "crypto"])
    )

    await NewsSubscriberAgent.register(
        runtime,
        "sports_subscriber",
        lambda: NewsSubscriberAgent("体育新闻订阅者", ["sports", "football", "basketball"])
    )

    # 添加订阅 - 订阅不同类别的新闻
    await runtime.add_subscription(TypeSubscription("news.tech", "tech_subscriber"))
    await runtime.add_subscription(TypeSubscription("news.finance", "finance_subscriber"))
    await runtime.add_subscription(TypeSubscription("news.sports", "sports_subscriber"))

    runtime.start()

    print("=== 发布科技新闻 ===")
    # 发布科技新闻 - 只有 tech_subscriber 会收到
    await runtime.publish_message(
        NewsMessage(category="tech", headline="AI 新突破！"),
        topic_id=TopicId("news.tech", "default")
    )

    await runtime.publish_message(
        NewsMessage(category="ai", headline="大模型性能提升"),
        topic_id=TopicId("news.tech", "default")  # 使用相同的 topic 类型
    )

    print("\n=== 发布财经新闻 ===")
    # 发布财经新闻 - 只有 finance_subscriber 会收到
    await runtime.publish_message(
        NewsMessage(category="finance", headline="股市创新高"),
        topic_id=TopicId("news.finance", "default")
    )

    print("\n=== 发布体育新闻 ===")
    # 发布体育新闻 - 只有 sports_subscriber 会收到
    await runtime.publish_message(
        NewsMessage(category="sports", headline="足球比赛精彩瞬间"),
        topic_id=TopicId("news.sports", "default")
    )

    # 等待处理完成
    await runtime.stop_when_idle()

    # 检查收到的新闻
    print("\n=== 统计 ===")
    for subscriber_type in ["tech_subscriber", "finance_subscriber", "sports_subscriber"]:
        agent = await runtime.try_get_underlying_agent_instance(
            AgentId(subscriber_type, "default"),
            type=NewsSubscriberAgent
        )
        print(f"{subscriber_type}: 收到 {len(agent.received_news)} 条新闻")
        for news in agent.received_news:
            print(f"  - [{news.category}] {news.headline}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
