---
title: LeWorldModel
description: Attention Residuals 双模式研读报告
date: 2026-03-27
arxiv: 2603.19312
---

> 📄 arXiv: [2603.19312](https://arxiv.org/abs/2603.19312)

# Attention Residuals 双模式研读报告

**论文标题**: Attention Residuals (Technical Report)  
**作者**: Kimi Team, Moonshot AI  
**arXiv**: 2603.15031v1 [cs.CL]  
**日期**: 2026 年 3 月 16 日  
**代码**: https://github.com/MoonshotAI/Attention-Residuals

---

## Part A: 深度专业学术速读报告

## 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 现代大语言模型 (LLM) 普遍采用 PreNorm 残差连接，但其固定单位权重累加导致隐藏状态幅度随深度 O(L) 增长，逐层稀释各层贡献。本研究旨在解决这一"PreNorm 稀释"问题，提出一种能够选择性聚合深度方向信息的机制。 |
| **方法** | 提出 Attention Residuals (AttnRes)，用 softmax 注意力替代固定残差累加，每层使用学习到的、输入依赖的权重选择性聚合先前层输出。为降低大规模训练开销，进一步提出 Block AttnRes，将层分组为块，在块级别表示上进行注意力，将内存和通信从 O(Ld) 降至 O(Nd)。 |
| **结果** | Scaling Law 实验表明，Block AttnRes 在相同计算量下 consistently 优于基线，等效于 1.25×计算优势。在 48B 参数 Kimi Linear 架构上预训练 1.4T tokens，所有下游任务均有提升，尤其是多步推理任务 (GPQA-Diamond +7.5 分，Math +3.6 分，HumanEval +3.1 分)。训练开销<4%，推理延迟开销<2%。 |
| **结论** | AttnRes 通过深度方向的 softmax 注意力实现了选择性信息聚合，缓解了 PreNorm 稀释问题，使输出幅度有界、梯度分布更均匀。Block AttnRes 以约 8 个块即可恢复大部分 Full AttnRes 收益，是实际可用的即插即用替换方案。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

残差连接 (Residual Connections) 自 He et al. (2015) 提出以来，已成为现代深度神经网络的标准构建模块。在 Transformer 架构中，残差更新公式 h_l = h_{l-1} + f_{l-1}(h_{l-1}) 被广泛理解为"梯度高速公路"，允许梯度通过恒等映射绕过非线性变换，从而实现深层网络的稳定训练。

然而，残差连接还扮演着第二个较少被关注的角色：展开递归可知，每一层接收的是所有先前层输出的均匀加权和。这意味着残差连接定义了**深度方向的信息聚合方式**。与序列混合 (sequence mixing) 和专家路由 (expert routing) 已采用可学习的输入依赖权重不同，深度方向的聚合仍由固定单位权重控制，缺乏选择性强调或抑制单个层贡献的机制。

在实践中，PreNorm (Xiong et al., 2020) 已成为主导范式，但其无权重累加导致隐藏状态幅度随深度 O(L) 增长，逐层稀释每层的相对贡献。早期层信息被埋没且无法选择性检索；经验上，相当一部分层可以被剪枝而损失很小 (Gromov et al., 2025)。

**核心研究问题 (RQs)**:
1. 能否设计一种机制，使每层能够选择性聚合所有先前层的输出，而非固定单位权重累加？
2. 这种机制能否在大规模训练中保持效率，成为实际可用的残差连接替代方案？
3. 选择性深度聚合能否改善训练动态和下游任务性能？

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

**残差连接的演进**:
- **标准残差** (He et al., 2015): 固定单位权重累加
- **Highway Networks** (Srivastava et al., 2015): 引入逐元素门控 g_l ∈ [0,1]，但仍限于单层访问
- **Scaled Residual Paths** (DeepNet, Wang et al., 2022): 缩放残差路径以稳定训练
- **Multi-stream Recurrences** (Hyper-Connections, Zhu et al., 2025; mHC, Xie et al., 2026): 维护多个并行流，但仍受限于立即前驱状态

**跨层连接方法**:
- **DenseNet** (Huang et al., 2018): 拼接所有先前特征图，但组合权重固定
- **DenseFormer** (Pagliardini et al., 2024): 赋予每层访问所有先前输出的能力，但使用固定、输入无关的标量系数
- **MRLA** (Fang et al., 2023): 对所有先前层应用逐元素 sigmoid 门控，但 separable query-key 乘积更接近线性注意力

**研究缺口 (Gap)**:
现有方法要么局限于单层访问 (Highway、mHC)，要么缺乏输入依赖的选择性权重 (DenseFormer)，要么难以扩展到大规模 (MRLA)。关键缺口在于：**缺乏一种既能选择性访问所有先前层输出，又能保持计算效率、可大规模应用的深度聚合机制**。

本文的创新点在于将序列注意力机制推广到深度方向，提出深度 softmax 注意力，完成从线性注意力到 softmax 注意力的转变——这与序列建模中从 RNN 到 Transformer 的演进形成对偶。

### 1.3. 研究目标与核心假设/命题 (Objectives & Hypotheses/Propositions)

**研究目标**:
1. 提出 Attention Residuals (AttnRes)，用学习的 softmax 注意力替代固定残差累加
2. 设计 Block AttnRes 变体，降低内存和通信开销至 O(Nd)
3. 开发系统优化 (跨阶段缓存、两阶段计算)，使 Block AttnRes 在大规模训练中实用
4. 通过 Scaling Law、消融实验和下游基准验证方法有效性

**核心假设**:
- **H1**: 输入依赖的深度选择性聚合优于固定单位权重累加
- **H2**: Block AttnRes 能以约 8 个块恢复大部分 Full AttnRes 收益
- **H3**: AttnRes 能缓解 PreNorm 稀释，使输出幅度有界、梯度分布更均匀
- **H4**: 改进的深度信息流对组合性任务 (推理、代码)  benefit 更大

### 2. 研究设计与方法 (Methodology)

#### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

本研究采用**系统构建式研究**方法论：
1. **理论动机**: 基于时间 - 深度对偶性，将序列注意力推广到深度方向
2. **方法设计**: 提出 Full AttnRes 和 Block AttnRes 两种变体
3. **系统优化**: 针对大规模分布式训练开发基础设施优化
4. **实证验证**: 通过 Scaling Law、消融实验、下游基准多维度验证

**形式化对偶性**:
标准残差递归 h_l = h_{l-1} + f_{l-1}(h_{l-1}) 与 RNN 的时间递归形式相同。展开后：h_l = h_1 + Σ_{i=1}^{l-1} f_i(h_i)，这与 RNN 隐藏状态 S_t = S_{t-1} + k_t v_t^⊤ 的线性注意力形式一致。

AttnRes 将深度方向的线性注意力推广为 softmax 注意力：
$$h_l = \sum_{i=0}^{l-1} \alpha_{i \to l} \cdot v_i$$

其中注意力权重 α_{i→l} 通过 softmax 计算：
$$\alpha_{i \to l} = \frac{\phi(w_l, k_i)}{\sum_{j=0}^{l-1} \phi(w_l, k_j)}, \quad \phi(q, k) = \exp(q^\top \text{RMSNorm}(k))$$

#### 2.2. 数据来源与样本 (Data Source & Sample)

**训练数据**:
- **Scaling Law 实验**: 5 种模型规模 (194M-528M 激活参数)，在相同数据分布上训练
- **主实验**: Kimi Linear 48B 架构 (48B 总参数/3B 激活参数)，在 1.4T tokens 上预训练
  - 阶段 1: WSD 预训练，1T tokens
  - 阶段 2: Mid-training，≈400B 高质量 tokens
  - 上下文扩展：32K tokens

**评估基准** (三大类):
1. **语言理解与推理**: MMLU, MMLU-Pro, GPQA-Diamond, BBH, ARC-Challenge, HellaSwag, TriviaQA
2. **推理 (代码与数学)**: GSM8K, MGSM, Math, CMath, HumanEval, MBPP
3. **中文理解**: CMMLU, C-Eval

#### 2.3. 操作化与测量 (Operationalization & Measurement)

**关键变量定义**:

| 变量 | 定义 | 测量方式 |
|---|---|---|
| **验证 Loss** | 模型在 held-out 验证集上的交叉熵损失 | 每步训练后计算 |
| **输出幅度** | 各 Transformer 块输出的 L2 范数 | 训练结束时测量 |
| **梯度幅度** | 各块参数梯度的 L2 范数 | 训练过程中追踪 |
| **下游性能** | 各基准任务的准确率/得分 | 标准评估协议 |
| **训练开销** | 相对于基线的端到端训练时间增加 | Wall-clock 时间比较 |
| **推理延迟** | 典型推理工作负载的延迟增加 | 标准推理基准 |

**AttnRes 关键组件**:
- **伪查询向量**: w_l ∈ R^d，每层一个可学习参数，初始化为零
- **RMSNorm**: 防止大输出层主导注意力权重
- **块大小**: 主实验使用 6 层/块，产生 9 块 + 词嵌入 = 10 个深度源

**初始化策略**: 所有伪查询向量初始化为零，确保初始注意力权重均匀，AttnRes 退化为等权平均，防止训练初期波动。

### 3. 结果与发现 (Results & Findings)

#### 3.1. 主要发现概述 (Overview of Key Findings)

**Scaling Law 结果**:
拟合的幂律曲线显示：
- **基线**: L = 1.891 × C^{-0.057}
- **Block AttnRes**: L = 1.870 × C^{-0.058}
- **Full AttnRes**: L = 1.865 × C^{-0.057}

在 5.6 PFLOP/s-days 计算量下，Block AttnRes 达到 loss 1.692，基线为 1.714，**等效于 1.25×计算优势**。Full 与 Block AttnRes 的差距随规模缩小，在最大规模时仅差 0.001。

**下游任务性能** (表 3):

| 任务类别 | 具体任务 | 基线 | AttnRes | 提升 |
|---|---|---|---|---|
| **综合推理** | GPQA-Diamond | 36.9 | 44.4 | **+7.5** |
| | MMLU | 73.5 | 74.6 | +1.1 |
| | MMLU-Pro | 52.2 | 52.2 | 0.0 |
| **数学** | Math | 53.5 | 57.1 | **+3.6** |
| | GSM8K | 81.7 | 82.4 | +0.7 |
| **代码** | HumanEval | 59.1 | 62.2 | **+3.1** |
| | MBPP | 72.0 | 73.9 | +1.9 |
| **中文** | CMMLU | 82.0 | 82.9 | +0.9 |
| | C-Eval | 79.6 | 82.5 | **+2.9** |

**关键模式**: 改进在**多步推理任务**上最为显著 (GPQA、Math、Code)，知识型任务 (MMLU、TriviaQA) 也有稳定提升。这与假设 H4 一致：改进的深度信息流对组合性任务 benefit 更大。

**训练动态分析** (图 5):
1. **验证 Loss**: AttnRes 在整个训练过程中 consistently 低于基线，差距在 decay 阶段扩大
2. **输出幅度**: 基线随深度单调增长 (PreNorm 稀释)，Block AttnRes 在块内有界，呈现周期性模式
3. **梯度幅度**: 基线在早期层梯度过大，AttnRes 通过可学习 softmax 权重实现更均匀分布

#### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**图 1: Attention Residuals 概览**
- **展示内容**: 对比标准残差 (a)、Full AttnRes (b)、Block AttnRes (c) 的信息流
- **揭示关系**: 标准残差为均匀累加；Full AttnRes 每层选择性聚合所有先前输出；Block AttnRes 在块级别压缩，降低内存从 O(Ld) 到 O(Nd)
- **关键数据**: Block AttnRes 以 N≈8 即可恢复大部分收益

**图 4: Scaling Law 曲线**
- **展示内容**: 三种变体在不同计算量下的验证 loss
- **揭示关系**: AttnRes consistently 优于基线，Block 紧密跟踪 Full
- **关键数据**: 5.6 PFLOP/s-days 时，Block AttnRes 1.692 vs 基线 1.714

**图 5: 训练动态对比**
- **展示内容**: (a) 验证 loss 曲线，(b) 各块输出幅度，(c) 各块梯度幅度
- **揭示关系**: AttnRes 缓解 PreNorm 稀释，输出有界，梯度均匀
- **关键数据**: 基线输出幅度随深度增长至 15×10^{-5}，AttnRes 保持在 5×10^{-5} 以内

**图 8: 学习的注意力权重分布**
- **展示内容**: 16 层模型的深度注意力权重热力图
- **揭示关系**: 
  - **保持局部性**: 每层对直接前驱注意力最强
  - **学习到的跳跃连接**: 某些层对早期源有选择性注意 (如层 4 注意早期源)
  - **嵌入持久性**: 词嵌入 h_1 在整个网络中保持非平凡权重
  - **块注意力保留结构**: Block 变体保持与 Full 相同的本质模式

**表 1: 内存访问成本对比**

| 方法 | 每层每 token 总 I/O |
|---|---|
| 标准残差 | 3d |
| mHC (m=4) | 34d |
| Full AttnRes (两阶段) | 24d |
| Block AttnRes (N=8, S=16) | **5.5d** |

Block AttnRes 的内存效率显著优于 mHC，这是其可扩展性的关键。

### 4. 讨论 (Discussion)

#### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

**回答 RQ1 - 选择性深度聚合的有效性**:
AttnRes 通过引入输入依赖的 softmax 注意力，成功实现了深度方向的选择性信息聚合。消融实验表明，输入依赖查询进一步降低 loss 从 1.737 到 1.731，验证了 H1。与 DenseFormer (固定权重，1.767) 相比，AttnRes (1.737) 的 0.03 loss 提升凸显了输入依赖权重的重要性。

**回答 RQ2 - 大规模实用性**:
Block AttnRes 结合跨阶段缓存和两阶段计算策略，实现了：
- 训练开销 <4% (流水线并行下)
- 推理延迟开销 <2%
- 内存从 O(Ld) 降至 O(Nd)

这验证了 H2：约 8 个块即可恢复大部分 Full AttnRes 收益。图 6 的块大小消融显示，S=2,4,8 时 loss 均在 1.746 附近，S>16 时才显著退化。

**回答 RQ3 - 训练动态改善**:
图 5 的训练动态分析直接验证了 H3。AttnRes 通过选择性聚合：
1. **限制幅度增长**: 块边界的聚合重置累加，避免 O(L) 增长
2. **均匀化梯度**: softmax 权重的竞争性归一化防止某些层主导梯度流
3. **保留早期信息**: 嵌入层保持非平凡权重，防止信息丢失

#### 4.2. 理论贡献 (Theoretical Contributions)

**时间 - 深度对偶性**:
本文形式化了序列与深度的对偶关系：
- RNN 在时间维度使用递归：S_t = S_{t-1} + k_t v_t^⊤ (线性注意力)
- Transformer 用序列注意力替代时间递归
- 标准残差在深度维度使用递归：h_l = h_{l-1} + f_{l-1}(h_{l-1})
- AttnRes 用深度注意力替代深度递归

这完成了深度方向从线性注意力到 softmax 注意力的转变，与序列建模的演进平行。

**结构化矩阵分析**:
本文提出深度混合矩阵 M ∈ R^{L×L}，其中 M_{i→l} 表示层 l 对层 i 输出的权重。通过半可分秩 (semiseparable rank) 统一比较不同残差变体：

| 方法 | 权重类型 | 源访问 | M 的秩 |
|---|---|---|---|
| 标准残差 | 固定 | h_{l-1} | 1-半可分 |
| Highway | 输入依赖 | h_{l-1} | 1-半可分 |
| mHC | 输入依赖 | m 流 | m-半可分 |
| Full AttnRes | 输入依赖 | [h_1, ..., h_{l-1}] | L (稠密) |
| Block AttnRes | 输入依赖 | [b_0, ..., b_{N-1}, b_n^i] | N 到 N+S |

这一视角揭示：现有残差变体实质上是**深度线性注意力**，而 AttnRes 是**深度 softmax 注意力**。

#### 4.3. 实践启示 (Practical Implications)

**对架构设计的启示**:
图 7 的架构搜索显示，AttnRes 的最优配置在 d_model/L_b ≈ 45，而基线在 ≈60。这意味着**AttnRes 能更有效地利用额外深度**，偏好更深、更窄的网络。虽然这不直接转化为部署建议 (更深模型推理延迟更高)，但为架构选择提供了新维度。

**即插即用替换**:
Block AttnRes 可作为标准残差连接的 drop-in replacement：
- 仅需添加每层一个 RMSNorm 和一个伪查询向量 (参数量可忽略)
- 与任何归一化或门控方案兼容
- 推理时 KV 缓存大小有界 (N 个块表示)

**未来方向**:
- 更细粒度分块 (S<4) 在内存约束放宽时可进一步提升性能
- 探索线性复杂度深度注意力变体
- 将 AttnRes 与其他残差泛化方法 (如 mHC) 结合

#### 4.4. 局限性与未来研究 (Limitations & Future Research)

**局限性**:
1. **深度限制**: 当前架构深度 L<1000，使得 O(L²) 深度注意力可行；若深度大幅增加，需探索更高效的注意力变体
2. **推理延迟**: 虽然开销<2%，但更深模型本身因序列计算导致更高延迟
3. **块大小选择**: 最优块数 N≈8 是经验性的，缺乏理论指导
4. **单查询限制**: 默认使用单伪查询向量，多注意力头实验 (H=16) 反而损害性能

**未来研究方向**:
1. **更高效的深度注意力**: 探索线性复杂度核函数 φ(q,k) = φ(q)^⊤φ(k)，将注意力坍缩为递归
2. **自适应块大小**: 根据输入动态调整块划分
3. **与其他方法结合**: 如 AttnRes + mHC，结合多流与选择性访问
4. **理论分析**: 深度注意力的表达性边界、最优深度 - 宽度权衡的理论推导
5. **跨架构泛化**: 在非 MoE、非 Transformer 架构上验证 AttnRes

### 5. 结论 (Conclusion)

本文提出 Attention Residuals (AttnRes)，用学习的、输入依赖的深度注意力替代固定、均匀的残差累加。通过时间 - 深度对偶性动机，AttnRes 完成了深度方向从线性注意力到 softmax 注意力的转变。

**核心贡献**:
1. **方法创新**: Full AttnRes 实现深度 softmax 注意力，Block AttnRes 将开销从 O(Ld) 降至 O(Nd)
2. **系统优化**: 跨阶段缓存和两阶段计算使 Block AttnRes 在大规模训练中实用
3. **实证验证**: Scaling Law、消融实验、48B 模型 1.4T tokens 预训练一致证明有效性

**关键发现**:
- Block AttnRes 等效于 1.25×计算优势
- 所有下游任务均有提升，多步推理任务提升最显著
- 缓解 PreNorm 稀释，输出有界，梯度均匀
- 训练开销<4%，推理延迟<2%

AttnRes 为深度神经网络的信息流设计提供了新范式，将选择性注意力从序列维度扩展到深度维度，开启了架构设计的新可能性。

### 6. 核心参考文献 (Core References)

1. **He, K. et al. (2015)**. Deep Residual Learning for Image Recognition. arXiv:1512.03385. (残差学习奠基工作)
2. **Xiong, R. et al. (2020)**. On Layer Normalization in the Transformer Architecture. arXiv:2002.04745. (PreNorm 分析)
3. **Zhu, D. et al. (2025)**. Hyper-Connections. arXiv:2409.19606. (多流残差)
4. **Xie, Z. et al. (2026)**. mHC: Manifold-Constrained Hyper-Connections. arXiv:2512.24880. (稳定化多流)
5. **Pagliardini, M. et al. (2024)**. DenseFormer: Enhancing Information Flow in Transformers via Depth Weighted Averaging. arXiv:2402.02622. (跨层连接对比)

---

## Part B: 核心逻辑链与根本价值提炼

## 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | 现代 LLM 的 PreNorm 残差连接使用固定单位权重累加所有层输出，导致隐藏状态幅度随深度 O(L) 增长，逐层稀释各层贡献。早期层信息被埋没且无法选择性检索，相当一部分层可被剪枝而损失很小——这意味着深度方向的信息聚合机制存在根本缺陷。 |
| **切入视角** | 作者洞察到**时间 - 深度对偶性**：RNN 在时间维度用递归压缩信息，被 Transformer 的序列注意力取代；同理，残差连接在深度维度用递归压缩信息，也应被深度注意力取代。关键转折点是认识到"标准残差和 prior 变体实质是深度线性注意力，AttnRes 将其推广为深度 softmax 注意力"。 |
| **关键方法** | 每层引入一个可学习的伪查询向量 w_l ∈ R^d，计算对所有先前层输出的 softmax 注意力权重，实现输入依赖的选择性聚合。为降低开销，将 L 层分成 N≈8 个块，块内标准累加、块间注意力，配合跨阶段缓存和两阶段计算，将内存和通信从 O(Ld) 降至 O(Nd)。 |
| **核心发现** | Block AttnRes 在 Scaling Law 中 consistent 优于基线，等效 1.25×计算优势；在 48B 模型 1.4T tokens 预训练中，所有下游任务提升，多步推理任务提升最显著 (GPQA +7.5, Math +3.6, HumanEval +3.1)；训练动态分析证实缓解 PreNorm 稀释，输出幅度有界、梯度分布更均匀；训练开销<4%，推理延迟<2%。 |

---

## 方法公式化

**AttnRes 核心公式**:

```
标准残差：h_l = h_{l-1} + f_{l-1}(h_{l-1})
         = h_1 + Σ_{i=1}^{l-1} f_i(h_i)  [展开后，固定单位权重]

AttnRes:   h_l = Σ_{i=0}^{l-1} α_{i→l} · v_i
           其中 α_{i→l} = softmax(w_l^⊤ RMSNorm(k_i))
           v_0 = h_1 (词嵌入), v_i≥1 = f_i(h_i)

Block AttnRes: h_l = Σ_{n=0}^{N-1} α_{n→l} · b_n + Σ_{j=1}^{i} α_{j→l} · b_n^j
               其中 b_n = Σ_{j∈B_n} f_j(h_j) (块表示)
                     b_n^i (块内部分和)
```

**文字公式**:

```
选择性深度聚合 = (伪查询向量 w_l) × (RMSNorm 化的先前层输出) → softmax 注意力权重

Block 优化 = (层分组为 N 块) × (块内累加 + 块间注意力) → O(Nd) 内存

实用化 = (跨阶段缓存) + (两阶段计算：并行块间 + 序列块内) → <4% 训练开销
```

---

## 最终双重总结

**一句话总结（核心价值）**：
Attention Residuals 通过发现时间 - 深度对偶性，将 Transformer 的序列注意力思想推广到深度维度，用学习的 softmax 注意力替代固定残差累加，实现了输入依赖的选择性深度信息聚合，在 48B 模型上验证了等效 1.25×计算优势和全任务提升，同时以 Block 设计和系统优化将开销控制在可接受范围，为深度神经网络的信息流设计提供了新范式。

**一句话总结（大白话版）**：
就像 Transformer 用注意力机制让每个词能看到句子里所有其他词一样，AttnRes 让神经网络的每一层能"回头看"前面所有层的输出，并学会选择性地关注重要的那些，而不是简单地全部加在一起——这让模型更聪明地利用深度，推理能力更强，尤其是做数学题和写代码这种多步思考的任务。
