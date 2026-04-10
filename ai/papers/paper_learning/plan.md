---
title: 论文学习计划
description: AI 论文研读学习路线图
created: 2026-03-28
status: in_progress
---

# 论文学习计划

基于 [论文索引](../index.md) 中的 34 篇论文，制定以下学习路线。

## 学习进度追踪

- [x] 阶段一：基础框架 ✅ 2026-03-28
- [ ] 阶段二：记忆与 RAG
- [ ] 阶段三：推理优化
- [ ] 阶段四：Agent 进阶
- [ ] 阶段五：领域应用

---

## 阶段一：基础框架（1-2 周）

**目标**：掌握核心工具和平台

| 状态 | 论文 | 优先级 | 笔记 |
|------|------|--------|------|
| ✅ 完成 | [OpenDevin](../OpenDevin_2407.16741.md) | ⭐⭐⭐ | [大白话](./notes/OpenDevin_大白话.md) / [深入](./notes/OpenDevin_深入.md) |
| ✅ 完成 | [AgentScope](../AgentScope_2407.17789.md) | ⭐⭐⭐ | [大白话](./notes/AgentScope_大白话.md) / [深入](./notes/AgentScope_深入.md) |
| ✅ 完成 | [LlamaFactory](../LlamaFactory_2403.13372.md) | ⭐⭐ | [大白话](./notes/LlamaFactory_大白话.md) / [深入](./notes/LlamaFactory_深入.md) |

**关键收获**：
- Agent 架构设计模式（事件流、动作-观察循环）
- 多智能体协作机制（Actor 分布式、任务委托）
- LLM 微调基础（LoRA/QLoRA、Model-Sharing RLHF）

**论文 PDF 位置**：[papers/paper_learning/pdfs/](./pdfs/)

---

## 阶段二：记忆与 RAG（1 周）

**目标**：理解 LLM 记忆扩展技术

| 状态 | 论文 | 优先级 | 笔记 |
|------|------|--------|------|
| ⬜ | [MemOS](../MemOS_2507.03724.md) | ⭐⭐⭐ | [笔记](./notes/MemOS.md) |
| ⬜ | [Mem0](../Mem0_2504.19413.md) | ⭐⭐⭐ | [笔记](./notes/Mem0.md) |
| ⬜ | [LightRAG](../LightRAG_2410.05779.md) | ⭐⭐ | [笔记](./notes/LightRAG.md) |

**对比重点**：
- MemOS vs Mem0 vs EverMemOS 的记忆模型差异
- 图增强检索 vs 向量检索

---

## 阶段三：推理优化（1 周）

**目标**：掌握模型部署优化技术

| 状态 | 论文 | 优先级 | 笔记 |
|------|------|--------|------|
| ⬜ | [PowerInfer](../PowerInfer_2312.12456.md) | ⭐⭐⭐ | [笔记](./notes/PowerInfer.md) |
| ⬜ | [Bitnet.cpp](../Bitnetcpp_2502.11880.md) | ⭐⭐ | [笔记](./notes/Bitnet.md) |
| ⬜ | [SpecEyes](../SpecEyes_2603.23483.md) | ⭐⭐ | [笔记](./notes/SpecEyes.md) |

**实践方向**：
- 消费级 GPU 部署优化
- 量化技术对比
- 推测解码原理

---

## 阶段四：Agent 进阶（1-2 周）

**目标**：深入 Agent 架构设计

| 状态 | 论文 | 优先级 | 笔记 |
|------|------|--------|------|
| ⬜ | [HyperAgents](../Hyperagents_2603.19461.md) | ⭐⭐⭐ | [笔记](./notes/HyperAgents.md) |
| ⬜ | [AI Scientist-v2](../AIScientistv2_2504.08066.md) | ⭐⭐⭐ | [笔记](./notes/AIScientist.md) |
| ⬜ | [MiroThinker](../MiroThinker_2511.11793.md) | ⭐⭐ | [笔记](./notes/MiroThinker.md) |
| ⬜ | [EvoScientist](../EvoScientist_2603.08127.md) | ⭐⭐ | [笔记](./notes/EvoScientist.md) |

**深度思考**：
- Agent 自改进机制
- 思维链与白板推理
- 多智能体演化

---

## 阶段五：领域应用（按需学习）

### 文档处理方向
| 状态 | 论文 | 笔记 |
|------|------|------|
| ⬜ | [MinerU 2.5](../MinerU2.5_2509.22186.md) | [笔记](./notes/MinerU.md) |
| ⬜ | [SmolDocling](../SmolDocling_2503.11576.md) | [笔记](./notes/SmolDocling.md) |
| ⬜ | [PaddleOCR-VL](../PaddleOCRVL_2510.14528.md) | [笔记](./notes/PaddleOCR.md) |

### 多模态方向
| 状态 | 论文 | 笔记 |
|------|------|------|
| ⬜ | [LTX-2](../LTX2_2601.03233.md) | [笔记](./notes/LTX2.md) |
| ⬜ | [Fish Audio S2](../FishAudioS2_2603.08823.md) | [笔记](./notes/FishAudio.md) |
| ⬜ | [VideoDetective](../VideoDetective_2603.22285.md) | [笔记](./notes/VideoDetective.md) |

### 金融方向
| 状态 | 论文 | 笔记 |
|------|------|------|
| ⬜ | [TradingAgents](../TradingAgents_2412.20138.md) | [笔记](./notes/TradingAgents.md) |

### 机器人/RL 方向
| 状态 | 论文 | 笔记 |
|------|------|------|
| ⬜ | [OpenClawRL](../OpenClawRL_2603.10165.md) | [笔记](./notes/OpenClawRL.md) |
| ⬜ | [MetaClaw](../MetaClaw_2603.17187.md) | [笔记](./notes/MetaClaw.md) |

---

## 学习建议

1. **动手实践**：Agent 类论文建议复现核心功能
2. **对比阅读**：同主题论文一起看（如 MemOS vs Mem0 vs EverMemOS）
3. **关注代码**：OpenDevin、AgentScope、LlamaFactory 都有开源仓库
4. **联系项目**：TradingAgents 和股票分析系统架构类似，值得深入研究

---

## 笔记目录结构

```
paper_learning/
├── plan.md           # 本文件 - 学习计划
├── notes/            # 学习笔记
│   ├── OpenDevin_大白话.md
│   ├── OpenDevin_深入.md
│   ├── AgentScope_大白话.md
│   ├── AgentScope_深入.md
│   ├── LlamaFactory_大白话.md
│   ├── LlamaFactory_深入.md
│   └── ...
├── pdfs/             # 论文 PDF
│   ├── OpenDevin_2407.16741.pdf
│   ├── AgentScope_2407.17789.pdf
│   └── LlamaFactory_2403.13372.pdf
└── insights/         # 跨论文总结（阶段一产出）
    ├── Event_Stream.md      # 时序化 Action-Observation
    ├── Actor_Model.md       # 分布式并行机制
    ├── Placeholder.md       # 非阻塞占位符
    ├── 环境抽象.md          # 环境即 Agent
    ├── DelegateAction.md    # 任务委托机制
    ├── Model-Sharing_RLHF.md # 单模型多角色
    ├── QLoRA.md             # 量化微调
    └── Agent架构对比.md     # 三篇论文架构对比
```

---

## 相关资源

- [论文索引](../index.md) - 所有论文概览
- [Stock Analysis](../../finance/stock-analysis/) - 交易系统实践