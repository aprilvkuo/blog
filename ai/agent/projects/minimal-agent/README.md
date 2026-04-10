# Minimal Agent

> 不依赖框架，用 ~100 行代码实现 Agent 核心，理解本质

## 目标

- [ ] Step 1: 最小 Agent（~50 行）- 核心循环
- [ ] Step 2: 添加 Memory（~30 行）- 对话历史
- [ ] Step 3: Multi-Agent 路由（~20 行）- 多 Agent 协作

## 运行

```bash
# 设置 API Key
export OPENAI_API_KEY=your_key

# 运行
python minimal_agent.py
```

## 学习笔记

- [[../../notes/最小Agent实现]]

## 关键问题

1. 如何定义工具？Function Calling 的格式是什么？
2. 如何判断 LLM 想要调用工具 vs 想要回复？
3. 如何处理多次工具调用？
4. 如何处理上下文溢出？
5. 如何实现 Agent 路由？