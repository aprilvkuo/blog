---
title: MiroThinker
description: MiroThinker: Pushing the Performance Boundaries of Open-Source Research Agents via Model, Context, and Interactive Scaling 双模式研读报告
date: 2026-03-27
arxiv: 2511.11793
category: agent
tags: ['optimization', 'llm', 'agent', 'scientific']
outline: [2, 3]
---

::: tip 📄 论文信息
- **arXiv**: [2511.11793](https://arxiv.org/abs/2511.11793)
- **分类**: Agent/智能体
- **标签**: optimization, llm, agent, scientific
:::


::: info 📑 目录
本文档包含完整的论文研读报告，包括深度学术速读和技术实现分析两部分。
:::

# MiroThinker: Pushing the Performance Boundaries of Open-Source Research Agents via Model, Context, and Interactive Scaling 双模式研读报告

**论文信息：** arXiv:2511.11793 [cs.CL] | MiroMind Team | 2025 年 11 月

---

## Part A: 深度专业学术速读报告

### 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 大语言模型正从静态文本生成器向动态工具增强型智能体转变。研究能力成为智能新前沿，但开源研究智能体在模型规模、上下文长度和交互深度上与商业系统存在明显差距。本研究旨在通过三维度扩展（模型、上下文、交互）推动开源研究智能体的性能边界。 |
| **方法** | 基于 Qwen2.5/Qwen3 模型，采用 ReAct 范式，设计三阶段训练流程（监督微调、偏好优化、强化学习）。提出交互扩展（Interactive Scaling）作为第三维度，配合 256K 上下文窗口和基于近因的上下文保留策略，支持每任务最多 600 次工具调用。 |
| **结果** | MiroThinker-72B 在四个基准测试中取得领先：GAIA 81.9%、HLE 37.7%、BrowseComp 47.1%、BrowseComp-ZH 55.6%，超越先前开源智能体，接近 GPT-5-high 等商业系统。 |
| **结论** | 交互深度展现出与模型规模和上下文长度类似的扩展行为，是构建下一代开源研究智能体的第三个关键维度。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

大语言模型（LLMs）的快速演进引发了人工智能范式的转变：从静态文本生成器转向能够推理并与现实世界交互的动态工具增强型智能体。在这一新兴范式中，**研究能力**（research capability）成为智能的新前沿。实现研究级推理不仅需要语言流畅性，还需要提出假设、检索和验证证据、以及跨多源信息综合洞察的能力。

专有系统如 ChatGPT Agent 和 Claude Research 展示了接近人类的专业能力，但这些系统保持封闭状态，限制了透明度、可复现性和社区驱动的创新。

开源社区虽取得显著进展，但存在两大局限：
1. **基础模型层面**：开源权重 LLM 通常只发布模型权重，未提供端到端研究推理所需的完整工具套件或智能体框架
2. **专用研究智能体层面**：模型规模相对较小，受限于上下文长度和交互深度，与领先商业研究智能体存在明显性能差距

**核心研究问题**：如何推动开源研究智能体的性能边界，缩小与商业系统的差距？

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

**Agent Foundation Models (AFMs)**：GPT-5、Claude-4.5、Grok-3、Kimi K2、MiniMax M2、GLM-4.6、DeepSeek-V3.1 等模型在训练时明确纳入智能体导向能力（决策、工具使用、与环境交互），但仍主要聚焦代码和搜索智能体。

**Deep Research Models**：
- **专有系统**：OpenAI Deep Research、Claude Research、Kimi-Researcher、Grok DeepSearch 等将 LLM 与智能体工具使用和长程推理结合
- **开源系统**：WebThinker、WebSailor、WebShaper、Tongyi DeepResearch、Cognitive Kernel-Pro、AFM、WebDancer、DeepMiner 等探索新训练算法和动态记忆机制，但模型规模小、上下文和交互深度受限

**研究缺口**：现有开源研究智能体缺乏系统性的**交互扩展**能力，无法支持深度、多轮的研究工作流。

### 1.3. 研究目标与核心假设/命题 (Objectives & Hypotheses/Propositions)

**研究目标**：引入 MiroThinker v1.0，一个开源高性能研究智能体模型，沿三个关键维度推动开源系统性能边界：
1. **模型规模**（Model Size）
2. **上下文长度**（Context Length）
3. **交互深度**（Interaction Depth）

**核心命题**：
- 交互深度展现出与模型规模和上下文长度类似的扩展行为
- 通过强化学习实现的交互扩展可使模型在 256K 上下文窗口内执行多达 600 次工具调用
- 三维度协同扩展可使开源智能体性能接近商业系统

---

## 2. 研究设计与方法 (Methodology)

### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

MiroThinker v1.0 基于 **ReAct 范式**（Reasoning + Acting）在单智能体设置下开发。模型在推理、工具调用和观察之间交替迭代，直至终止。

**形式化定义**：
- 在步骤 t，智能体维护轨迹：H_t = {(T¹, A¹, O¹), ..., (T^(t-1), A^(t-1), O^(t-1))}
- 思考模型生成内部思考：T_t = f_θ(q, H_t)
- 行动策略输出工具调用：A_t = π_θ(H_t, T_t)
- 环境执行并返回观察：O_t = Tool(A_t)
- 更新轨迹：H_(t+1) = H_t ∪ {(T_t, A_t, O_t)}

### 2.2. 数据来源与样本 (Data Source & Sample)

**MiroVerse v1.0 数据集**由两部分组成：

**1. MultiDocQA 合成**：
- 文档语料库：Wikipedia、Common Crawl、精选网络存储库
- 通过超链接构建知识图谱，进行类别平衡采样
- 事实提取与约束模糊化（时间/空间泛化、指代间接化）
- 使用 LLM 生成需要跨文档多跳推理的问题

**2. 智能体轨迹合成**：
- **智能体范式**：ReAct 单智能体 + MiroFlow 多智能体
- **工具调用机制**：Function Calling + Model Context Protocol (MCP)
- **多样化 LLM**：GPT-OSS、DeepSeek-V3.1 等

**开源数据补充**：MuSiQue、HotpotQA、WebWalkerQA-Silver、MegaScience、TaskCraft、QA-Expert-Multi-Hop-V1.0、OneGen-TrainDataset-MultiHopQA、2WikiMultihopQA、WikiTables、WebShaper、WebDancer、Toucan-1.5M，以及 AM-Thinking-v1-Distilled 和 Nemotron-Post-Training-Dataset。

### 2.3. 操作化与测量 (Operationalization & Measurement)

**工具接口**：
1. **执行环境**：Linux 沙箱，支持 create_sandbox、run_command、run_python_code
2. **文件管理**：upload_file_from_local_to_sandbox、download_file_from_sandbox_to_local、download_file_from_internet_to_sandbox
3. **信息检索**：google_search（Google 搜索）、scrape_and_extract_info（基于 Qwen3-14B 的网页信息提取）

**上下文管理策略**：
1. **基于近因的上下文保留**：仅保留最近 K 个工具响应，保留完整的思考和行动序列
   - 定义保留索引集：S_t^(K) = {i ∈ {1,...,t-1} | i ≥ t-K}
   - 构建近因过滤历史：Ĥ_t，掩蔽 S_t^(K) 之外的工具响应
2. **结果截断**：对过长工具输出进行截断并添加"[Result truncated]"标记

**训练流程**（三阶段）：
1. **智能体监督微调**（Agentic SFT）：学习模仿涉及多跳推理和工具使用的专家轨迹
2. **偏好优化**（Preference Optimization）：使决策与任务目标对齐
3. **强化学习**（Reinforcement Learning）：驱动真实环境中的创造性探索和泛化

**评估指标**：在 GAIA、HLE、BrowseComp、BrowseComp-ZH 四个基准测试上的准确率。

---

## 3. 结果与发现 (Results & Findings)

### 3.1. 主要发现概述 (Overview of Key Findings)

**MiroThinker v1.0 提供三个变体**：8B、30B、72B，配备 256K 上下文窗口和完整工具套件。

**基准测试结果（72B 变体）**：

| 基准测试 | MiroThinker-72B | 最强开源对手 | 提升 |
|---|---|---|---|
| GAIA-Text-Only | 81.9% | MiniMax-M2 (75.7%) | +6.2 pts |
| HLE | 37.7% | Tongyi-DeepResearch (32.9%) | +4.8 pts |
| BrowseComp | 47.1% | MiniMax-M2 (45.1%) | +2.0 pts |
| BrowseComp-ZH | 55.6% | GLM-4.6 (49.5%) | +6.1 pts |

**关键发现**：
- MiroThinker 在所有基准测试中一致超越先前开源智能体
- 性能接近 GPT-5-high、Claude Research 等商业系统
- 多语言推理能力强劲（BrowseComp-ZH 表现突出）

### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**Figure 1**：MiroThinker 与最先进智能体和智能体基础模型的比较
- 展示了 MiroThinker-72B 在多个基准测试上相对于开源和商业系统的位置
- 揭示了交互扩展带来的性能提升

**Figure 2**：MiroThinker v1.0 智能体架构概述
- 展示了结构化接口（执行环境、文件管理、信息检索）与近因感知上下文管理的集成
- 右侧示例说明了基于近因的上下文保留机制：早期轮次的工具输出被省略以维持上下文效率

**Figure 3**：数据构建流程概述
- 展示了来自 HuggingFace 和 GitHub 的公共数据集如何被过滤和验证
- 原始网络数据通过知识图谱生成和数据引擎处理
- 两种来源的 QA 对被转换为智能体轨迹，形成完整的 MiroVerse v1.0 数据集

---

## 4. 讨论 (Discussion)

### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

MiroThinker 的成功验证了**交互扩展**作为第三维度的有效性：

1. **交互深度与性能的正相关**：研究性能随模型参与更深、更频繁的代理 - 环境交互而可预测地提升
2. **环境反馈的价值**：与孤立运行的 LLM 测试时扩展不同，交互扩展利用环境反馈和外部信息获取来纠正错误并优化轨迹
3. **上下文效率**：简单的近因保留策略作为强基线，未导致性能下降，同时为交互扩展释放更多上下文空间

### 4.2. 理论贡献 (Theoretical Contributions)

1. **提出交互扩展维度**：首次系统性地将交互深度确立为与模型规模、上下文长度并列的第三个关键扩展维度
2. **验证扩展行为**：证明交互深度展现出与模型规模和上下文长度类似的扩展行为（scaling behaviors）
3. **开源研究智能体框架**：提供完整的开源研究智能体实现，包括模型权重、工具套件和训练方法

### 4.3. 实践启示 (Practical Implications)

1. **降低研究门槛**：开源高性能研究智能体使更多研究者和开发者能够访问先进的研究工具
2. **可复现性**：完整的开源实现支持社区复现、验证和改进
3. **定制化可能**：开源模型允许针对特定领域进行微调和定制
4. **成本效益**：提供 8B、30B、72B 三个变体，支持不同计算预算

### 4.4. 局限性与未来研究 (Limitations & Future Research)

**局限性**：
1. **HuggingFace 访问限制**：为防止信息泄露，工具中明确禁用了对 HuggingFace 的访问
2. **上下文管理简化**：当前使用简单的近因保留策略，可能未充分利用长期依赖
3. **单智能体设置**：虽然支持 MiroFlow 多智能体范式，但主要评估在单智能体设置下进行

**未来研究方向**：
1. 探索更复杂的上下文管理策略（如分层记忆、注意力机制）
2. 扩展多智能体协作研究能力
3. 针对特定领域（如科学文献、法律、医疗）的专业化研究智能体
4. 实时知识更新与长期记忆机制

---

## 5. 结论 (Conclusion)

MiroThinker v1.0 通过三维度扩展（模型规模、上下文长度、交互深度）推动了开源研究智能体的性能边界。72B 变体在 GAIA、HLE、BrowseComp、BrowseComp-ZH 四个基准测试中分别取得 81.9%、37.7%、47.1%、55.6% 的准确率，超越先前开源智能体并接近商业系统。

核心贡献在于确立了**交互扩展**作为构建下一代开源研究智能体的第三个关键维度，与模型容量和上下文窗口形成互补。通过强化学习，模型实现了高效的交互扩展：在 256K 上下文窗口内可执行多达 600 次工具调用，支持持续多轮推理和复杂现实世界研究工作流。

---

## 6. 核心参考文献 (Core References)

1. **Yao et al. (2022)**. ReAct: Synergizing Reasoning and Acting in Language Models. *arXiv:2210.03629*
2. **OpenAI (2025)**. GPT-5 Technical Report.
3. **Anthropic (2025)**. Claude Research System Card.
4. **Moonshot AI (2025)**. Kimi-Researcher Technical Report.
5. **OpenAI (2025)**. Deep Research System Overview.

---

## Part B: 核心逻辑链与根本价值提炼

### 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | 开源研究智能体与商业系统（如 ChatGPT Agent、Claude Research）之间存在显著性能差距，根源在于现有开源方案仅关注模型规模或上下文长度的单一维度扩展，忽视了**交互深度**这一关键维度，导致无法支持复杂、多轮的真实研究工作流。 |
| **切入视角** | 作者提出**交互扩展**（Interactive Scaling）作为第三维度：不是让模型在孤立环境中进行更长的推理链（易导致退化），而是训练模型处理更深、更频繁的代理 - 环境交互，利用环境反馈和外部信息获取来纠正错误并优化轨迹。这是区别于传统 test-time scaling 的关键转折点。 |
| **关键方法** | 1) **三阶段训练**：监督微调建立基础智能体行为 → 偏好优化对齐决策目标 → 强化学习驱动真实环境探索；2) **近因上下文保留**：仅保留最近 K 个工具响应，保留完整思考 - 行动序列，在 256K 窗口内支持 600 次工具调用；3) **多源数据合成**：MultiDocQA + 智能体轨迹合成 + 开源数据集，覆盖多样化推理风格。 |
| **核心发现** | MiroThinker-72B 在四个基准测试中取得 81.9%（GAIA）、37.7%（HLE）、47.1%（BrowseComp）、55.6%（BrowseComp-ZH）的准确率，超越先前开源智能体并接近商业系统。分析表明，研究性能随交互深度增加而可预测提升，验证了交互深度的扩展行为与模型规模、上下文长度类似。 |

