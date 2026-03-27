---
title: MinerU2.5
description: MinerU2.5: 解耦视觉 - 语言模型用于高效高分辨率文档解析 双模式研读报告
date: 2026-03-27
arxiv: 2509.22186
category: framework
tags: ['scientific', 'optimization', 'llm', 'framework', 'vision', 'efficiency', 'ocr', 'rag']
outline: [2, 3]
---

::: tip 📄 论文信息
- **arXiv**: [2509.22186](https://arxiv.org/abs/2509.22186)
- **分类**: 工具/框架
- **标签**: scientific, optimization, llm, framework, vision, efficiency, ocr, rag
:::


::: info 📑 目录
本文档包含完整的论文研读报告，包括深度学术速读和技术实现分析两部分。
:::

# MinerU2.5: 解耦视觉 - 语言模型用于高效高分辨率文档解析 双模式研读报告

---

## Part A: 深度专业学术速读报告

## 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 文档解析是多模态理解的基础任务，支撑信息抽取、RAG 和智能文档分析等应用。现有方法（pipeline 式和端到端 VLM）面临高分辨率处理效率低、token 冗余严重、幻觉问题等挑战。本研究旨在开发一个既能保持 SOTA 识别精度，又能维持卓越计算效率的文档解析模型。 |
| **方法** | 提出 MinerU2.5，一个 1.2B 参数的文档解析视觉 - 语言模型。采用 coarse-to-fine 两阶段解析策略：Stage I 在 downscaled 图像（1036×1036）上进行全局布局分析，Stage II 基于布局结果对 native-resolution crops 进行细粒度内容识别。配套开发系统化数据引擎，支持大规模高质量训练数据生成。 |
| **结果** | 在 OmniDocBench 等多个基准上达到 SOTA。整体性能超越 Gemini-2.5 Pro、Qwen2.5-VL-72B、GPT-4o 等通用 VLM，以及 MonkeyOCR-pro-3B、dots.ocr 等领域专用模型。推理吞吐量达 2.12 pages/s（A100），是 MonkeyOCR-pro-3B 的 4 倍、dots.ocr 的 7 倍。表格识别（TEDS）7 个基准中 5 个 SOTA，公式识别（CDM）7 个基准中 4 个 SOTA。 |
| **结论** | MinerU2.5 通过解耦架构成功解决了文档解析中性能与效率的权衡问题。其核心价值不仅在于 standalone 能力，更在于作为 LLM 时代的基础工具，能够高效将非结构化文档转化为结构化数据，支持高质量预训练语料构建和 RAG 系统增强。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

文档解析（Document Parsing）作为多模态理解领域的基础任务，在信息抽取、检索增强生成（RAG）和智能文档分析等下游应用中扮演着关键角色。与自然图像相比，文档图像具有三个显著特征：显著更高的分辨率、更密集的内容和更复杂的结构布局。这些固有属性带来了一系列独特挑战。

首先，高分辨率和细粒度布局结构要求模型能够以原生分辨率处理图像，以保留精细细节。其次，文档的文本密集性和长度特性对模型的参数效率和鲁棒性提出了严苛要求。第三，OCR 的成功不仅依赖于精确的文本识别，还 heavily 依赖于可靠的布局分析和高效推理。

现有文档解析方法可分为两大范式：基于 pipeline 的方法和基于 VLM 的端到端方法。Pipeline 方法采用模块化设计，将任务分解为布局检测、阅读顺序预测、文本行/公式/表格识别等离散阶段，每个阶段由专用模型处理。这种方法虽然具有可解释性，但存在工作流繁琐和跨模块错误传播的问题。端到端 VLM 方法展现出更优的语义建模能力，但在长文档处理中受限于幻觉问题，且在处理高分辨率输入时面临严重的效率瓶颈。

**核心研究问题**：如何在保持 SOTA 识别精度的同时，显著提升文档解析的计算效率，有效解决 VLM 处理高分辨率文档时的 token 冗余问题？

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

**传统 Pipeline 方法**：早期 OCR 系统如 PaddleOCR、Marker、MinerU 等采用模块化 pipeline 架构，依次执行布局检测、文本识别和阅读顺序预测。例如，Marker 集成了 Surya OCR 与布局分析和阅读顺序预测模块；MinerU 利用 PDF-Extract-Kit 协调多个专用模型。这种架构允许对各组件进行专业化优化，但存在跨阶段错误传播风险，且在处理复杂布局（如多栏文本或跨页结构）时鲁棒性有限。此外，模块间依赖关系使得系统使用、维护和更新变得繁琐。

**通用视觉 - 语言模型**：Gemini-2.5 Pro、Qwen2.5-VL-72B 等通用 VLM 在文档理解任务中展现出潜力。Gemini-2.5 Pro 在文本解析方面超越传统 pipeline 模型，在公式识别方面接近专用系统 UniMERNet。Qwen2.5-VL-72B 采用原生分辨率视觉编码器，适应不同图像尺寸。然而，专有模型成本高、处理速度慢，开源模型需要大规模参数才能达到最优性能，限制了实际部署。两者在密集文本区域仍易受幻觉问题影响。

**领域专用 VLM**：GOT、Ocean-OCR、olmOCR、dots.ocr 等采用端到端架构，将文档解析统一在单个模型中。GOT 作为早期代表，开创了 OCR 2.0 范式，在单一框架内统一了文本、公式、表格和图表的识别。后续模型利用原生分辨率视觉编码器进一步提升性能。然而，端到端设计面临可扩展性挑战：布局与内容的联合优化常降低复杂文档的准确性，而原生分辨率处理引入 prohibitive 的 O(N²) 复杂度。

**多阶段方法**：Dolphin 和 MonkeyOCR 等最近工作尝试解耦布局分析与内容识别。Dolphin 采用 Swin-Transformer VLM 先进行页面级布局分析，然后并行解析识别区域，但固定分辨率严重限制了 crop 解析质量。MonkeyOCR 采用类似策略但使用原生分辨率视觉编码器，改进了性能和效率，但需要多个专用模型，增加了系统复杂性和部署开销。

**研究缺口**：现有方法未能同时解决以下问题：(1) 高分辨率处理的效率瓶颈；(2) token 冗余导致的计算浪费；(3) 单一统一模型与多阶段策略的权衡；(4) 数据多样性不足和标注质量不一致。MinerU2.5 的目标正是填补这一缺口，提出一个统一模型，通过解耦架构实现高效原生分辨率解析。

### 1.3. 研究目标与核心假设/命题 (Objectives & Hypotheses/Propositions)

**研究目标**：
1. 开发一个轻量级（~1.2B 参数）文档解析 VLM，在多个基准上达到 SOTA 性能
2. 通过解耦架构显著降低计算成本，避免 O(N²) 复杂度的视觉 token 冗余
3. 构建系统化数据引擎，生成大规模、多样化、高质量训练数据
4. 提升模型在复杂场景（旋转表格、无边界表格、混合语言公式等）中的鲁棒性

**核心命题**：
- **P1**: 解耦的两阶段策略（全局布局分析 + 局部内容识别）能够在保持高精度的同时，将计算成本降低一个数量级
- **P2**: 通过 thumbnail 进行布局分析（1036×1036）足以捕捉全局结构组织，同时控制计算成本
- **P3**: 基于布局引导的 native-resolution crops 识别能够保留细粒度细节，避免 downsampling 导致的信息损失
- **P4**: 系统化数据引擎（特别是 IMIC 策略）能够有效识别和标注困难样本，显著提升模型在挑战性场景中的性能

---

## 2. 研究设计与方法 (Methodology)

### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

MinerU2.5 采用**系统构建式研究**范式，结合模型架构创新、训练策略设计和数据工程三个维度：

**架构设计**：受 Qwen2-VL 框架启发，采用三组件架构：
- **Vision Encoder**: 675M 参数 NaViT，支持动态图像分辨率，使用 2D-RoPE 进行位置编码
- **LM Decoder**: 0.5B 参数 Qwen2-Instruct，文档解析任务对大语言模型依赖较低
- **Patch Merger**: 对相邻 2×2 视觉 token 进行 pixel-unshuffle，平衡效率与性能

**关键设计选择**：
- 用 M-RoPE 替换原始 1D-RoPE，增强对不同分辨率和长宽比的泛化能力
- 避免 Qwen2.5-VL 的 window attention 设计，因其在文档解析任务中导致性能下降
- 采用 NaViT 而非 Swin-Transformer，支持真正的动态分辨率处理

### 2.2. 数据来源与样本 (Data Source & Sample)

**数据引擎整体流程**：

1. **数据精选 (Data Curation)**：
   - 来源：大规模内部文档池（公开网络数据 + 商业采购文档）
   - 挑战：原始数据存在显著的长尾分布
   - 解决方案：多维度平衡策略
     - 布局多样性：页面级图像聚类，选择多样化视觉布局和风格代表
     - 文档类型多样性：基于元数据（学科、标签）分层采样，涵盖学术论文、教科书、报告、演示文稿等
     - 元素平衡：使用初步检测模型确保标题、段落、表格、公式、图像等关键元素的类别分布平衡
     - 语言平衡：过滤数据以保持中英文档可比体积

2. **预训练数据集准备 (Pre-training Dataset Preparation)**：
   - 初始标注：使用 MinerU2-pipeline 生成基线标注
   - 质量提升：使用专用专家模型进行多步优化
     - 文本内容：使用 Qwen2.5-VL-72B-Instruct 验证和校正裁剪文本区域的识别结果
     - 公式内容：使用内部重新训练的 UniMERNet 模型替换识别的公式，提升保真度
     - 表格内容：使用内部高性能表格解析模型重新生成所有表格结构
   - 最终规模：6.9M 样本（布局分析 2.3M，文本块 2.4M，公式块 1.1M，表格块 1.1M）

3. **微调数据集构建 (Fine-tuning Dataset Construction)**：
   - 核心创新：**Iterative Mining via Inference Consistency (IMIC)**
   - 流程：
     - 从大规模数据池中自动过滤困难样本
     - 使用基础模型（如 Gemini-2.5-Pro 处理复杂表格）进行预标注
     - 人工专家细致审核和校正
     - 结合高质量困难案例和小部分随机采样的常规样本
   - 最终规模：630K 样本（布局分析 43K，文本块 300K，公式块 147K，表格块 140K）

### 2.3. 操作化与测量 (Operationalization & Measurement)

**两阶段解析策略**：

**Stage I - 布局分析**：
- 输入：统一 resize 到 1036×1036 像素的 thumbnail
- 输出：每个文档元素的四个属性
  - Position: 边界框坐标
  - Class: 元素类别（统一标签系统）
  - Rotation Angle: 旋转角度
  - Reading Order: 阅读顺序
- 提示词："Layout Detection:"
- 参数选择依据：thumbnail 尺寸需平衡全局可见性和效率——太小导致细节丢失，太大触发 NaViT 的二次复杂度

**Stage II - 内容识别**：
- 输入：基于检测布局从原始高分辨率图像裁剪的局部区域
- 分辨率上限：2048×28×28 像素，避免过小 crop 导致细节丢失，同时防止过大 crop 的冗余计算
- 任务类型：
  - Text Recognition: 文本块识别
  - Formula Recognition: 公式识别
  - Table Recognition: 表格识别
- 提示词：见 Appendix B

**任务重构与创新**：

**布局分析**：
- **统一标签系统**：涵盖 17+ 类别，包括常被忽略的非正文元素（header、footer、page number、page footnote）
- **细粒度分类**：如图像细分为 image、chart、chemical structure，各有独立 caption 标签
- **语义区分**：code、algorithm、reference、list 等视觉上不同的文本块分配独立类别
- **PageIoU 新指标**：页面级覆盖率度量，定义为：
  
  PageIoU(P, G) = |Pcover ∩ Gcover| / |Pcover ∪ Gcover| = Σ min(Pcover(p), Gcover(p)) / Σ max(Pcover(p), Gcover(p))
  
  其中 Pcover 和 Gcover 分别为预测和真实标注的覆盖图。相比传统 mAP，PageIoU 更符合人类感知。

**公式识别**：
- **原子 - 复合公式解耦**：
  - Atomic Formulas: 最小、不可分割的语义单元，具有紧密 2D 拓扑（如单个分数、矩阵）
  - Composite Formulas: 由多个原子公式组成的复杂结构
- 检测阶段识别 composite formula，然后进行 atomic decomposition，分别识别每个 atomic formula
- 避免 VLM 将长公式视为单一实体导致的结构性幻觉

**表格识别**：
- 从财报中提取大规模高质量表格数据用于训练
- 支持多种表格类型：旋转表格、无边界表格、部分边界表格、合并单元格表格等

**数据增强策略**：
- 空间变换：Scaling、Grid Distortion、Rotation（不应用于布局分析样本）
- 背景变换：Texture、Weather effect、Image background、Watermark、Scanlines、Shadow
- 颜色变换：Brightness Contrast、Illumination、RGB Shift
- 退化变换：PSF Blur、Vibration Blur、Gaussian Blur、Erosion/Dilation

### 2.4. 模型部署优化

**推理引擎**：基于 vLLM 实现高效离线推理 pipeline

**关键优化**：
1. **异步后端**：处理页面级请求的批处理提交，实现 CPU 和 GPU 工作负载更好重叠
2. **解耦推理任务**：将 Stage I 和 Stage II 作为独立推理任务，允许下游处理在单个结果可用时立即开始，而非等待整个批次
3. **动态采样参数调整**：基于 Stage I 检测的布局类型，动态调整 Stage II 的 frequency penalty 和 presence penalty
   - 文本段落：较高 penalty 抑制退化 token 重复
   - 表格内容：较低 penalty 保留合法重复结构（如表格、方程）
4. **vLLM 调度参数调优**：max_num_batched_tokens、max_num_seqs、cuda graph sizes

---

## 3. 结果与发现 (Results & Findings)

### 3.1. 主要发现概述 (Overview of Key Findings)

**整体性能突破**：
MinerU2.5 在 OmniDocBench 基准上展现了全面领先性能。在整体性能指标上，MinerU2.5 超越了所有对比模型，包括通用 VLM（Gemini-2.5 Pro、Qwen2.5-VL-72B、GPT-4o、InternVL3.5-241B）和领域专用模型（MonkeyOCR-pro-3B、dots.ocr、PP-StructureV3、Nanonets-OCR-s）。这证明了轻量级专用模型通过架构创新可以达到甚至超越大规模通用模型的性能。

**效率优势显著**：
在推理效率方面，MinerU2.5 展现了数量级的优势。在 A100 80G GPU 上，MinerU2.5 达到 2.12 pages/s 的吞吐量，是 MonkeyOCR-pro-3B（0.47 pages/s）的 4.5 倍，是 dots.ocr（0.28 pages/s）的 7.6 倍。端到端生成速度（仅计算 Stage II 的有效输出 token）达到 2337.25 tokens/s。值得注意的是，即使没有任何部署优化，MinerU2.5 的基线吞吐量（0.95 pages/s，1045.14 tokens/s）也已超越其他模型的默认配置。

**任务特异性表现**：

**布局分析**：在 PageIoU 指标下，MinerU2.5 在多个基准上达到 SOTA。统一标签系统确保了全面的元素覆盖，包括 header、footer、page number 等非正文元素，这对 RAG 等下游应用至关重要。增强多任务范式（同时预测位置、类别、旋转角度、阅读顺序）有效解决了旋转元素解析挑战，并简化了整个文档分析 pipeline。

**表格识别**：在 TEDS 指标评估下，MinerU2.5 在 7 个基准中 5 个达到 SOTA，1 个第二。特别是在 CC-OCR 和 In-house TR Benchmark 上，MinerU2.5 展现了与 Gemini-2.5 Pro 相当甚至略优的性能。这一突破主要归功于从财报中提取的大规模高质量表格训练数据。

**公式识别**：在 CDM 指标评估下，MinerU2.5 在 7 个基准中 4 个达到 SOTA，1 个第二。在公共数据集上，MinerU2.5 在 SCE（简单印刷公式）上达到 96.4 CDM，在 LaTeX-80M M（矩阵基准）上达到 90.6 CDM，展现了在模糊截图和复杂矩阵场景中的领先性能。在内部评估数据集上，MinerU2.5 在中文文本识别方面与 Qwen2.5-VL-72B 持平（90.6 CDM），在真实数学文档（Fuzzy Math）和极难公式识别（Complex）上达到最佳结果。

### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**Figure 1 - 性能亮点**：
该图展示了 MinerU2.5 在 OmniDocBench 上的性能对比。整体性能（Overall Performance）条形图中，MinerU2.5 明显高于所有对比模型。元素级性能（Element-wise Performance）分为四个子任务：
- Text Block (1-Edit): MinerU2.5 接近 100 分，显著高于其他模型
- Formula (CDM): MinerU2.5 达到约 95 分，略高于 Gemini-2.5 Pro
- Table (TEDS): MinerU2.5 达到约 95 分，显著高于其他专用模型
- Reading Order (1-Edit): MinerU2.5 接近满分

这证明了 MinerU2.5 在各子任务上的全面领先能力。

**Figure 2 - 模型框架**：
该图直观展示了两阶段解析策略。Stage I 中，原始文档图像（2640×3320 像素）被 resize 为 thumbnail（1036×1036），进行布局检测，输出每个元素的类型、边界框、旋转角度和阅读顺序。Stage II 中，基于布局结果从原始高分辨率图像裁剪关键区域（Crop 1、Crop 2、...、Crop 8），每个 crop 以原生分辨率进行细粒度内容识别（文本识别、表格识别、公式识别），最后按阅读顺序合并结果。这一设计清晰揭示了解耦架构如何平衡全局结构理解和局部细节保留。

**Figure 3 - 数据引擎概览**：
该图展示了数据引擎的三阶段流程：(1) 数据精选：基于视觉特征、领域、元素、语言等多维度过滤大规模原始文档池；(2) 预训练数据准备：使用 MinerU2-VLM 进行初步解析，然后使用专用模型（QwenVL、UniMERNet、Self-TabR）分别提升文本、公式、表格结果质量；(3) 微调数据集构建：使用 IMIC 策略自动发现困难案例，经过专家审核和模型预标注生成高质量 SFT 数据集。这一 virtuous cycle 是 MinerU2.5 性能突破的关键支撑。

**Figure 4 - PageIoU 指标说明**：
该图通过两个案例对比了传统 IoU-based recall 和 PageIoU 的差异。Case 1 中，粗糙覆盖整个段落的预测获得完美的 Recall@IoU0.5 = 1.0，但视觉上并不精确；Case 2 中，逐行精确预测因不匹配段落级 ground truth 而获得较低的 Recall@IoU0.5 = 0.6，但视觉上明显更优。PageIoU 通过页面级覆盖率度量，给 Case 1 评分 0.78，给 Case 2 评分 0.97，与人类感知高度一致。这一新指标解决了文档布局分析中边界模糊导致的评估偏差问题。

**Table 3 - 推理性能对比**：
该表对比了不同模型在不同后端和 GPU 上的推理性能。关键发现：
- MinerU2.5 在 A100 80G 上达到 2337.25 tokens/s 和 2.12 pages/s
- 在 H200 141G 上进一步提升至 4938.31 tokens/s 和 4.47 pages/s
- 相比之下，MonkeyOCR-pro-3B 仅 520.16 tokens/s 和 0.47 pages/s
- dots.ocr 仅 311.06 tokens/s 和 0.28 pages/s

这证明了 MinerU2.5 的架构效率优势，即使参数量（1.2B）小于 MonkeyOCR-pro-3B（3.7B），吞吐量却高出 4 倍以上。

---

## 4. 讨论 (Discussion)

### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

MinerU2.5 的成功验证了核心研究命题：**解耦架构能够有效解决文档解析中性能与效率的权衡问题**。

**为什么解耦策略有效？**

首先，**计算复杂度降低**。端到端原生分辨率方法的视觉 token 数量随图像分辨率呈 O(N²) 增长。对于典型的高分辨率文档页面（如 3000×4000 像素），视觉 token 数量可达数万甚至数十万，导致巨大的计算开销。MinerU2.5 的两阶段策略将问题分解为：(1) 低分辨率 thumbnail 上的全局布局分析（固定 1036×1036，约 1000 个 token）；(2) 多个小 crop 的局部内容识别（每个 crop 上限 2048 像素）。这种设计将总 token 数量降低了一个数量级。

其次，**信息保留优化**。单纯的 downsampling 会丢失细粒度细节，特别是密集文本、复杂公式和精细表格结构。MinerU2.5 通过在 Stage II 使用 native-resolution crops，确保了关键区域的原始分辨率被保留。布局分析阶段仅需捕捉全局结构（元素位置、类型、阅读顺序），这些信息在 thumbnail 分辨率下已足够；内容识别阶段才需要高分辨率细节。这种"按需高分辨率"策略实现了信息保留与计算效率的最佳平衡。

第三，**错误传播缓解**。Pipeline 方法的主要缺陷是跨模块错误传播。MinerU2.5 虽然是两阶段，但两个阶段在单一统一模型内实现，共享视觉编码器和语言解码器的表征学习。此外，布局分析结果直接指导内容识别的 crop 提取和任务类型选择，形成了紧密耦合而非松散的 pipeline 连接。

**为什么轻量级模型能达到 SOTA？**

MinerU2.5 仅 1.2B 参数，远小于 Qwen2.5-VL-72B（72B）和 InternVL3.5-241B（241B），却在多个基准上超越这些大规模模型。这一现象揭示了**专业化 vs 通用化**的权衡：

- 通用 VLM 需要在广泛任务（图像理解、视觉问答、推理等）上保持能力，参数被分散使用
- MinerU2.5 专注于单一任务（文档解析），所有参数都针对该任务优化
- 文档解析任务对语言推理能力要求相对较低，0.5B 的 Qwen2-Instruct 已足够
- 关键能力在于视觉编码（675M NaViT）和视觉 - 语言对齐，而非纯语言能力

这一发现对资源受限场景具有重要实践意义：在特定垂直领域，轻量级专用模型可能比大规模通用模型更具性价比。

### 4.2. 理论贡献 (Theoretical Contributions)

**架构创新贡献**：
1. **Decoupled VLM 范式**：提出了全局布局分析与局部内容识别解耦的 VLM 架构，为高分辨率视觉任务提供了新的设计思路。这一范式可推广到其他需要兼顾全局理解和局部细节的任务，如医学图像分析、遥感图像解译等。

2. **动态分辨率处理**：通过 thumbnail + native-resolution crops 的组合，实现了真正的动态分辨率处理。相比固定分辨率或 window attention 方法，这一设计在保持性能的同时显著提升了效率。

3. **统一标签系统**：提出的层次化、全面覆盖的标签系统（17+ 类别，包括非正文元素）为文档布局分析建立了新标准，有助于推动领域内的标准化和可比性。

**方法论贡献**：
1. **PageIoU 指标**：提出的页面级覆盖率度量解决了传统 IoU-based 指标在文档布局分析中的评估偏差问题，为领域提供了更符合人类感知的评估工具。

2. **IMIC 数据策略**：Iterative Mining via Inference Consistency 通过推理一致性自动挖掘困难样本，结合 AI 辅助标注流程，为高质量训练数据构建提供了可复用的方法论。

3. **原子 - 复合公式解耦**：将公式识别问题重构为"检测 composite formula → 分解为 atomic formulas → 分别识别"的流程，有效缓解了 VLM 的结构性幻觉问题。

**实证贡献**：
在 10+ 公共和内部基准上的系统性评估，建立了文档解析任务的新 SOTA 基准。特别是 OmniDocBench 上的全面对比，为后续研究提供了可靠的参考点。

### 4.3. 实践启示 (Practical Implications)

**对研究者的启示**：
1. **专业化优于通用化**：在资源受限场景，针对特定任务优化的轻量级模型可能比大规模通用模型更具性价比。研究者应考虑任务特异性架构设计，而非盲目追求参数规模。

2. **数据质量 > 数据数量**：IMIC 策略证明，针对性地构建高质量困难样本数据集，比单纯增加数据规模更能提升模型性能。研究者应重视数据工程和困难案例挖掘。

3. **评估指标需匹配任务特性**：PageIoU 的提出表明，传统指标可能不适合新任务。研究者应根据任务特点设计更合适的评估方法。

**对工程师的启示**：
1. **部署优化至关重要**：MinerU2.5 的推理 pipeline 展示了异步处理、动态参数调整、vLLM 调度优化等技术对实际性能的巨大影响。工程师应重视推理优化，而非仅关注模型训练。

2. **统一模型简化部署**：相比需要多个专用模型的 pipeline 方法，MinerU2.5 的单一模型架构显著降低了部署复杂性和维护成本。

3. **硬件适配策略**：MinerU2.5 在不同 GPU（A100、H200、RTX 4090）上的性能数据为实际部署提供了参考。工程师应根据目标硬件选择合适的配置。

**对应用开发者的启示**：
1. **RAG 系统增强**：MinerU2.5 能够高效将非结构化文档转化为结构化 Markdown，保留表格、公式、布局等语义信息，显著提升 RAG 系统的检索质量和生成准确性。

2. **预训练语料构建**：MinerU2.5 可作为基础工具，快速处理海量文档集合，构建高质量预训练语料。这对于大模型预训练和数据闭环构建具有重要价值。

3. **多文档类型支持**：MinerU2.5 在学术论文、教科书、报告、演示文稿、试卷、笔记、报纸、杂志等多种文档类型上的鲁棒性，使其适用于广泛的实际应用场景。

### 4.4. 局限性与未来研究 (Limitations & Future Research)

**局限性**：

1. **极端低质量文档**：论文未充分评估 MinerU2.5 在极端低质量扫描文档（如严重模糊、破损、手写潦草）上的表现。虽然数据增强包含退化变换，但真实世界的极端情况可能超出训练分布。

2. **多语言支持范围**：论文主要关注中英文档，对其他语言（如阿拉伯语、印地语、东南亚语言等）的支持未充分讨论。这些语言的书写系统和布局特性可能带来新挑战。

3. **非拉丁/非汉字脚本**：公式识别主要针对标准数学符号，对特殊领域符号（如化学结构式、电路图、乐谱等）的支持有限。

4. **实时性要求**：虽然 MinerU2.5 效率显著优于对比模型，但在需要亚秒级响应的实时交互场景中，2.12 pages/s 的吞吐量可能仍不足够。

5. **3D 和交互式文档**：论文未涉及 3D 文档、交互式 PDF（含表单、链接、多媒体）等复杂文档类型的解析。

**未来研究方向**：

1. **跨语言泛化**：扩展 MinerU2.5 到更多语言，特别是书写系统和布局特性差异较大的语言。研究多语言联合训练策略和语言自适应机制。

2. **领域自适应**：针对特定垂直领域（如法律文档、医疗记录、专利文献）进行领域自适应，探索 few-shot 或 zero-shot 领域迁移方法。

3. **多模态融合**：将 MinerU2.5 与其他模态（如音频、视频）结合，支持多媒体文档的联合解析和理解。

4. **增量学习**：研究增量学习策略，使 MinerU2.5 能够持续从新数据中学习，适应文档样式和内容的演化。

5. **可解释性增强**：虽然两阶段架构已具有一定可解释性，但可进一步研究可视化注意力机制、错误分析工具等，提升模型决策的透明度。

6. **边缘设备部署**：探索 MinerU2.5 在边缘设备（如移动设备、嵌入式系统）上的部署优化，研究模型压缩、量化、蒸馏等技术。

---

## 5. 结论 (Conclusion)

MinerU2.5 代表了解耦视觉 - 语言模型在文档解析任务上的重大突破。通过创新的 coarse-to-fine 两阶段策略，MinerU2.5 成功解决了高分辨率文档解析中性能与效率的权衡问题：Stage I 在低分辨率 thumbnail 上进行全局布局分析，Stage II 基于布局引导对 native-resolution crops 进行细粒度内容识别。这一设计将计算成本降低了一个数量级，同时保留了关键区域的原始分辨率细节。

配套开发的系统化数据引擎，特别是 IMIC（Iterative Mining via Inference Consistency）策略，通过推理一致性自动挖掘困难样本，结合 AI 辅助标注流程，构建了高质量训练数据集，显著提升了模型在挑战性场景中的鲁棒性。

在实证评估中，MinerU2.5 在 OmniDocBench 等多个基准上达到 SOTA，全面超越了通用 VLM（Gemini-2.5 Pro、Qwen2.5-VL-72B、GPT-4o）和领域专用模型（MonkeyOCR-pro-3B、dots.ocr、PP-StructureV3）。推理效率方面，MinerU2.5 达到 2.12 pages/s（A100），是 MonkeyOCR-pro-3B 的 4 倍、dots.ocr 的 7 倍，展现了卓越的计算效率。

MinerU2.5 的核心价值不仅在于其 standalone 性能，更在于其作为 LLM 时代基础工具的潜力。其高效将非结构化文档转化为结构化数据的能力，对于构建高质量预训练语料和增强 RAG 系统具有重要价值。通过保留表格、公式、布局等语义信息的完整性，MinerU2.5 有望显著提升下一代 AI 应用对复杂文档知识的利用能力。

---

## 6. 核心参考文献 (Core References)

1. **Qwen2-VL**: Peng Wang, Shuai Bai, Sinan Tan, et al. "Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution." arXiv preprint arXiv:2409.12191, 2024.

2. **NaViT**: Mostafa Dehghani, Basil Mustafa, Josip Djolonga, et al. "Patch N'Pack: NaViT, a Vision Transformer for Any Aspect Ratio and Resolution." Advances in Neural Information Processing Systems, 36: 2252–2274, 2023.

3. **MinerU**: Bin Wang, Chao Xu, Xiaomeng Zhao, et al. "MinerU: An Open-Source Solution for Precise Document Content Extraction." arXiv preprint arXiv:2409.18839, 2024.

4. **UniMERNet**: Bin Wang, Zhuangcheng Gu, Guang Liang, et al. "UniMERNet: A Universal Network for Real-World Mathematical Expression Recognition." arXiv preprint arXiv:2404.15254, 2024.

5. **OmniDocBench**: Linke Ouyang, Yuan Qu, Hongbin Zhou, et al. "OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations." Proceedings of the Computer Vision and Pattern Recognition Conference, pages 24838–24848, 2025.

---

## Part B: 核心逻辑链与根本价值提炼

## 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | 文档解析 VLM 面临"高分辨率悖论"：要保持识别精度需要原生分辨率处理，但原生分辨率导致 O(N²) 复杂度的视觉 token 爆炸，计算成本 prohibitive。现有端到端方法要么牺牲精度（downsampling），要么牺牲效率（全图原生分辨率）；pipeline 方法则 suffer 从错误传播和系统复杂性。 |
| **切入视角** | "解耦而非统一"：与其试图用单一 pass 同时处理全局布局和局部细节，不如将问题分解为两个专业化阶段——Stage I 用低分辨率快速捕捉"在哪里有什么"（全局结构），Stage II 用原生分辨率精确识别"具体是什么"（局部内容）。关键洞察是：布局分析不需要高分辨率，内容识别才需要；将高分辨率计算"按需分配"到关键区域，而非浪费在空白或低信息区域。 |
| **关键方法** | **Two-Stage Decoupled Parsing** = (Thumbnail Layout Analysis @ 1036²) + (Native-Res Crop Recognition @ 2048² max)。Stage I 将整页 resize 为固定 thumbnail，预测每个元素的位置、类别、旋转角度、阅读顺序；Stage II 基于布局结果裁剪关键区域，以原生分辨率进行文本/公式/表格识别。配合 IMIC 数据引擎自动挖掘困难样本，针对性提升鲁棒性。 |
| **核心发现** | MinerU2.5（1.2B 参数）在 OmniDocBench 等基准上全面超越 Gemini-2.5 Pro、Qwen2.5-VL-72B（72B）、GPT-4o 等通用 VLM，以及 MonkeyOCR-pro-3B、dots.ocr 等专用模型。推理吞吐量达 2.12 pages/s，是 MonkeyOCR-pro-3B 的 4×、dots.ocr 的 7×。证明轻量级专用模型通过架构创新可达到甚至超越大规模通用模型的性能效率比。 |

---

## 方法公式化

**高效文档解析 = (全局布局分析 @ 低分辨率 + 局部内容识别 @ 原生分辨率) × 按需计算**

更精确地：

**MinerU2.5 = Layout_Thumbnail(1036²) → Crop_Selection → Recognition_NativeRes(2048² max) × IMIC_Data_Engine**

或简化为：

**性能/效率 = (解耦两阶段 + 动态分辨率) / Token 冗余**

---

## 最终双重总结

**一句话总结（核心价值）**：MinerU2.5 通过解耦全局布局分析（低分辨率 thumbnail）与局部内容识别（原生分辨率 crops）的两阶段策略，在保持 SOTA 识别精度的同时将计算成本降低一个数量级，配合 IMIC 数据引擎自动挖掘困难样本，证明了轻量级专用模型（1.2B）可通过架构创新超越大规模通用 VLM（72B+）的性能效率比，成为 LLM 时代文档解析的基础工具。

**一句话总结（大白话版）**：MinerU2.5 就像先看缩略图搞清楚页面上有哪些块（标题、表格、公式等），再放大每个块仔细看具体内容，而不是直接把整张高清图塞给模型——这样既看得准又快，小模型也能干出大模型的效果。
