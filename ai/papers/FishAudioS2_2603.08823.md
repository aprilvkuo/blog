---
title: FishAudioS2
description: Fish Audio S2 Technical Report 双模式研读报告
date: 2026-03-27
arxiv: 2603.08823
category: multimodal
tags: ['speech', 'multimodal', 'scientific', 'optimization', 'vision', 'llm']
outline: [2, 3]
---

::: tip 📄 论文信息
- **arXiv**: [2603.08823](https://arxiv.org/abs/2603.08823)
- **分类**: 多模态
- **标签**: speech, multimodal, scientific, optimization, vision, llm
:::


::: info 📑 目录
本文档包含完整的论文研读报告，包括深度学术速读和技术实现分析两部分。
:::

# Fish Audio S2 Technical Report 双模式研读报告

---

## Part A: 深度专业学术速读报告

### 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 高质量、可控的文本转语音（TTS）系统在现代 AI 系统中日益重要，但大规模生成细粒度自然语言指令仍是主要瓶颈。本研究旨在开发一个支持多说话人、多轮生成、且能通过自然语言描述实现指令跟随控制的开源 TTS 系统。 |
| **方法** | 采用 Dual-AR（双自回归）架构，结合多用途数据流水线和多奖励 RL 对齐框架。数据流水线包含语音质量评估模型和丰富转录 ASR 模型，既用于预训练过滤又用于 RL 奖励。RL 采用 GRPO 变体，联合优化语义准确性、声学质量和说话人相似度。 |
| **结果** | Fish Audio S2 在多个基准测试中取得领先：Seed-TTS-Eval 中文 WER 0.54%、英文 WER 0.99%；Audio Turing Test 后验均值 0.483（指令重写后 0.515）；EmergentTTS-Eval 整体胜率 81.88%；推理 RTF 0.195，TTFA <100ms。 |
| **结论** | 通过 Dual-AR 架构、双用途数据流水线和多奖励 RL 对齐，Fish Audio S2 实现了细粒度自然语言控制、长音频连贯合成和原生多说话人多轮生成能力，在开源 TTS 领域树立了新标杆。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

文本转语音（TTS）技术已成为现代 AI 系统的核心组件，支撑着有声书 narrattion、视频配音和个性化聊天机器人等应用场景。近年来，大规模模型（如 Zhang et al., 2025; Du et al., 2025; Li et al., 2026; Hu et al., 2026）推动了 TTS 领域的快速发展。大多数工作遵循两阶段范式：模型首先基于文本生成高层离散语音 token，然后由独立的声学解码器将其解码为完整波形（Wang et al., 2023; Défossez et al., 2022; Kong et al., 2020; Anastassiou et al., 2024）。

然而，该领域面临两个关键挑战：第一，大规模生成细粒度自然语言指令（用于描述声音特征如情感、韵律等）仍然是主要瓶颈，这一过程难以手动扩展；第二，尽管强化学习（RL）方法如 DPO、PPO 和 GRPO 已在大语言模型（LLM）领域成为标准，但它们在 TTS 领域的采用仍然有限。

本文的核心研究问题是：**如何构建一个支持细粒度自然语言指令控制、具备高质量语音生成能力且可大规模部署的开源 TTS 系统？**

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

作者引用了多个关键研究方向：

1. **神经编解码器与离散语音表示**：Descript Audio Codec (DAC) (Kumar et al., 2023) 提供了高保真音频压缩方案；Moshi (Défossez et al., 2024) 引入了滑动窗口 Transformer 块用于长程依赖建模。

2. **大规模 TTS 系统**：Seed-TTS (Anastassiou et al., 2024)、CosyVoice 系列 (Du et al., 2024, 2025)、Qwen3-TTS (Hu et al., 2026) 等展示了大规模预训练的有效性。

3. **数据标注与清洗**：近期工作引入了复杂的流程来清洗语音语料库和标注副语言特征（Cheng et al., 2025; Yang et al., 2025），但细粒度指令的大规模生成仍是瓶颈。

4. **强化学习对齐**：DPO (Rafailov et al., 2023)、PPO (Schulman et al., 2017) 和 GRPO (Shao et al., 2024) 在 LLM 领域已广泛应用（Guo et al., 2025; Agarwal et al., 2025），但在 TTS 领域的采用有限。

**研究缺口**：现有 TTS 系统缺乏统一的框架来消除预训练数据与后训练目标之间的分布偏移，且缺少针对细粒度指令跟随能力的系统性评估基准。

### 1.3. 研究目标与核心假设/命题 (Objectives & Hypotheses/Propositions)

本文的研究目标是开发 Fish Audio S2，一个开源的、支持细粒度自然语言控制的 TTS 系统。核心命题包括：

1. **双用途数据流水线假设**：将同一模型既用于预训练过滤又用于 RL 奖励，可以消除分布偏移，提高训练效率。
2. **多奖励 RL 对齐假设**：联合优化语义准确性、声学质量和说话人相似度，可以在表达力和鲁棒性之间取得平衡。
3. **Dual-AR 架构假设**：解耦时间语义建模和深度声学建模，可以在保持高质量的同时实现高效推理。

---

## 2. 研究设计与方法 (Methodology)

### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

本研究采用系统构建式研究方法论，包含四个核心阶段：

1. **音频 Tokenizer 训练**：训练离散音频表示模型
2. **大规模预训练与 SFT**：将 LLM 与离散音频表示对齐
3. **基于 RL 的后训练**：通过强化学习优化生成质量
4. **推理引擎优化**：基于 SGLang 构建生产就绪的推理系统

### 2.2. 数据来源与样本 (Data Source & Sample)

预训练阶段使用了超过**1000 万小时**的原始音频数据，覆盖约**80 种语言和方言**。数据经过三阶段流水线处理：

- **阶段 1**：声源分离与分割，使用语音分离模块从背景噪声中提取干净语音，再通过 VAD 将连续音频切片为 utterance 级别片段
- **阶段 2**：质量过滤，语音质量模型从多个维度（信噪比、说话人一致性、录音质量、可懂度）评估每个 utterance
- **阶段 3**：丰富转录，ASR 模型生成高精度转录，同时标注说话人转换和声音特征（如情感、韵律、副语言）

### 2.3. 操作化与测量 (Operationalization & Measurement)

**核心变量定义与测量**：

| 变量 | 定义 | 测量方法 |
|---|---|---|
| **语义准确性 (R_STT)** | 生成语音与目标文本的一致性 | ASR 转录模型提取 per-token 置信度，对说话人 ID 标签和语音指令实施 token 加权掩码惩罚 |
| **声学偏好 (R_Pref)** | 生成语音的声学质量 | 语音质量模型评分 |
| **音色相似度 (R_SIM)** | 生成语音与参考说话人的相似度 | 外部声纹模型提取特征并计算余弦相似度 |
| **可懂度** | 语音内容的可理解程度 | Word Error Rate (WER) / Character Error Rate (CER) |
| **说话人相似度** | 音色一致性 | WavLM-large 提取说话人嵌入并计算余弦相似度 |

**系统架构**：

- **Slow AR**：基于 Qwen3-4B，4B 参数量，沿时间轴自回归生成语义 token
- **Fast AR**：4 层 Transformer，独立权重和嵌入表，沿 codebook 深度轴生成细粒度声学细节
- **音频 Tokenizer**：446M 参数，基于 DAC 架构，10 层 RVQ，2048×下采样，21Hz 帧率

---

## 3. 结果与发现 (Results & Findings)

### 3.1. 主要发现概述 (Overview of Key Findings)

**客观评估结果**：

1. **Seed-TTS-Eval（语音克隆可懂度）**：Fish Audio S2 在中文测试集上 WER 为 0.54%，英文为 0.99%，在困难中文测试集上为 5.99%，均优于或媲美其他开源和闭源模型。

2. **多语言评估（CV3-Eval 和 Minimax Multilingual Testset）**：在 Minimax 多语言测试集的 24 种语言中，Fish Audio S2 在 11 种语言上取得最低 WER，在 17 种语言上取得最高说话人相似度（SIM）。在 CV3-Eval 的 9 语言子集上，平均错误率从 Fish Audio S1 的 3.96 降至 3.01（相对降低 23.9%）。

3. **长音频基准（Long-TTS-Eval）**：在英文和中文长音频生成任务中，Fish Audio S2 均取得最低 WER/CER，证明了其在生成长音频时的鲁棒性。

**LLM-as-a-Judge 评估结果**：

1. **Audio Turing Test**：Fish Audio S2 后验均值为 0.483，指令重写后提升至 0.515，显著超越之前的 SOTA 模型（如 Seed-TTS 的 0.417、MiniMax-Speech 的 0.387）。

2. **EmergentTTS-Eval**：整体胜率为 81.88%，在所有列出的系统中表现最佳。在副语言（91.61%）、疑问句（84.41%）和句法复杂度（83.39%）等指令敏感场景中表现尤为突出。

3. **Fish Audio Instruction Benchmark**：标签激活率（TAR）在中文上为 0.984、英文上为 0.881；自然度评分在中文上为 4.40/5.0、英文上为 4.21/5.0；表达力评分在中文上为 4.94/5.0、英文上为 4.50/5.0。

**推理性能**：

- **RTF（实时因子）**：0.195（生成速度是实时的 5 倍+）
- **TTFA（首音频时间）**：<100ms
- **吞吐量**：高并发下可持续 3000+ 声学 token/秒

### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**表 1：Seed-TTS-Eval 结果**

| 模型 | 中文 WER | 英文 WER | 困难中文 WER |
|---|---|---|---|
| Fish Audio S2 | **0.54** | **0.99** | 5.99 |
| Fish Audio S1 | 0.54 | 1.07 | 17.00 |
| CosyVoice 3-1.5B | 1.12 | 2.21 | **5.83** |

该表显示 Fish Audio S2 在中文和英文语音克隆任务上均取得领先 WER，表明其发音更清晰稳定。困难中文测试集上虽略逊于 CosyVoice 3-1.5B，但相比 S1 的 17.00 有显著提升。

**表 5：Audio Turing Test 后验统计**

| 模型 | 均值 (标准差) | 95% HDI |
|---|---|---|
| Fish Audio S2 (带指令) | **0.515** (0.061) | [0.510, 0.521] |
| Fish Audio S2 | 0.483 (0.068) | [0.477, 0.489] |
| Seed-TTS | 0.417 (0.011) | [0.398, 0.438] |
| GPT-4o | 0.138 (0.011) | [0.118, 0.158] |

该结果表明 Fish Audio S2 在人类不可区分性评估中显著优于其他模型，指令重写可进一步提升 6.6%。这验证了指令跟随能力对提升语音真实性和自然度的关键作用。

**图 5：RL 后训练奖励曲线**

训练奖励曲线显示总奖励 R_total 在收敛前持续上升，证明了多维度奖励设计在整个 RL 后训练阶段提供了稳定一致的训练信号。

---

## 4. 讨论 (Discussion)

### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

Fish Audio S2 的实验结果验证了三个核心设计选择的有效性：

1. **Dual-AR 架构**：通过解耦时间语义建模和深度声学建模，模型能够在保持高质量的同时实现高效推理。RTF 0.195 和 TTFA <100ms 的结果证明了这一架构的生产就绪能力。

2. **双用途数据流水线**：将语音质量模型和丰富转录 ASR 模型既用于预训练过滤又用于 RL 奖励，有效消除了分布偏移。这一设计使得 RL 训练信号与预训练数据分布一致，提高了训练稳定性。

3. **多奖励 RL 对齐**：联合优化语义准确性、声学质量和说话人相似度，使得模型在多个维度上取得平衡。EmergentTTS-Eval 中 81.88% 的整体胜率证明了这一策略的有效性。

### 4.2. 理论贡献 (Theoretical Contributions)

本研究的理论贡献包括：

1. **提出双用途数据流水线范式**：为 TTS 系统的数据 curration 提供了新思路，通过复用同一模型作为过滤器和奖励信号，消除了预训练与后训练之间的分布偏移。

2. **将 RL 对齐方法成功应用于 TTS**：证明了 GRPO 等 RL 方法可以有效提升 TTS 系统的生成质量，特别是对于细粒度指令跟随能力。

3. **提出细粒度指令跟随评估基准**：Fish Audio Instruction Benchmark 填补了 TTS 评估领域的空白，提供了超越传统 WER/MOS 指标的评估维度。

### 4.3. 实践启示 (Practical Implications)

对于实践者，本研究提供了以下指导意义：

1. **开源生态系统**：模型权重、微调代码和 SGLang 推理引擎的开源降低了高质量 TTS 开发的门槛，促进了研究社区的创新。

2. **生产部署参考**：基于 SGLang 的推理引擎展示了如何在生产环境中实现高吞吐量和超低延迟，为实际部署提供了参考架构。

3. **细粒度控制能力**：支持通过自然语言描述实现细粒度声音控制（如情感、韵律、副语言），为有声书、视频配音和聊天机器人等应用提供了新的可能性。

### 4.4. 局限性与未来研究 (Limitations & Future Research)

本研究的局限性包括：

1. **数据多样性有限**：Fish Audio Instruction Benchmark 目前仅包含约 500 条 utterance，数据多样性和声学标签分布存在不平衡。

2. **人 - 模型对齐分析处于早期阶段**：Gemini 3 Pro 作为 LLM-as-a-Judge 与人类判断的一致性仍有提升空间（客观事件检测准确率 76.2%，主观评分相关性中等）。

3. **低资源语言表现**：在某些低资源语言（训练数据少于 1000 小时）上，MiniMax-Speech 和 ElevenLabs 仍保持优势。

未来研究方向：

1. 扩展 Fish Audio Instruction Benchmark 的数据集，提高数据多样性和标签平衡性
2. 改进自动化评估流水线，提高 LLM-as-a-Judge 与人类判断的一致性
3. 探索更高效的 RL 训练方法，进一步降低计算成本
4. 针对低资源语言进行专门的优化和数据增强

---

## 5. 结论 (Conclusion)

Fish Audio S2 是一个支持细粒度自然语言控制、长音频连贯合成和原生多说话人多轮生成的 SOTA TTS 系统。通过 Dual-AR 架构、双用途数据流水线和多奖励 RL 对齐三项核心创新，该系统在开源 TTS 领域树立了新标杆。客观基准和 LLM-as-a-Judge 评估均证明了其在可懂度、说话人相似度、自然度和指令跟随能力上的有效性。研究团队开源了模型权重、微调代码和 SGLang 推理引擎，为下一代 expressive、可控语音合成的研究提供了坚实基础。

---

## 6. 核心参考文献 (Core References)

1. **Anastassiou et al. (2024)**. Seed-TTS: A family of high-quality versatile speech generation models. *arXiv preprint arXiv:2406.02430*.

2. **Du et al. (2025)**. CosyVoice 3: Towards in-the-wild speech generation via scaling-up and post-training. *arXiv preprint arXiv:2505.17589*.

3. **Hu et al. (2026)**. Qwen3-TTS technical report. *arXiv preprint arXiv:2601.15621*.

4. **Shao et al. (2024)**. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. *arXiv preprint arXiv:2402.03300*.

5. **Zheng et al. (2024)**. SGLang: Efficient execution of structured language model programs. *arXiv preprint arXiv:2312.07104*.

---

## Part B: 核心逻辑链与根本价值提炼

### 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | TTS 领域存在两个关键瓶颈：一是大规模生成细粒度自然语言指令（描述声音特征如情感、韵律）难以手动扩展；二是 RL 对齐方法在 TTS 领域的采用有限，且预训练数据与后训练目标之间存在分布偏移。 |
| **切入视角** | 作者提出了"双用途"设计思想：同一模型既用于预训练阶段的过滤/标注，又直接复用为 RL 阶段的奖励信号。这一设计从根源上消除了分布偏移，同时使细粒度语音标注能够自动扩展而无需人工干预。 |
| **关键方法** | 1) Dual-AR 架构：用 4B 参数的 Slow AR 沿时间轴生成语义 token，用 4 层 Fast AR 沿 codebook 深度轴生成细粒度声学细节；2) 多用途数据流水线：语音质量模型 + 丰富转录 ASR 模型双重复用；3) 多奖励 RL 对齐：GRPO 变体联合优化语义准确性、声学质量和说话人相似度。 |
| **核心发现** | Fish Audio S2 在多个维度取得 SOTA：Seed-TTS-Eval 中文 WER 0.54%、英文 0.99%；Audio Turing Test 0.515（指令重写后）；EmergentTTS-Eval 胜率 81.88%；推理 RTF 0.195、TTFA <100ms。证明了双用途设计和多奖励 RL 对齐的有效性。 |

---

### 方法公式化

**可靠工业级 TTS = (Dual-AR 架构 × 双用途数据流水线) × 多奖励 RL 对齐**

展开为：
- **Dual-AR 架构** = (Slow AR 语义规划 + Fast AR 声学细化) ÷ 序列长度膨胀
- **双用途数据流水线** = (语音质量模型 + 丰富转录 ASR) × 2（预训练过滤 + RL 奖励）
- **多奖励 RL 对齐** = (语义准确性 + 声学质量 + 说话人相似度) × GRPO 变体

---

### 最终双重总结

**一句话总结（核心价值）**：Fish Audio S2 通过 Dual-AR 架构解耦语义与声学建模、双用途数据流水线消除分布偏移、多奖励 RL 对齐平衡多维质量，实现了支持细粒度自然语言控制、长音频连贯合成和原生多说话人多轮生成的开源 TTS 系统，在可懂度、自然度和指令跟随能力上均达到 SOTA 水平。

**一句话总结（大白话版）**：这套系统让 AI 说话更像真人——不仅能模仿不同人的声音，还能听懂"用生气的语气说这句话"或"这里笑一下"这样的指令，而且生成速度比实时说话快 5 倍，延迟不到 100 毫秒，开源给大家随便用。
