# Agent 学习计划

> 目标：**高端 Agent 岗位** —— 具备原理深度、工程能力、评估体系、可展示成果

---

## 为什么这个计划能帮你拿到高端岗位

| 高端岗位要求 | 本计划覆盖 |
|-------------|-----------|
| 深度理解原理 | 阶段一、二：从框架到模型层，理解本质 |
| 工程实践能力 | 阶段四：生产级可靠性、安全、性能 |
| 评估改进能力 | 阶段三：Benchmark、Eval 飞轮（这是护城河） |
| 可展示成果 | 阶段五：开源、博客、项目 |

---

## 阶段一：基础构建（框架层）

**时间**：2-3 周
**目标**：理解框架设计哲学，不是学用法

### 1.1 核心抽象

- [x] Agent = LLM + Tool Call Loop 的实现方式
- [x] Memory 三种模式：短期、长期、工作记忆
- [x] State Management：有状态 vs 无状态
- [x] Tool Definition：Function Calling 的封装方式

> 详细笔记：[[核心抽象详解]]

### 1.2 动手实现

- [ ] **100 行代码实现最小 Agent**（无框架，理解本质）
- [ ] 添加 Memory（简单向量检索）
- [ ] 添加 Multi-Agent（简单路由）

**输出**：[[../notes/最小Agent实现]]
**面试问题**：你能不依赖框架从头实现一个 Agent 吗？

### 1.3 三大框架对比

**LangGraph**（Graph-based）：
- [ ] 核心概念：Node、Edge、StateGraph
- [ ] 关键问题：为什么用图而不是链？Human-in-the-loop 如何实现？

**CrewAI**（Role-based）：
- [ ] 核心概念：Agent、Task、Crew、Process
- [ ] 关键问题：Role 抽象是否过度？与 LangGraph 本质区别？

**AutoGen**（Conversation-driven）：
- [ ] 核心概念：ConversableAgent、GroupChat
- [ ] 关键问题：对话模式的灵活性 vs 可控性？

**输出**：[[../insights/三大框架对比]]
**面试问题**：什么场景用什么框架？为什么？

---

## 阶段二：本质深入（模型层）

**时间**：3-4 周
**目标**：理解框架解决不了的问题——这是区分高低端的关键

### 2.1 Planning & Reasoning

> 这是 Agent 的能力上限，由模型层决定

- [ ] 精读 ReAct / Tree-of-Thoughts / Plan-and-Solve 论文
- [ ] 研究 o3/Gemini 2.5 的 Chain-of-Thought 突破点
- [ ] 分析 Agent 在复杂任务上的失败模式
- [ ] 理解"规划-执行-修正"循环中的信息损耗

**输出**：[[../insights/Planning机制分析]]
**面试问题**：Planning 的理论边界在哪里？模型层 vs 框架层的分工？

### 2.2 Multi-Agent 协调

> 这是系统级复杂度的来源

- [ ] 信息传递中的损耗与幻觉累积
- [ ] Agent 自我认知能力（"我不知道"）
- [ ] Deadlock / 循环依赖检测
- [ ] LangGraph vs CrewAI vs AutoGen 的协调策略差异

**输出**：[[../insights/MultiAgent协调问题]]
**面试问题**：如何让多 Agent 系统可靠？信息损耗如何量化？

### 2.3 设计模式

> 从使用者视角转为设计者视角

- [ ] ReAct 模式：Reasoning + Acting 循环
- [ ] Plan-and-Execute：先规划后执行
- [ ] Self-Reflection：自我修正
- [ ] Memory Pattern：短期/长期/工作记忆

**输出**：[[../insights/框架设计模式]]

---

## 阶段三：评估体系（差异化能力）

**时间**：2-3 周
**目标**：掌握 Agent 评估方法——这是 Anthropic 的护城河，也是你的差异化能力

> ⚠️ 大多数工程师只会用框架，不会评估。这是高端岗位的核心能力。

### 3.1 Benchmark 研究

- [ ] **SWE-bench**：代码 Agent 的标准测试，分析 top agent 的解题策略
- [ ] **AgentBench**：通用 Agent 能力评估
- [ ] **TAU-bench**：表格推理
- [ ] 理解 eval 数据集设计的难点

### 3.2 评估飞轮

- [ ] 如何设计针对特定场景的 eval
- [ ] Eval 结果如何驱动系统改进
- [ ] 建立 eval → 改进 → 再 eval 的闭环

**输出**：[[../insights/Agent评估方法论]]
**面试问题**：你如何评估一个 Agent 是否好用？如何持续改进？

### 3.3 失败分析实践

