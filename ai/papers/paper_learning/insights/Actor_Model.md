---
title: Actor 模型
type: concept
---

# Actor 模型

> **定义**: 并发计算模型，每个 Actor 是独立执行单元，通过消息传递通信，无需共享状态，天然适合多智能体系统。

## 核心要点

- **独立进程**: 每个 Agent 可运行在独立 Actor 进程
- **消息传递**: Actor 间只通过消息通信，无锁竞争
- **原子化**: Agent 的 `reply()` 是原子操作，不会被中断
- **分布式**: 自动分配到多设备，透明扩展

## 示例

```python
# AgentScope 的 Actor 分布式
@to_dist  # 一行代码启用分布式
class MyAgent(Agent):
    def reply(self, msg):
        return self.llm.generate(msg)

# 一对一模式：每个 Agent 独立进程
agent1 = MyAgent().to_dist()  # Actor 1
agent2 = MyAgent().to_dist()  # Actor 2

# 多对一模式：多 Agent 共享进程（节省资源）
agents = [SimpleAgent() for _ in range(10000)]
# 自动打包到少数 Actor
```

## 相关论文

- [[AgentScope]]: 核心架构，实现百万级智能体并行
- [[OpenDevin]]: Docker Runtime 类似隔离思想（进程级）

## 相关概念

- [[Placeholder]]: Actor 模型的非阻塞机制
- [[环境抽象]]: 将环境也视为 Actor

---

## 为什么重要

| 方法 | 100万智能体 | 问题 |
|------|------------|------|
| 串行 | ~12 天 | 无法实用 |
| Python 异步 | 8.6 小时 | 锁竞争、GIL 限制 |
| **Actor 分布式** | **40 秒** | 无锁、进程隔离 |

**核心洞察**: Agent 交互天然是原子化的——一个 Agent 接收消息、思考、回复，这整个过程不需要被中断。Actor 模型恰好匹配这个特征。