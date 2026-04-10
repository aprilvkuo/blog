---
title: DelegateAction
type: concept
---

# DelegateAction

> **定义**: Agent 间任务委托机制，通用 Agent 将子任务委托给专家 Agent，实现专业化分工协作。

## 核心要点

- **主 Agent 决策**: 分析任务，决定自己处理还是委托
- **专家 Agent 执行**: 专注特定领域（搜索、编码、浏览）
- **委托协议**: `AgentDelegateAction(agent, inputs)` 指定目标和参数
- **结果返回**: 专家 Agent 完成后，结果回到主 Agent

## 示例

```python
# OpenDevin 的委托机制
class CodeActAgent(Agent):
    def step(self, state):
        task = state.task

        if need_browsing(task):
            # 委托给 BrowsingAgent
            return AgentDelegateAction(
                agent="BrowsingAgent",
                inputs={"query": "search docs"}
            )
        else:
            # 自己处理
            return CmdRunAction("vim file.py")

# BrowsingAgent 执行搜索，结果回到 CodeActAgent
```

## 相关论文

- [[OpenDevin]]: 核心协作机制

## 相关概念

- [[Event Stream]]: 委托事件也记录在 Stream
- [[环境抽象]]: 不同设计，环境是被动广播

---

## 与环境抽象的对比

| 维度 | DelegateAction | 环境抽象 |
|------|----------------|----------|
| 通信模式 | 点对点 | 广播 |
| 目的 | 专业化分工 | 共享场景 |
| 主动性 | Agent 主动委托 | 环境被动转发 |
| 适用场景 | 任务分解 | 模拟世界 |

**组合使用**:
```
用户任务 → CodeActAgent（主）
                ├── 委托 → BrowsingAgent（搜索）
                └── 委托 → PythonAgent（编码）
                └── 自己 → Terminal（执行）
```