---
title: Event Stream
type: concept
---

# Event Stream

> **定义**: 时序化的 Action-Observation 记录，是 Agent 系统的核心数据结构，解耦 Agent 逻辑与执行环境。

## 核心要点

- **Action** = Agent 的输出（命令、代码、消息、委托）
- **Observation** = 环境的反馈（结果、错误、状态）
- **时间戳** 记录顺序，支持回放、中断、恢复
- **解耦设计**：Agent 只需处理 state，不关心执行细节

## 示例

```python
# Event Stream 结构
events = [
    Event(action=CmdRunAction("ls"), observation=CmdOutput("file1.txt")),
    Event(action=MessageAction("查看文件"), observation=UserMessage("好的")),
]

# Agent 只需读取 state.history
class MyAgent(Agent):
    def step(self, state):
        history = state.history  # Event Stream
        action = self.llm.decide(history)
        return action
```

## 相关论文

- [[OpenDevin]]: 核心架构，Event Stream Layer 是系统中枢
- [[AgentScope]]: 类似的消息传递机制（Msg 对象）

## 相关概念

- [[Action]]: Agent 的输出类型
- [[Observation]]: 环境的反馈类型
- [[Placeholder]]: 非阻塞占位符（AgentScope 的变体）

---

## 为什么重要

| 维度 | 传统消息队列 | Event Stream |
|------|-------------|--------------|
| 时序保证 | 可能乱序 | 严格时间戳 |
| 回放能力 | 无 | 支持 |
| 中断恢复 | 无 | 支持 |
| Agent 解耦 | 需了解队列 API | 只读 state |

**设计理念**: Agent 不应关心"如何执行"，只关心"做什么"和"看到什么"。