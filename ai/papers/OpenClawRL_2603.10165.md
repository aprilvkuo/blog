---
title: OpenClawRL
description: OpenClaw-RL: Train Any Agent Simply by Talking 双模式研读报告
date: 2026-03-27
arxiv: 2603.10165
category: rl
tags: ['optimization', 'rl', 'scientific']
outline: [2, 3]
---

::: tip 📄 论文信息
- **arXiv**: [2603.10165](https://arxiv.org/abs/2603.10165)
- **分类**: 强化学习
- **标签**: optimization, rl, scientific
:::


::: info 📑 目录
本文档包含完整的论文研读报告，包括深度学术速读和技术实现分析两部分。
:::

# OpenClaw-RL: Train Any Agent Simply by Talking 双模式研读报告

**论文信息**: arXiv:2603.10165v1 [cs.CL] | 2026 年 3 月 10 日  
**作者**: Yinjie Wang, Xuyang Chen, Xiaolong Jin, Mengdi Wang, Ling Yang  
**代码**: https://github.com/Gen-Verse/OpenClaw-RL

---

## Part A: 深度专业学术速读报告

## 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 现有 Agent 系统在每次行动后都会接收 next-state 信号（用户回复、工具输出、状态变化），但仅将其作为下一行动的上下文，未将其作为在线学习信号。本研究旨在回收这些被浪费的信号，实现 Agent 在部署中持续自我优化。 |
| **方法** | 提出 OpenClaw-RL 框架，采用四组件完全解耦的异步架构（Policy Serving、Environment、PRM Judging、Policy Training）。设计两种互补的信号回收方法：Binary RL 通过 PRM 将评估性信号转换为标量过程奖励；Hindsight-Guided OPD 从 next-state 提取文本提示，构建增强教师上下文进行 token 级蒸馏。 |
| **结果** | 个人 Agent 场景中，组合方法在 36 次交互后实现显著提升（得分从 0.17 提升至 0.81）；通用 Agent 场景中，整合过程奖励和结果奖励在工具调用（0.30 vs 0.17）和 GUI（0.33 vs 0.31）任务上均优于仅用结果奖励。 |
| **结论** | Next-state 信号是通用的在线学习源，个人对话、终端执行、GUI 交互、SWE 任务和工具调用轨迹都可以流入同一训练循环。Binary RL 和 OPD 的组合产生显著优化增益，使模型能够同时个性化和改进长视野任务能力。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

当前部署的 AI Agent 系统存在一个根本性浪费：每次行动后，Agent 都会接收一个 next-state 信号（用户回复、工具执行结果、GUI 状态转换或测试裁决），但现有系统仅将其视为下一行动的上下文信息（Fu et al., 2025; Mei et al., 2025; Sheng et al., 2025; Wang et al., 2025b; Zhu et al., 2025）。本研究的核心洞察是：next-state 信号编码了关于前一行动的隐式评估信息，包括行动表现如何以及应该如何改进。

核心研究问题 (RQs)：
1. 如何从异构交互流中回收 next-state 信号作为在线学习源？
2. 评估性信号和指令性信号能否被分别提取并用于策略优化？
3. 单一框架能否同时支持个人 Agent 个性化和通用 Agent 的大规模强化学习？

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

**过程奖励模型 (PRMs)**: PRMs 在数学推理领域已有广泛研究，证明步骤级监督优于仅结果监督（Lightman et al., 2023; Wang et al., 2024; Cui et al., 2025b）。然而，现有 PRM 研究几乎都依赖可验证的 ground truth，且主要在离线设置中使用。在个人 Agent 场景中，PRM 可以逐轮捕捉用户满意度；在通用 Agent 场景中，PRM 提供长视野任务所需的密集每步信用分配（Wang et al., 2026）。

**事后重标注与上下文增强**: Hindsight relabeling（Zhang et al., 2023; Hübotter et al., 2026）和上下文增强蒸馏（Yang et al., 2024b, 2025c）表明，将结构化修正信息添加到上下文中可以显著改善输出。但这些方法都操作于固定数据集，无法利用实时交互信号。

**研究缺口**: 现有 RL 系统要么完全忽略 next-state 信号，要么仅在离线、预收集的形式中利用它，依赖固定数据集或终端结果奖励。没有系统能够实时回收 next-state 信号作为在线学习源，且同时支持多种异构交互类型。

### 1.3. 研究目标与核心假设 (Objectives & Hypotheses)

**研究目标**:
1. 设计一个统一框架，从个人对话、终端、GUI、SWE 和工具调用环境中回收 next-state 信号
2. 开发两种互补的信号回收方法：Binary RL（评估性信号）和 Hindsight-Guided OPD（指令性信号）
3. 验证框架在个人 Agent 个性化和通用 Agent 强化学习中的有效性

**核心假设**:
- H1: Next-state 信号同时包含评估性和指令性信息，可被分别提取
- H2: Binary RL 和 OPD 是互补的，组合使用优于单独使用任一方法
- H3: 在长视野 Agent 任务中，整合过程奖励和结果奖励优于仅用结果奖励

---

## 2. 研究设计与方法 (Methodology)

### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

本研究采用系统构建与实证验证相结合的方法。首先形式化交互流为马尔可夫决策过程 (MDP)，然后设计 OpenClaw-RL 框架，最后通过模拟实验和真实场景实验验证有效性。

核心形式化：每个交互流定义为 MDP (S, A, T, r)：
- **状态 s_t**: 截至第 t 轮的完整对话或环境上下文
- **行动 a_t**: Agent 的响应，由策略π_θ生成的 token 序列
- **转移 T(s_{t+1}|s_t, a_t)**: 由环境决定，s_{t+1}是跟随 a_t 的用户回复、执行结果或工具输出
- **奖励 r(a_t, s_{t+1})**: 通过 PRM 评估器从 next-state 信号推断

### 2.2. 数据来源与样本 (Data Source & Sample)

**个人 Agent 场景**:
- 学生场景：LLM 模拟学生使用 OpenClaw 完成 GSM8K 数学题，要求避免被察觉使用 AI
- 教师场景：LLM 模拟教师使用 OpenClaw 批改作业，要求评语具体且友好
- 策略模型：Qwen3-4B，学习率 1×10⁻⁵，每 16 个样本触发一次训练

**通用 Agent 场景**:
- 终端 Agent：SETA RL 数据 (Shen et al., 2026)，128 个并行环境
- GUI Agent：OSWorld-Verified (Xie et al., 2024)，64 个并行环境，评估排除 Chrome 和多应用任务
- SWE Agent：SWE-Bench-Verified (Jimenez et al., 2023)，64 个并行环境
- 工具调用 Agent：DAPO RL 数据 (Yu et al., 2025a)，32 个并行环境，在 AIME 2024 上评估
- 模型：Qwen3-8B、Qwen3VL-8B-Thinking、Qwen3-32B、Qwen3-4B-SFT

### 2.3. 操作化与测量 (Operationalization & Measurement)

**Binary RL**:
- PRM 评估器对每个 (a_t, s_{t+1}) 进行 m 次独立查询，取多数投票 r_final ∈ {+1, -1, 0}
- 训练目标：PPO 风格 clipped surrogate，ε=0.2，ε_high=0.28，β_KL=0.02

**Hindsight-Guided OPD**:
- 步骤 1：Judge 提取分数和提示，仅当 score=+1 且提示长度>10 字符时保留
- 步骤 2：选择最长提示作为增强上下文 s_enhanced = s_t ⊕ hint
- 步骤 3：计算 token 级优势 A_t = logπ_teacher(a_t|s_enhanced) - logπ_θ(a_t|s_t)
- 步骤 4：使用与 Binary RL 相同的 clipped surrogate 损失

**组合方法**:
- 优势计算：A_t = w_binary·r_final + w_opd·(logπ_teacher - logπ_θ)，默认权重均为 1

**评估指标**:
- 个人 Agent：由同一 LLM 模拟器根据个人偏好分配个性化得分（0-1 范围）
- 通用 Agent：滚动任务准确率（终端/SWE）或任务成功率（GUI/工具调用）

---

## 3. 结果与发现 (Results & Findings)

### 3.1. 主要发现概述 (Overview of Key Findings)

**发现 1：组合方法最优**
在个人 Agent 场景中，Binary RL + OPD 组合方法在更新 8 步后得分 0.76，更新 16 步后得分 0.81，显著优于单独使用 Binary RL（0.25→0.23）或 OPD（0.25→0.72）。OPD 由于训练样本稀疏，效果显现较慢，但最终性能更高。

**发现 2：快速个性化**
在组合优化方法下，OpenClaw 仅需 36 次解题交互（学生场景）或 24 次批改交互（教师场景）即可实现显著且可见的改进。优化后，Agent 学会避免明显的 AI 风格措辞（如使用"bold"或过度结构化的分步响应），转向更自然随意的风格；在教师场景中学会写更友好、更详细的反馈。

**发现 3：过程奖励对长视野任务至关重要**
在通用 Agent 场景中，整合结果奖励和过程奖励在工具调用（0.30 vs 0.17）和 GUI（0.33 vs 0.31）设置上均优于仅用结果奖励。代价是需要额外资源托管 PRM。

**发现 4：框架支持多场景扩展**
OpenClaw-RL 成功支持终端、GUI、SWE 和工具调用四种真实场景，通过大规模环境并行化（128/64/64/32 个并行环境）实现可扩展的 RL 训练。

### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**表 3：不同优化方法性能对比**
| 方法 | 更新 8 步 | 更新 16 步 |
|---|---|---|
| Binary RL | 0.25 | 0.23 |
| OPD | 0.25 | 0.72 |
| 组合 | 0.76 | 0.81 |

该表显示组合方法在两个时间点都取得最佳性能。Binary RL 单独使用仅提供边际改进，OPD 在早期效果不明显但在后期显著提升，组合方法兼具两者的优势：Binary RL 提供广泛的梯度覆盖，OPD 在可用指令信号的样本上提供高分辨率修正。

**表 4：整合奖励 vs 仅结果奖励**
| 设置 | 整合奖励 | 仅结果奖励 |
|---|---|---|
| 工具调用 | 0.30 | 0.17 |
| GUI | 0.33 | 0.31 |

该表证明在长视野任务中，过程奖励提供密集信用分配，使策略能够在整个轨迹中获得监督信号，而不仅是在终端步骤。

**图 2：优化前后对比示例**
学生场景优化前：Agent 输出过度结构化、使用"Final Answer"等明显 AI 风格措辞
学生场景优化后：Agent 输出更自然随意，如"The answer is 100%. Here's the breakdown..."
教师场景优化前：简短评语"Correct. Well done!"
教师场景优化后：详细友好评语，包含具体表扬和 emoji

---

## 4. 讨论 (Discussion)

### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

OpenClaw-RL 的核心贡献在于识别并回收了两种被浪费的 next-state 信号。评估性信号通过 PRM 转换为密集的过程奖励，解决了长视野任务中的信用分配问题；指令性信号通过 OPD 转换为 token 级优势监督，提供了比标量奖励更丰富的方向性指导。

组合方法的成功验证了 H2：Binary RL 和 OPD 确实是互补的。Binary RL 接受所有评分轮次，适用于任何 next-state 信号（包括隐式反应如用户重新提问）；OPD 仅在 next-state 包含明确指令内容时启用（如用户给出明确修正或环境产生详细错误轨迹）。两者结合实现了"广泛覆盖 + 高分辨率修正"的双重优势。

### 4.2. 理论贡献 (Theoretical Contributions)

**扩展 PRM 应用范围**: 将 PRM 从数学推理领域扩展到通用 Agent 场景，包括个人对话、终端、GUI、SWE 和工具调用。关键创新是在线设置中从实时 next-state 信号推断过程奖励，而非依赖预收集的 ground truth。

**统一异构交互流**: 首次证明个人对话、终端执行、GUI 交互、SWE 任务和工具调用轨迹可以流入同一训练循环，由单一策略同时学习。这打破了现有系统为每种环境设计专用训练管道的局限。

**On-Policy Distillation 创新**: Hindsight-Guided OPD 统一了事后重标注、上下文增强蒸馏和自蒸馏三条研究线索：从实时 next-state 提取文本提示（事后重标注），模型在提示增强上下文中作为自己的教师（自蒸馏），token 级 log 概率差提供方向性优势监督（无需预收集数据、外部教师或配对偏好）。

### 4.3. 实践启示 (Practical Implications)

**个人 Agent 部署**: OpenClaw-RL 使个人 Agent 能够通过正常使用自动优化，无需单独的数据收集或标注阶段。用户只需像平常一样与 Agent 交互，系统会自动从对话信号中学习用户偏好。

**通用 Agent 训练**: 框架支持大规模并行环境部署，适用于需要长视野规划的任务（如软件开发、GUI 操作）。整合过程奖励和结果奖励可显著提升性能，但需权衡 PRM 托管成本。

**零服务中断**: 异步解耦架构确保模型在服务实时请求的同时进行训练，权重更新是优雅的，不会中断推理。这对于生产环境部署至关重要。

### 4.4. 局限性与未来研究 (Limitations & Future Research)

**局限性**:
1. PRM 评估器需要额外计算资源，特别是在高并发场景中
2. OPD 依赖 next-state 中包含可提取的指令信号，在隐式反馈场景中效果受限
3. 个人 Agent 实验使用 LLM 模拟器，真实用户场景的效果需进一步验证
4. 目前仅训练 main-line 轮次，side turn（辅助查询、记忆组织）未用于训练

**未来研究方向**:
1. 探索更高效的 PRM 实现，如轻量化评估器或缓存机制
2. 研究如何从隐式反馈（如用户沉默、会话终止）中提取信号
3. 在真实用户部署中进行长期跟踪研究，验证个性化效果的持久性
4. 扩展支持更多交互类型，如语音交互、多模态交互
5. 研究多用户场景下的联邦学习或个性化聚合策略

---

## 5. 结论 (Conclusion)

OpenClaw-RL 基于一个简单而深刻的洞察：每次 Agent 交互产生的 next-state 信号是通用的，单一策略可以同时从所有信号中学习。通过 Binary RL 回收评估性信号作为标量过程奖励，通过 Hindsight-Guided OPD 回收指令性信号作为 token 级优势监督，组合两种方法产生显著优化增益。结果是：一个模型能够同时个性化到个体用户并改进长视野 Agent 任务能力，完全从它已经在进行的交互中训练。

---

## 6. 核心参考文献 (Core References)

1. **Wang et al. (2026)**. RLAnything: Forge environment, policy, and reward model in completely dynamic RL system. arXiv:2602.02488. *为 OpenClaw-RL 提供过程奖励整合的实证基础*

2. **Yang et al. (2025c)**. Supercorrect: Advancing small LLM reasoning with thought template distillation and self-correction. ICLR. *上下文增强蒸馏方法的先驱工作*

3. **Zhang et al. (2023)**. The wisdom of hindsight makes language models better instruction followers. ICML. *事后重标注方法的代表性工作*

4. **Lightman et al. (2023)**. Let's verify step by step. ICLR. *过程奖励模型在数学推理中的奠基性工作*

5. **Zhu et al. (2025)**. slime: An LLM post-training framework for RL scaling. GitHub. *OpenClaw-RL 异步架构的基础框架*

---

## Part B: 核心逻辑链与根本价值提炼

## 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | 现有 Agent 系统每次行动后都会收到 next-state 信号（用户回复、工具输出、状态变化），但仅将其用作下一行动的上下文，完全浪费了其中隐含的评估信息（行动表现如何）和指令信息（应该如何改进）。这是一个普遍存在但被忽视的学习信号浪费问题。 |
| **切入视角** | 关键洞察：next-state 信号是"流无关"的——个人对话、终端执行、GUI 交互、SWE 任务和工具调用轨迹本质上都是同一类交互，可以由单一策略在同一训练循环中学习。这打破了现有系统为每种环境设计专用管道的思维定式。 |
| **关键方法** | 双管齐下：(1) Binary RL 用 PRM 评估器将 next-state 转换为标量奖励（+1/-1/0），提供广泛但粗糙的监督；(2) Hindsight-Guided OPD 从 next-state 提取文本提示，构建"增强教师上下文"，计算 token 级 log 概率差作为方向性优势，提供稀疏但高分辨率的修正。两者用加权损失组合。 |
| **核心发现** | 组合方法在个人 Agent 场景中 36 次交互后得分从 0.17 提升至 0.81；在通用 Agent 场景中，整合过程奖励和结果奖励在工具调用（0.30 vs 0.17）和 GUI（0.33 vs 0.31）上显著优于仅用结果奖励。证明 next-state 信号确实是有效的在线学习源。 |

---

## 方法公式化

**OpenClaw-RL = (Binary RL + Hindsight-Guided OPD) × 异步解耦架构**

其中：
- **Binary RL**: 优势 A_t = PRM(a_t, s_{t+1}) → {+1, -1, 0}（多数投票）
- **OPD**: 优势 A_t = logπ_teacher(a_t | s_t ⊕ hint) - logπ_θ(a_t | s_t)
- **组合**: A_t = w_binary·A_t^binary + w_opd·A_t^opd（默认权重均为 1）
- **异步架构**: Policy Serving → Environment → PRM Judging → Policy Training（四组件完全解耦，零阻塞）

---

## 最终双重总结

**一句话总结（核心价值）**：OpenClaw-RL 通过识别并回收每次 Agent 交互中 next-state 信号隐含的评估性和指令性信息，设计了 Binary RL 和 Hindsight-Guided OPD 两种互补方法，在完全解耦的异步架构中实现单一策略同时从个人对话、终端、GUI、SWE 和工具调用等多种异构交互流中在线学习，使 Agent 能够通过正常使用持续自我优化。

**一句话总结（大白话版）**：就像人能从别人的反应中学到东西一样，OpenClaw-RL 让 AI Agent 能从用户的每次回复、工具的每次输出中偷偷学习——用户说"不对"它就知道错了，用户说"应该先检查文件"它就知道怎么改，用得越多就越聪明，而且不打扰正常使用。
