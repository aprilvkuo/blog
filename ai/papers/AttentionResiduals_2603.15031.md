---
title: AttentionResiduals
description: Attention Residuals 双模式研读报告
date: 2026-03-27
arxiv: 2603.15031
category: optimization
tags: ['llm', 'scientific', 'optimization', 'efficiency']
outline: [2, 3]
---

::: tip 📄 论文信息
- **arXiv**: [2603.15031](https://arxiv.org/abs/2603.15031)
- **分类**: 模型优化
- **标签**: llm, scientific, optimization, efficiency
:::


::: info 📑 目录
本文档包含完整的论文研读报告，包括深度学术速读和技术实现分析两部分。
:::

# Attention Residuals 双模式研读报告

**论文标题**: Attention Residuals  
**arXiv**: 2603.15031  
**作者**: Kimi Team (Guangyu Chen, Yu Zhang, Jianlin Su 等 38 位作者)  
**日期**: 2026 年 3 月 16 日  
**领域**: 计算语言学 (cs.CL)  
**代码**: https://github.com/MoonshotAI/Attention-Residuals

---

## Part A: 深度专业学术速读报告

## 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 现代大语言模型 (LLM) 标准采用 PreNorm 残差连接，但其固定单位权重的累积方式导致隐藏状态幅度随深度无控制增长 (O(L))，逐渐稀释每一层的贡献。本研究旨在解决这一"PreNorm 稀释"问题。 |
| **方法** | 提出 Attention Residuals (AttnRes)，用 softmax 注意力机制替代固定的残差累积，使每层能够以学习的、输入依赖的权重选择性聚合早期表示。进一步提出 Block AttnRes，将层划分为块，在块级表示上进行注意力计算，将内存和通信开销从 O(Ld) 降至 O(Nd)。 |
| **结果** | Scaling law 实验证实改进在所有模型规模上一致。在 Kimi Linear 架构 (48B 总参数/3B 激活参数) 上预训练 1.4T tokens，AttnRes 缓解了 PreNorm 稀释，产生更均匀的输出幅度和梯度分布，在所有评估任务上提升下游性能。Block AttnRes 在 8 块配置下恢复 Full AttnRes 大部分收益，训练开销<4%，推理延迟开销<2%。 |
| **结论** | AttnRes 通过将深度方向的信息聚合从固定权重升级为内容依赖的 softmax 注意力，完成了与序列维度从 RNN 到 Transformer 相似的范式转变。该方法可作为标准残差连接的即插即用替换，在大规模训练中实用且高效。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

标准残差连接 (Residual Connections) 自 ResNet 提出以来，已成为现代深度神经网络的基石。在 Transformer 架构中，残差更新公式 h_l = h_{l-1} + f_{l-1}(h_{l-1}) 被广泛理解为"梯度高速公路"，允许梯度通过恒等映射绕过变换层，从而实现深度稳定训练。

然而，残差连接还扮演着第二个较少受到关注的角色：**信息跨深度聚合**。展开递归关系可知，每一层接收的是所有先前层输出的均匀加权和。与序列混合 (self-attention) 和专家路由 (MoE) 已采用可学习的输入依赖权重不同，**深度方向的聚合仍由固定单位权重控制**，缺乏选择性强调或抑制个别层贡献的机制。

在实践中，PreNorm 已成为主导范式，但其无加权累积导致隐藏状态幅度随深度呈 O(L) 增长，逐渐稀释每层的相对贡献。早期层的信息被埋没且无法选择性检索；经验表明，相当一部分层可以被剪枝而损失微小。

**核心研究问题**:
1. 如何使深度方向的信息聚合具备输入依赖的选择性，类似注意力机制在序列维度上的作用？
2. 如何在保持效率的前提下，将这种机制扩展到大规模模型训练？
3. 这种机制能否改善训练动态和下游任务性能？

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

**残差连接的演进**:
- **ResNet** (He et al., 2015): 提出恒等映射残差连接，解决深度网络退化问题
- **PreNorm vs PostNorm**: PreNorm (Xiong et al., 2020) 恢复干净的恒等路径但引入幅度增长；PostNorm 保持有界幅度但扭曲梯度传播
- **DeepNorm** (Wang et al., 2022): 通过缩放残差路径缓解 PreNorm 问题
- **Highway Networks** (Srivastava et al., 2015): 引入逐元素门控，但仍受限于单状态递归

**多状态递归方法**:
- **Hyper-Connections** (Zhu et al., 2025) 和 **mHC** (Xie et al., 2026): 维护 m 个并行流，学习混合矩阵
- **DDL** (Zhang et al., 2026): 通过 delta 规则擦除 - 写入机制维护矩阵状态
- **SiameseNorm** (Li et al., 2026): 维护两个参数共享的流 (PreNorm + PostNorm)

**跨层连接方法**:
- **DenseNet** (Huang et al., 2018): 拼接所有先前特征图
- **DenseFormer** (Pagliardini et al., 2024): 使用学习到的每层标量系数 (固定)
- **MUDDFormer** (Xiao et al., 2025): 通过小型 MLP 生成位置依赖权重
- **MRLA** (Fang et al., 2023): 应用逐元素 sigmoid 门控

**研究缺口**:
1. 现有方法仍受限于**加性递归范式**，无法实现对个别早期层输出的选择性访问
2. 引入跨层访问的方法难以扩展到大规模训练
3. 缺乏对深度方向信息聚合的系统性理论分析

### 1.3. 研究目标与核心假设/命题 (Objectives & Hypotheses/Propositions)

**研究目标**:
1. 提出一种新机制，用**softmax 注意力替代固定残差累积**，实现深度方向的内容依赖选择性聚合
2. 设计可扩展的基础设施优化，使该方法在大规模训练中实用高效
3. 通过系统性实验验证方法的有效性和理论分析

**核心命题**:
- **P1 (时间 - 深度对偶性)**: 深度方向的信息聚合与序列方向的递归存在形式对偶性，序列维度的注意力机制可以平行迁移到深度维度
- **P2 (线性注意力视角)**: 标准残差连接和先前的递归变体实际上执行深度方向的**线性注意力**，AttnRes 将其推广为**softmax 注意力**
- **P3 (可扩展性)**: 通过块级优化和基础设施设计，AttnRes 可以作为标准残差连接的即插即用替换，开销可忽略

---

## 2. 研究设计与方法 (Methodology)

### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

本研究采用**系统构建 + 实证验证**的方法论：

1. **理论分析**: 建立时间 - 深度对偶性框架，将残差连接统一为结构化矩阵视角
2. **方法设计**: 提出 Full AttnRes 和 Block AttnRes 两种变体
3. **基础设施优化**: 设计跨阶段缓存和两阶段计算策略
4. **实证验证**: 通过 scaling law、消融实验和下游基准测试全面评估

### 2.2. 数据来源与样本 (Data Source & Sample)

**模型配置**:
- **Scaling Law 实验**: 5 个模型规模 (194M-528M 激活参数)
- **主实验**: Kimi Linear 48B 架构 (27 个 Transformer 块/54 层，8/256 路由专家 + 1 共享专家)
- **训练数据**: 1.4T tokens，遵循 Kimi Linear 数据配方

**评估基准**:
- **语言理解与推理**: MMLU, MMLU-Pro Hard, GPQA-Diamond, BBH, ARC-Challenge, HellaSwag, TriviaQA
- **推理 (代码与数学)**: GSM8K, MGSM, Minerva Math, CMath, HumanEval, MBPP
- **中文理解**: CMMLU, C-Eval

### 2.3. 操作化与测量 (Operationalization & Measurement)

**Full AttnRes 公式化**:
```
h_l = Σ_{i=0}^{l-1} α_{i→l} · v_i
α_{i→l} = softmax(q_l, k_i) = exp(q_l^T RMSNorm(k_i)) / Σ_j exp(q_l^T RMSNorm(k_j))
```
其中 q_l = w_l (每层一个可学习的 d 维权重向量)，k_i = v_i = h_1 (i=0) 或 f_i(h_i) (i≥1)

**Block AttnRes**:
- 将 L 层划分为 N 块，每块 S=L/N 层
- 块内：通过求和归约为单个表示 b_n = Σ_{j∈B_n} f_j(h_j)
- 块间：在 N 个块级表示上应用完整注意力
- 复杂度：从 O(L²d) 降至 O(N²d)，内存从 O(Ld) 降至 O(Nd)

**关键设计选择**:
- **伪查询解耦**: w_l 是独立于前向计算的参数，允许并行计算
- **RMSNorm on keys**: 防止大振幅输出主导注意力权重
- **零初始化**: 所有 w_l 初始化为 0，确保初始注意力权重均匀，避免训练不稳定

**基础设施优化**:
1. **跨阶段缓存** (训练): 缓存接收到的块，消除流水线并行中的冗余传输
2. **两阶段计算** (推理): Phase1 批量计算块间注意力，Phase2 顺序计算块内注意力 + online softmax 合并
3. **内存高效预填充**: 沿序列维度分片块表示，减少每设备内存占用

---

## 3. 结果与发现 (Results & Findings)

### 3.1. 主要发现概述 (Overview of Key Findings)

**Scaling Law 结果**:
- Baseline: L = 1.891 × C^{-0.057}
- Block AttnRes: L = 1.870 × C^{-0.058}
- Full AttnRes: L = 1.865 × C^{-0.057}

在 5.6 PFLOP/s-days 时，Block AttnRes 达到 1.692，而 Baseline 为 1.714，相当于**1.25 倍计算优势**。Full AttnRes 与 Block AttnRes 的差距随规模缩小，在最大规模时仅为 0.001。

**训练动态分析**:
1. **验证损失**: AttnRes 在整个训练过程中持续保持更低的验证损失，在衰减阶段差距扩大
2. **输出幅度**: Baseline 遭受 PreNorm 稀释问题 (隐藏状态幅度随深度单调增长)；Block AttnRes 将增长限制在块内，产生有界的周期性模式
3. **梯度幅度**: Baseline 在最早层产生不成比例的大梯度；Block AttnRes 的 softmax 权重引入竞争，产生更均匀的梯度分布

**下游性能** (Kimi Linear 48B, 1.4T tokens):
| 任务类型 | 具体任务 | 提升 |
|---|---|---|
| 多步推理 | GPQA-Diamond | +7.5 |
| 数学推理 | Minerva Math | +3.6 |
| 代码生成 | HumanEval | +3.1 |
| 知识型 | MMLU | +1.1 |
| 知识型 | TriviaQA | +1.9 |

所有基准测试均达到或超过 Baseline，改进在多步推理任务上尤为显著。

### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**图 1: Scaling Law 曲线**
- **展示内容**: 三个变体 (Baseline/Block/Full AttnRes) 在不同计算预算下的验证损失
- **揭示关系**: AttnRes 始终优于 Baseline，且优势随计算量增加而扩大
- **关键数据**: Block AttnRes 在 5.6 PFLOP/s-days 时达到 Baseline 需 7.0 PFLOP/s-days 才能达到的损失

**图 2: 训练动态对比** (1T tokens)
- **展示内容**: 验证损失、输出幅度、梯度幅度随训练步数的变化
- **揭示关系**: AttnRes 缓解 PreNorm 稀释，改善梯度流动
- **关键数据**: Baseline 隐藏状态幅度随深度增长 10 倍+，AttnRes 保持有界波动

**图 3: 学习的注意力权重热力图**
- **展示内容**: 每层 (行) 对先前源 (列) 的注意力权重分布
- **揭示关系**: 
  - **保持局部性**: 每层最关注直接前驱，但出现选择性非对角集中
  - **层专业化**: 嵌入 h_1 在整个网络中保持非平凡权重，尤其在 pre-attention 层
  - **Block 保持结构**: 块级压缩保留基本通路，起到隐式正则化作用

**表 1: 消融实验** (16-head 模型，验证损失)
| 变体 | 损失 | 对比 |
|---|---|---|
| Baseline | 1.766 | - |
| DenseFormer | 1.767 | 无增益 (固定权重不足) |
| mHC | 1.747 | +0.019 (多流混合) |
| Block AttnRes (N=8) | 1.746 | +0.020 (单查询向量) |
| Full AttnRes | 1.737 | +0.029 (完整跨层访问) |
| + 输入依赖查询 | 1.731 | +0.035 (但有 d×d 投影开销) |

---

## 4. 讨论 (Discussion)

### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

**时间 - 深度对偶性的验证**:
本研究的核心洞察是将深度方向的信息聚合类比于序列方向的递归。正如 Transformer 用注意力替代 RNN 的时间递归，AttnRes 用注意力替代深度递归。这一对偶性在数学上表现为：

- **RNN over time**: h_t = h_{t-1} + f(h_{t-1}) → Attention: h_t = Σ α_{i→t} v_i
- **Residual over depth**: h_l = h_{l-1} + f(h_{l-1}) → AttnRes: h_l = Σ α_{i→l} v_i

实验结果支持这一类比：AttnRes 在深度方向实现了与 self-attention 在序列方向相似的收益。

**PreNorm 稀释问题的解决**:
PreNorm 的核心矛盾是：归一化恢复梯度流动但导致幅度增长。AttnRes 通过选择性聚合绕过这一矛盾：
- 块内累积被块间注意力"重置"，防止无限增长
- softmax 权重的竞争性归一化自然平衡各层贡献
- RMSNorm on keys 防止大振幅输出主导

**结构化矩阵视角的洞见**:
将残差变体统一为深度混合矩阵 M 的视角揭示了：
- **标准残差**: M 是全 1 下三角矩阵 (秩 L)
- **(m)HC**: M 是 m-半可分矩阵 (秩 m)
- **Full AttnRes**: M 是稠密秩 L 矩阵 (输入依赖)
- **Block AttnRes**: M 的有效秩在 N 到 N+S 之间

这一视角解释了为什么 AttnRes 优于线性注意力方法：softmax 的竞争性归一化产生更锐利的选择。

### 4.2. 理论贡献 (Theoretical Contributions)

**1. 时间 - 深度对偶性框架**:
建立了序列递归与深度残差的形式对偶性，为跨维度方法迁移提供理论基础。

**2. 残差连接的统一视角**:
通过结构化矩阵分析，将标准残差、Highway、(m)HC、DDL 等统一为深度方向线性注意力的特例，AttnRes 完成向 softmax 注意力的跃迁。

**3. 可扩展深度注意力设计**:
提出 Block AttnRes 及配套设施优化，证明深度注意力在现有硬件上可行。

### 4.3. 实践启示 (Practical Implications)

**对模型架构师的启示**:
1. **即插即用替换**: Block AttnRes 可直接替换现有 Transformer 的残差连接，无需修改其他组件
2. **块数选择**: N≈8 在大多数规模下恢复大部分收益，可作为默认配置
3. **初始化策略**: 伪查询向量必须零初始化，避免训练不稳定

**对大规模训练的启示**:
1. **流水线并行友好**: 跨阶段缓存将通信从 O(C) 降至 O(P)，支持高效 1F1B 调度
2. **推理开销可控**: 两阶段计算 + kernel 融合将延迟开销控制在 2% 以内
3. **长上下文支持**: 序列分片预填充将 128K 上下文的内存从 15GB 降至 1.9GB/设备

**对下游任务的启示**:
改进在多步推理和代码生成任务上最显著，表明改善的深度信息流特别有利于组合性任务。

### 4.4. 局限性与未来研究 (Limitations & Future Research)

**局限性**:
1. **深度限制**: 当前架构深度 L<1000，使 O(L²) 注意力可行；若深度继续增长，可能需要线性复杂度变体
2. **固定块数**: 当前使用固定 N≈8，未探索自适应块划分
3. **单查询向量**: 默认使用与输入解耦的伪查询，虽高效但可能限制表达能力

**未来方向**:
1. **更细粒度块**: 随硬件内存容量提升，采用更小 S 或 Full AttnRes
2. **输入依赖查询**: 探索从隐藏状态投影查询的变体 (消融显示损失可进一步降至 1.731)
3. **线性复杂度深度注意力**: 借鉴序列侧的线性注意力方法 (如 RetNet, GLA)
4. **架构搜索**: AttnRes 改变最优深度 - 宽度权衡 (实验显示偏好更深更窄的架构)

---

## 5. 结论 (Conclusion)

本研究提出 Attention Residuals (AttnRes)，通过将固定残差累积替换为深度方向的 softmax 注意力，实现了内容依赖的选择性跨层信息聚合。核心贡献包括：

1. **方法创新**: Full AttnRes 和 Block AttnRes 两种变体，前者理论完备，后者实用高效
2. **理论洞见**: 时间 - 深度对偶性框架和结构化矩阵分析，统一现有残差变体为深度线性注意力
3. **基础设施**: 跨阶段缓存和两阶段计算策略，使大规模训练可行
4. **实证验证**: Scaling law、消融实验和 48B 模型 1.4T tokens 预训练，一致证明有效性

AttnRes 完成了深度方向从线性注意力到 softmax 注意力的范式转变，与序列方向从 RNN 到 Transformer 的演进形成对称。在现有硬件约束下，Block AttnRes (N≈8) 是实用的默认选择；随硬件发展，更细粒度的深度注意力有望进一步释放潜力。

---

## 6. 核心参考文献 (Core References)

1. **He et al. (2015)**. Deep Residual Learning for Image Recognition. *CVPR*. (ResNet 残差连接)
2. **Xiong et al. (2020)**. Layer Normalization in Transformer. *arXiv*. (PreNorm/PostNorm 分析)
3. **Vaswani et al. (2017)**. Attention Is All You Need. *NeurIPS*. (Transformer 注意力机制)
4. **Zhang et al. (2025)**. Kimi Linear Architecture. *arXiv*. (基线架构)
5. **Xie et al. (2026)**. Multi-Stream Hyper-Connections. *arXiv*. (mHC 多流混合)

---

---

## Part B: 核心逻辑链与根本价值提炼

## 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | PreNorm 残差连接的固定单位权重累积导致隐藏状态幅度随深度 O(L) 增长，逐渐稀释每层贡献，早期层信息被埋没且无法选择性检索。这限制了深度网络的有效层数和表达能力。 |
| **切入视角** | 发现深度方向的信息聚合与序列方向的递归存在形式对偶性：正如 Transformer 用注意力替代 RNN 的时间递归，深度方向也可以用注意力替代残差递归。关键洞察是"残差连接本质上是深度方向的线性注意力"。 |
| **关键方法** | 用 softmax 注意力替代固定残差累积：h_l = Σ α_{i→l} · v_i，其中 α 由每层一个可学习的 d 维伪查询向量 w_l 计算。进一步提出 Block AttnRes，将层划分为 N 块，在块级表示上注意力，将复杂度从 O(L²d) 降至 O(N²d)。 |
| **核心发现** | Scaling law 显示 AttnRes 在所有规模上一致优于 Baseline，等效于 1.25 倍计算优势。在 48B 模型 1.4T tokens 预训练中，AttnRes 缓解 PreNorm 稀释，改善梯度分布，在所有下游任务上提升性能 (GPQA-Diamond +7.5, HumanEval +3.1)。 |

---

## 方法公式化

**AttnRes 核心公式**:

```
标准残差：h_l = h_{l-1} + f_{l-1}(h_{l-1})
          = h_1 + Σ_{i=1}^{l-1} f_i(h_i)  [展开后]
          = Σ_{i=0}^{l-1} 1 · v_i         [统一权重为 1]

AttnRes:   h_l = Σ_{i=0}^{l-1} α_{i→l} · v_i
           α_{i→l} = softmax(w_l^T RMSNorm(v_i))
           
Block AttnRes:
           块内：b_n = Σ_{j∈B_n} f_j(h_j)
           块间：h_l = Σ_{n=0}^{N-1} α_{n→l} · b_n
```

**文字公式**:

```
深度信息聚合 = (伪查询向量 w_l) × softmax(与所有先前层表示的相似度)
Block 优化 = (层划分为 N 块) × (块内求和 + 块间注意力)
效率提升 = (跨阶段缓存) × (两阶段计算 + online softmax 合并)
```

**结构化矩阵视角**:

```
标准残差：M = 全 1 下三角矩阵 (秩 L，输入独立)
(m)HC:     M = m-半可分矩阵 (秩 m，输入依赖)
AttnRes:   M = 稠密矩阵 (秩 L，输入依赖，softmax 归一化)
```

---

## 最终双重总结

**一句话总结（核心价值）**:
Attention Residuals 通过将深度方向的固定残差累积升级为输入依赖的 softmax 注意力机制，并配合块级优化和基础设施设计，在保持计算效率的同时实现了选择性跨层信息聚合，在 48B 模型 1.4T tokens 预训练中一致提升所有下游任务性能，完成了深度方向从线性注意力到 softmax 注意力的范式转变。

**一句话总结（大白话版）**:
就像 Transformer 用注意力机制让每个词能看到句子里所有其他词一样，AttnRes 让神经网络的每一层能"回头看"前面所有层的输出，并学会哪些重要哪些不重要，而不是简单地全部加在一起，这样深层网络就能更好地利用早期层的信息，学得更聪明。

---

## 附录：关键术语对照表

| 英文 | 中文 | 说明 |
|---|---|---|
| Attention Residuals (AttnRes) | 注意力残差 | 本文提出的核心方法 |
| PreNorm | 预归一化 | 在残差分支前进行归一化 |
| PostNorm | 后归一化 | 在残差分支后进行归一化 |
| Block AttnRes | 块级注意力残差 | AttnRes 的可扩展变体 |
| Pseudo-query | 伪查询 | 每层一个可学习的查询向量 |
| Depth-wise attention | 深度方向注意力 | 在层维度上的注意力机制 |
| Semi-separable matrix | 半可分矩阵 | 结构化矩阵的一种 |
| Online softmax | 在线 softmax | 分块计算 softmax 的数值稳定算法 |
| Pipeline parallelism | 流水线并行 | 分布式训练策略 |
| Cross-stage caching | 跨阶段缓存 | 消除冗余通信的优化 |

---

*报告生成时间：2026 年 3 月 26 日*  
*解析工具：paper-parse 技能*
