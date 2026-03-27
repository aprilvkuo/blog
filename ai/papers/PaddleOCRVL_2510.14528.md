---
title: PaddleOCRVL
description: PaddleOCR-VL 双模式研读报告
date: 2026-03-27
arxiv: 2510.14528
category: multimodal
tags: ['scientific', 'optimization', 'vision', 'efficiency', 'multimodal', 'ocr']
outline: [2, 3]
---

::: tip 📄 论文信息
- **arXiv**: [2510.14528](https://arxiv.org/abs/2510.14528)
- **分类**: 多模态
- **标签**: scientific, optimization, vision, efficiency, multimodal, ocr
:::


::: info 📑 目录
本文档包含完整的论文研读报告，包括深度学术速读和技术实现分析两部分。
:::

# PaddleOCR-VL 双模式研读报告

**论文标题**: PaddleOCR-VL: Boosting Multilingual Document Parsing via a 0.9B Ultra-Compact Vision-Language Model

**作者**: Cheng Cui, Ting Sun, Suyin Liang, et al. (PaddlePaddle Team, Baidu Inc.)

**arXiv**: 2510.14528v4 [cs.CV] 25 Nov 2025

**代码**: https://github.com/PaddlePaddle/PaddleOCR

**模型**: https://huggingface.co/PaddlePaddle

---

## Part A: 深度专业学术速读报告

## 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 文档解析是信息检索和数据管理的核心技术，但现有方法存在集成复杂、误差累积、计算开销大等问题。本研究旨在提出一种高性能、资源高效的多模态文档解析方案。 |
| **方法** | 提出两阶段架构：PP-DocLayoutV2 负责布局分析和阅读顺序预测，PaddleOCR-VL-0.9B 负责元素级识别。采用 NaViT-style 动态分辨率视觉编码器 + ERNIE-4.5-0.3B 语言模型，支持 109 种语言。 |
| **结果** | 在 OmniDocBench v1.5 上达到 92.86 的总体得分（SOTA），在 olmOCR-Bench 上达到 80.0 分。推理速度比 MinerU2.5 快 53.1%（页面吞吐量）和 50.9%（token 吞吐量）。 |
| **结论** | PaddleOCR-VL 在页面级和元素级文档解析任务上均达到 SOTA 性能，同时保持最小资源消耗，适合实际部署。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

文档作为信息的核心载体，其复杂性和数量呈指数级增长，使得文档解析 (Document Parsing) 成为不可或缺的关键技术。文档解析的核心目标是实现对文档布局的深度结构和语义理解，具体包括：识别不同的文本块和列、区分公式/表格/图表/图像、确定正确的阅读顺序、检测关键元素（如脚注和图像标题）。

当前文档解析面临的核心挑战在于现代文档的固有复杂性：它们通常结合密集文本、复杂表格或图表、数学表达式、多语言和手写文本，以及多样化的布局结构。

本研究要回答的核心问题 (Research Questions)：
- **RQ1**: 如何在保持高性能的同时，降低文档解析模型的计算开销和资源消耗？
- **RQ2**: 如何克服纯 end-to-end VLM 方法在长序列输出中的幻觉和文本顺序错误问题？
- **RQ3**: 如何构建高质量的训练数据以支持多语言、多类型文档的解析？

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

当前文档解析研究主要遵循两种技术路线：

**路线一：Pipeline 方法**（基于模块化专家模型）
- 代表工作：MinerU [9]、PP-StructureV3 [10]、Marker [45]
- 优势：各模块性能强
- 局限：集成复杂度高、误差累积传播、处理高度复杂文档时存在固有限制

**路线二：End-to-end 方法**（基于多模态大模型）
- 代表工作：MinerU2.5 [2]、Dolphin [3]、POINTS-Reader [4]、olmOCR [12]
- 优势：简化工作流、可实现联合优化
- 局限：面对长或复杂布局时易产生文本顺序错误和幻觉、长序列输出计算开销大、限制实际部署

**研究缺口 (Research Gap)**：
现有方法无法同时满足高性能、低资源消耗和实际可部署性的需求。Pipeline 方法虽然性能强但集成复杂，End-to-end 方法虽然简化了流程但计算开销大且易产生幻觉。因此，需要一种新的架构设计来平衡性能与效率。

### 1.3. 研究目标与核心假设/命题 (Objectives & Hypotheses/Propositions)

**研究目标**：
提出 PaddleOCR-VL，一种基于视觉 - 语言模型的高性能、资源高效文档解析方案，实现：
1. 在多个公开基准上达到 SOTA 性能
2. 显著降低推理延迟和资源消耗
3. 支持 109 种语言的全球化文档处理

**核心命题**：
- **命题 1**: 两阶段架构（布局分析 + 元素识别）优于纯 end-to-end 方法，能够避免长序列自回归过程中的高延迟和幻觉问题
- **命题 2**: NaViT-style 动态分辨率视觉编码器 + 轻量级语言模型的组合能够在保持高精度的同时显著降低计算需求
- **命题 3**: 系统化的数据构建方法（自动标注 + 困难样本挖掘 + 数据合成）能够为高效鲁棒的文档解析提供坚实的训练数据基础

---

## 2. 研究设计与方法 (Methodology)

### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

本研究采用**系统构建式研究**方法，包含三个核心组成部分：

1. **架构设计**：提出两阶段文档解析架构，将复杂任务分解为布局分析和元素识别两个子任务
2. **数据构建**：开发系统化的训练数据构建 pipeline，包括自动标注、困难样本挖掘和数据合成
3. **实验验证**：在多个公开基准和内部基准上进行全面评估，对比现有 SOTA 方法

### 2.2. 数据来源与样本 (Data Source & Sample)

**训练数据规模**：超过 3000 万训练样本

**数据来源**（四个主要来源）：

1. **开源数据集**：
   - 文本：CASIA-HWDB [29]
   - 公式：UniMER-1M [30]、MathWriting [31]
   - 图表：ChartQA [32]、PlotQA [33]、Chart2Text [34]、DVQA [35]、Unichart [36]、Beagle [37]、ChartINFO [38]、visText [39]、ExcelChart [40]

2. **数据合成**：针对公共数据分布不均衡问题，采用数据合成策略低成本生成缺失数据类型

3. **网络可访问数据**：从互联网收集大量公开文档，包括学术论文、报纸、科学期刊、扫描手写文档、试卷、幻灯片等

4. **内部数据集**：百度多年 OCR 研究积累的多样化数据集

**评估数据集**：
- OmniDocBench v1.0/v1.5 [16]
- olmOCR-Bench [12]
- In-house-OCR（109 种语言，107,452 样本）
- Ocean-OCR-Handwritten（400 样本）
- In-house-Table（20 种表格类型）
- In-house-Formula（34,816 样本）
- In-house-Chart（1,801 样本，11 种图表类型）

### 2.3. 操作化与测量 (Operationalization & Measurement)

**架构组件**：

1. **PP-DocLayoutV2（布局分析模型）**：
   - RT-DETR [17] 用于元素定位和分类
   - Pointer Network [18]（6 层 transformer）用于阅读顺序预测
   - 采用两阶段训练策略：先训练 RT-DETR，冻结参数后独立训练 pointer network

2. **PaddleOCR-VL-0.9B（元素识别模型）**：
   - 视觉编码器：NaViT-style [15] 动态分辨率编码器（初始化自 Keye-VL [22]）
   - 投影层：2 层 MLP（随机初始化，GELU 激活，merge size=2）
   - 语言模型：ERNIE-4.5-0.3B [5]（开源轻量级模型）
   - 位置编码：3D-RoPE [24]

**训练设置**（表 1）：

| 阶段 | 训练样本 | 最大分辨率 | 序列长度 | 可训练组件 | 批次大小 | 最大学习率 | 最小学习率 | 轮次 |
|---|---|---|---|---|---|---|---|---|
| Stage 1 | 29M | 1280×28×28 | 16384 | 全部 | 128 | 5×10⁻⁵ | 5×10⁻⁶ | 1 |
| Stage 2 | 2.7M | 2048×28×28 | 16384 | 全部 | 128 | 5×10⁻⁶ | 5×10⁻⁷ | 2 |

**评估指标**：
- 文本识别：Edit Distance（编辑距离）
- 表格识别：TEDS [41]（Table Edit Distance Similarity）
- 公式识别：CDM [64]（Character Detection Matching）
- 图表识别：RMS-F1 [42]
- 阅读顺序：Reading Order Edit Distance
- 推理性能：Pages/s、Tokens/s、VRAM 使用量

---

## 3. 结果与发现 (Results & Findings)

### 3.1. 主要发现概述 (Overview of Key Findings)

**发现 1：PaddleOCR-VL 在页面级文档解析上达到 SOTA 性能**

在 OmniDocBench v1.5 基准上（表 2）：
- 总体得分：92.86（超越次优模型 MinerU2.5-1.2B 的 90.67）
- Text-Edit 距离：0.035（最低）
- Formula-CDM 得分：91.22（最高）
- Table-TEDS：90.89（最高）
- Reading Order Edit：0.043（最低）

在 OmniDocBench v1.0 基准上（表 3）：
- 平均总体编辑距离：0.115（最优）
- 中文表格 TEDS：92.14（最优）
- 中文阅读顺序编辑距离：0.063（最优）

在 olmOCR-Bench 基准上（表 4）：
- 总体得分：80.0 ± 1.0（最高）
- ArXiv 类别：85.7（最高）
- Headers and Footers：97.0（最高）

**发现 2：PaddleOCR-VL 在元素级识别任务上表现优异**

文本识别（表 5、6、7）：
- 在 OmniDocBench-OCR-block 的 9 种文档类型中，PaddleOCR-VL 在全部类型上达到最低编辑距离
- 在 109 种语言的 In-house-OCR 评估中，所有语言的编辑距离均为最低
- 在手写识别（Ocean-OCR-Bench）上，英文编辑距离 0.118、中文 0.034，均为 SOTA

表格识别（表 8、9）：
- OmniDocBench-Table-block：总体 TEDS 0.9195（最高）
- In-house-Table：总体 TEDS 0.8699（最高）

公式识别（表 10、11）：
- OmniDocBench-Formula-block：CDM 0.9453（SOTA）
- In-house-Formula：CDM 0.9882（最高）

图表识别（表 12）：
- In-house-Chart：RMS-F1 0.8440（超越 72B 级别多模态大模型）

**发现 3：PaddleOCR-VL 具有卓越的推理效率**

在 A100 GPU 上的端到端推理性能（表 13）：
- FastDeploy 后端：1.6184 pages/s、2486.4 tokens/s
- 页面吞吐量比 MinerU2.5 高 53.1%
- Token 吞吐量比 MinerU2.5 高 50.9%

在不同硬件配置上的稳定表现（表 A2）：
- H800：2.2250 pages/s、3416.7 tokens/s
- RTX 4090D：1.1507 pages/s、1768.1 tokens/s
- RTX 3060：0.3641 pages/s、559.5 tokens/s（仍保持可用性）

### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**图 1：OmniDocBench v1.0/v1.5 性能对比**
- 展示了 PaddleOCR-VL 相对于其他方法的性能优势
- 在两个版本基准上均达到 SOTA

**图 2：PaddleOCR-VL 整体架构**
- 清晰展示两阶段流程：布局分析 → 元素分割 → 元素识别 → 后处理
- 体现了任务分解的设计思想

**图 4：PaddleOCR-VL-0.9B 架构**
- 展示了 NaViT 视觉编码器 + MLP 投影 + ERNIE-4.5-0.3B 的组合
- 说明了动态分辨率处理机制

**表 2：OmniDocBench v1.5 综合评估**
- 关键数据：PaddleOCR-VL 总体得分 92.86，比次优的 MinerU2.5-1.2B（90.67）高 2.19 分
- 揭示了小模型（0.9B）可以在特定任务上超越大模型（如 Qwen2.5-VL-72B 的 87.02 分）

**表 13：端到端推理性能对比**
- 关键数据：PaddleOCR-VL (FastDeploy) 总时间 605.6 秒，比 MinerU2.5 的 927.3 秒快 34.7%
- 揭示了架构优化和推理引擎优化带来的效率提升

---

## 4. 讨论 (Discussion)

### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

**为什么两阶段架构优于纯 end-to-end 方法？**

1. **任务分解降低复杂度**：将文档解析分解为布局分析和元素识别两个子任务，每个子任务可以独立优化
2. **避免长序列自回归问题**：布局分析模型输出坐标和类别，而非长序列文本，避免了 VLM 在长序列生成中的幻觉和顺序错误
3. **灵活性和可扩展性**：两阶段架构更容易扩展新的布局类别，无需重新训练整个模型

**为什么 0.9B 小模型能超越 72B 大模型？**

1. **任务特定优化**：PaddleOCR-VL 专为文档解析任务设计，而非通用多模态任务
2. **动态分辨率处理**：NaViT-style 编码器支持任意分辨率输入，无需失真缩放
3. **高质量训练数据**：3000 万 + 高质量样本，覆盖 109 种语言和多种文档类型
4. **两阶段训练策略**：先对齐预训练，再指令微调，确保模型充分学习任务特定知识

### 4.2. 理论贡献 (Theoretical Contributions)

1. **验证了两阶段架构在文档解析任务上的有效性**：证明了任务分解可以避免纯 end-to-end 方法的固有问题
2. **提出了资源高效 VLM 设计范式**：展示了在特定任务上，小模型 + 高质量数据 + 架构优化可以超越大模型
3. **建立了系统化数据构建方法论**：为多模态模型训练数据构建提供了可复用的框架

### 4.3. 实践启示 (Practical Implications)

**对工程师的启示**：
1. 在实际部署中，应优先考虑任务特定的小模型，而非通用大模型
2. 两阶段架构更适合生产环境，具有更好的可控性和可维护性
3. FastDeploy 等专用推理引擎可以显著提升性能

**对研究者的启示**：
1. 数据质量比数据数量更重要，系统化数据构建方法值得深入研究
2. 动态分辨率处理是处理文档图像的关键技术
3. 困难样本挖掘是提升模型鲁棒性的有效手段

**对企业的启示**：
1. PaddleOCR-VL 适合资源受限环境部署，降低基础设施成本
2. 支持 109 种语言，适合全球化业务场景
3. 可显著提升 RAG 系统性能，改善信息检索质量

### 4.4. 局限性与未来研究 (Limitations & Future Research)

**局限性**：
1. **评估数据偏差**：部分基准（如 OmniDocBench v1.0）存在标注错误，可能影响评估准确性
2. **图表识别评估受限**：由于数据集规模限制和标注质量问题，图表识别仅在内部基准上评估
3. **依赖专家模型**：自动标注流程依赖 PP-StructureV3 等专家模型，可能继承其偏差

**未来研究方向**：
1. **端到端优化**：探索在保持两阶段优势的同时，实现更紧密的联合优化
2. **更大规模多语言支持**：扩展至更多语言，特别是低资源语言
3. **实时交互能力**：支持用户反馈和在线学习，持续提升性能
4. **多模态融合**：结合音频、视频等多模态信息，实现更丰富的文档理解

---

## 5. 结论 (Conclusion)

本研究提出了 PaddleOCR-VL，一种先进的资源高效文档解析模型。其核心组件 PaddleOCR-VL-0.9B 采用 NaViT-style 视觉编码器和 ERNIE-4.5-0.3B 语言模型，能够准确识别文本、表格、公式和图表等复杂元素，支持 109 种语言。

通过全面评估，PaddleOCR-VL 在多个公开基准上达到 SOTA 性能，同时保持快速推理和低资源消耗，适合实际部署。其两阶段架构设计、系统化数据构建方法和资源高效优化策略，为多模态文档处理技术的发展提供了重要参考。

PaddleOCR-VL 的广泛应用将显著提升 RAG 系统性能，使从复杂文档中提取信息更加高效，为未来 AI 应用提供更可靠的数据支持。

---

## 6. 核心参考文献 (Core References)

1. **MinerU2.5**: Junbo Niu, et al. "Mineru2.5: A decoupled vision-language model for efficient high-resolution document parsing." arXiv preprint arXiv:2509.22186, 2025.

2. **Qwen2.5-VL**: Shuai Bai, et al. "Qwen2.5-VL Technical Report." arXiv preprint arXiv:2502.13923, 2025.

3. **NaViT**: Mostafa Dehghani, et al. "Patch n'pack: Navit, a vision transformer for any aspect ratio and resolution." NeurIPS 36, 2023.

4. **OmniDocBench**: Linke Ouyang, et al. "Omnidocbench: Benchmarking diverse pdf document parsing with comprehensive annotations." CVPR 2025.

5. **ERNIE 4.5**: Baidu-ERNIE-Team. "Ernie 4.5 Technical Report." 2025.

---

## Part B: 核心逻辑链与根本价值提炼

## 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | 现有文档解析方法面临两难困境：Pipeline 方法性能强但集成复杂、误差累积；End-to-end VLM 方法简化流程但计算开销大、易产生幻觉。如何在保持高性能的同时实现资源高效和实际可部署？ |
| **切入视角** | 将文档解析任务分解为两个独立阶段：布局分析（定位 + 阅读顺序）和元素识别。布局分析用专用轻量模型处理，避免 VLM 长序列生成的固有问题；元素识别用紧凑 VLM 处理，专注内容理解。两阶段各司其职，互不干扰。 |
| **关键方法** | (1) PP-DocLayoutV2：RT-DETR + Pointer Network，负责布局检测和阅读顺序预测；(2) PaddleOCR-VL-0.9B：NaViT 动态分辨率视觉编码器 + ERNIE-4.5-0.3B 轻量语言模型；(3) 系统化数据构建：自动标注 + 困难样本挖掘 + 数据合成，构建 3000 万 + 高质量样本。 |
| **核心发现** | 在 OmniDocBench v1.5 上达到 92.86 分（SOTA），超越 MinerU2.5-1.2B 的 90.67 分和 Qwen2.5-VL-72B 的 87.02 分。推理速度比 MinerU2.5 快 53.1%，支持 109 种语言。证明了 0.9B 小模型在特定任务上可以超越 72B 大模型。 |

---

## 方法公式化

**可靠文档解析 = (两阶段任务分解 × 动态分辨率视觉编码) + (轻量语言模型 + 高质量数据构建)**

或者更具体地：

**PaddleOCR-VL = (PP-DocLayoutV2[布局 + 顺序] → PaddleOCR-VL-0.9B[元素识别]) × 30M 高质量数据**

---

## 最终双重总结

**一句话总结（核心价值）**：PaddleOCR-VL 通过将文档解析分解为布局分析和元素识别两个阶段，结合 NaViT 动态分辨率视觉编码器和 ERNIE-4.5-0.3B 轻量语言模型，在保持 0.9B 超紧凑参数量的同时，在多个基准上达到 SOTA 性能，推理速度比现有最优方法快 53.1%，支持 109 种语言，为资源受限环境下的多模态文档解析提供了实用解决方案。

**一句话总结（大白话版）**：就像把"看懂一页纸"这件事拆成两步——先用小模型快速找出页面上的文字块、表格、图片都在哪、应该按什么顺序读，再用一个专门训练过的小模型逐个识别这些内容，这样既快又准，还省资源，比那些试图一步到位的大模型更靠谱。
