---
title: Placeholder 机制
type: concept
---

# Placeholder 机制

> **定义**: 非阻塞占位符，Agent 调用立即返回 Placeholder，需要时才获取实际结果，避免等待阻塞主流程。

## 核心要点

- **立即返回**: `agent.reply(msg)` 返回 Placeholder，不等待 LLM
- **延迟获取**: `placeholder.get()` 时才阻塞等待结果
- **流水线优化**: 多 Agent 并行执行，主流程不卡顿
- **容错设计**: Placeholder 支持超时、异常处理

## 示例

```python
# 传统阻塞方式
result1 = agent1.reply(msg)  # 等待 LLM 完成 (5秒)
result2 = agent2.reply(result1)  # 再等待 (5秒)
# 总耗时: 10秒

# Placeholder 非阻塞
p1 = agent1.reply(msg)  # 立即返回
p2 = agent2.reply(p1)   # 立即返回（p1 是 Placeholder）
# 后续任务继续执行...

result = p2.get()  # 需要时才获取（并行等待）
# 总耗时: ~5秒
```

## 相关论文

- [[AgentScope]]: 核心机制，支持百万级并行

## 相关概念

- [[Actor 模型]]: Placeholder 是 Actor 的通信桥梁
- [[Event Stream]]: 不同设计哲学（序列化 vs 并行）

---

## 与 Event Stream 的对比

| 维度 | Event Stream | Placeholder |
|------|-------------|-------------|
| 设计哲学 | 序列化、可回放 | 并行、非阻塞 |
| 适用场景 | 单 Agent 复杂任务 | 多 Agent 并行任务 |
| 时序保证 | 严格 | 可能乱序（需处理） |
| 调试难度 | 易（有序记录） | 需同步点 |

**何时选择**:
- 需要**精确复现**任务流程 → Event Stream
- 需要**大规模并行**执行 → Placeholder