---

### 方法公式化

**可靠开源研究智能体 = (模型规模 + 上下文长度) × 交互深度 × 近因上下文管理**

或更简洁地：

**MiroThinker = (Qwen 基础模型 + 256K 上下文) × (600 次工具调用/任务) × 三阶段训练**

---

### 最终双重总结

**一句话总结（核心价值）**：MiroThinker 首次系统性地将交互深度确立为研究智能体的第三扩展维度，通过强化学习训练模型在 256K 上下文窗口内高效执行多达 600 次工具调用，使开源研究智能体性能首次接近商业系统，为社区提供了透明、可复现的高性能研究工具。

**一句话总结（大白话版）**：以前的开源 AI 助手只会"闷头想"，想得越久越容易出错；MiroThinker 学会了"边想边问"，通过不断查资料、验证信息来修正自己的思路，就像做研究时边思考边查文献一样，而且能连续查 600 次资料还不迷路，终于能和商业 AI 助手掰手腕了。

---

## 附录：资源链接

- **在线演示**：https://dr.miromind.ai/
- **代码仓库**：https://github.com/MiroMindAI/MiroThinker
- **模型权重**：https://huggingface.co/miromind-ai/MiroThinker-v1.0-72B
- **arXiv 论文**：https://arxiv.org/abs/2511.11793

---

*报告生成时间：2026 年 3 月 26 日*