- [ ] 分析 OpenDevin 在 SWE-bench 上的失败案例
- [ ] 总结失败模式，理解为什么"换框架也没用"

**输出**：[[../insights/Agent失败模式分析]]

---

## 阶段四：生产实践（工程能力）

**时间**：2-3 周
**目标**：从 demo 到 production——展示工程化能力

### 4.1 可靠性工程

- [ ] 工具调用失败的恢复策略（重试、fallback、降级）
- [ ] Cost / Latency 的动态权衡
- [ ] 长任务状态持久化与断点续传

### 4.2 安全边界

- [ ] Agent 权限控制模式
- [ ] Sandbox 设计
- [ ] 防止 Agent 越权操作

### 4.3 可观测性

- [ ] 接入 LangSmith 或类似工具
- [ ] 设计 Agent 的 tracing 和 logging 策略
- [ ] 建立异常告警机制

**输出**：[[../insights/Agent生产环境挑战]]
**面试问题**：你的 Agent 如何在生产环境保持稳定？

---

## 阶段五：求职输出（成果展示）

**时间**：持续
**目标**：把学习成果转化为可展示的资产

### 5.1 实践项目（必选 1 个）

| 项目 | 难度 | 亮点 |
|------|------|------|
| Research Agent | ⭐⭐ | 展示 Planning + Tool Use |
| Code Review Agent | ⭐⭐⭐ | 展示代码理解 + Multi-Agent |
| Data Analysis Agent | ⭐⭐⭐ | 展示 Eval 能力 + 可靠性 |

**要求**：
- 开源到 GitHub
- 有完整 README 和架构图
- 有 eval 结果和改进日志

### 5.2 技术博客（必选 2-3 篇）

选题建议：
- [ ] 《为什么 Claude Code 比开源框架好用？从原理分析》
- [ ] 《Agent 的 Planning 瓶颈在哪里？模型层 vs 框架层》
- [ ] 《如何评估一个 Agent？从 SWE-bench 学习》
- [ ] 《Multi-Agent 协调的核心挑战与解决方案》

### 5.3 开源贡献（加分项）

- [ ] 给 LangGraph / AutoGen 提 PR
- [ ] 修复 bug 或添加 feature
- [ ] 贡献文档或 example

---

## 进度追踪

| 阶段 | 内容 | 状态 | 开始 | 完成 |
|------|------|------|------|------|
| 1 | 基础构建（框架层） | 🔲 | - | - |
| 2 | 本质深入（模型层） | 🔲 | - | - |
| 3 | 评估体系（差异化） | 🔲 | - | - |
| 4 | 生产实践（工程能力） | 🔲 | - | - |
| 5 | 求职输出（成果展示） | 🔲 | - | - |

---

## 学习资源

### 必读论文

| 优先级 | 论文 | 价值 |
|--------|------|------|
| P0 | ReAct, Tree-of-Thoughts | Planning 基础 |
| P0 | Anthropic: Building Effective Agents | 工程实践 |
| P1 | OpenDevin, AutoGen 论文 | 架构设计 |
| P1 | SWE-bench 论文 | 评估方法 |

### 实践资源

- [LangGraph 官方教程](https://langchain-ai.github.io/langgraph/)
- [LangChain Academy](https://academy.langchain.com/)（免费）
- [SWE-bench Leaderboard](https://www.swebench.com/)（分析 top agent）

### 深度文章

- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [LangGraph vs CrewAI 对比](https://blog.langchain.dev/langgraph-multi-agent/)

---

## 核心问题清单

> 这些问题是面试的高频考点，持续更新答案

1. ✅ 为什么 Claude Code/Cursor 比开源框架好用？本质差异是什么？
2. ✅ Planning 的理论边界在哪里？模型层 vs 框架层的分工？
3. ✅ Multi-Agent 信息传递的损耗如何解决？
4. ✅ 如何让 Agent 知道"我不知道"而不是瞎编？
5. ✅ Eval 飞轮如何建立？
6. ✅ 什么场景用什么框架？
7. ✅ 如何评估一个 Agent 是否好用？
8. ✅ Agent 在生产环境如何保持稳定？

---

## 学习笔记索引

### 基础

- [ ] [[../notes/最小Agent实现]]
- [ ] [[../insights/三大框架对比]]
- [ ] [[../insights/框架设计模式]]

### 深入

- [ ] [[../insights/Planning机制分析]]
- [ ] [[../insights/MultiAgent协调问题]]
- [ ] [[../insights/框架边界认知]]

### 评估

- [ ] [[../insights/Agent评估方法论]]
- [ ] [[../insights/Agent失败模式分析]]

### 生产

- [ ] [[../insights/Agent生产环境挑战]]