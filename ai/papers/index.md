---
title: 论文研读
description: AI 论文研读报告集合
outline: false
---

# 📚 论文研读

本页面收录了 AI 领域的论文研读报告，涵盖 Agent、RAG、多模态、模型优化等方向。

## 📊 统计信息

<div class="paper-stats">

- **总计**: 34 篇论文
- **分类**: 10 个类别
- **Agent/智能体**: 8 篇
- **金融/交易**: 1 篇
- **工具/框架**: 5 篇
- **记忆系统**: 4 篇
- **多模态**: 4 篇
- **模型优化**: 5 篇
- **其他**: 2 篇
- **RAG/检索增强**: 1 篇
- **强化学习**: 2 篇
- **世界模型**: 2 篇

</div>

## 📁 分类目录

### Agent/智能体 {#agent}

<div class="paper-list">

- **[OpenDevin](./OpenDevin_2407.16741)** 
  - arXiv: `2407.16741` · 2026-03-27 · 'multi-agent' | 'social-simulation' | 'scientific' | 'llm' | 'agent'
  - *OpenHands 是一个功能完整、立即可用的 AI 智能体平台，支持学术和工业界的多样化研究和应用。平台采用 MIT 许可证，已获 32K GitHub stars，2.1K+ 贡献来自 188+ 贡献者，成为通用数字智能体研究的重要催化剂。*

- **[MiroThinker](./MiroThinker_2511.11793)** 
  - arXiv: `2511.11793` · 2026-03-27 · 'optimization' | 'llm' | 'agent' | 'scientific'
  - *交互深度展现出与模型规模和上下文长度类似的扩展行为，是构建下一代开源研究智能体的第三个关键维度。*

- **[Hyperagents](./Hyperagents_2603.19461)** 
  - arXiv: `2603.19461` · 2026-03-27 · 'social-simulation' | 'scientific' | 'optimization' | 'rag' | 'agent'
  - *HyperAgents 首次实现了不依赖对齐假设的通用自改进框架，元认知自改进使系统能够改进"如何改进"的能力，跨域转移和累积效应支持无界开放-ended 进步的可能性。*

- **[EvoScientist](./EvoScientist_2603.08127)** 
  - arXiv: `2603.08127` · 2026-03-27 · 'multi-agent' | 'social-simulation' | 'scientific' | 'llm' | 'agent'
  - *持久记忆和多智能体演化机制能有效提升科学想法质量和代码执行可靠性，为端到端 AI 科学家系统提供了可复用的演化架构。*

- **[AutoDev](./AutoDev_2403.08299)** 
  - arXiv: `2403.08299` · 2026-03-27 · 'llm' | 'agent' | 'scientific'
  - *AutoDev 显著提升了 LLM 在软件工程任务中的性能（相比 GPT-4 零样本基线提升 30%），同时保持了安全和用户可控的开发环境。该框架将 AI 代理从被动代码建议转变为主动任务执行，验证了自主 AI 代理在复杂软件工程任务中的有效性。*

- **[AgentScope](./AgentScope_2407.17789)** 
  - arXiv: `2407.17789` · 2026-03-27 · 'multi-agent' | 'social-simulation' | 'efficiency' | 'scientific' | 'distributed' | 'llm' | 'agent'
  - *AgentScope 的增强功能有效解决了大规模多智能体模拟的可扩展性、效率和多样性问题，实验结果验证了多智能体系统在社会模拟中的巨大潜力，为相关研究提供了灵活且强大的工具平台。*

- **[AgentScope10](./AgentScope10_2508.16279)** 
  - arXiv: `2508.16279` · 2026-03-27 · 'multi-agent' | 'efficiency' | 'scientific' | 'optimization' | 'llm' | 'agent'
  - *AgentScope 1.0 为构建可扩展、自适应、高效的智能体应用提供了实用基础，弥合了原型智能体与实际应用之间的差距。*

- **[AIScientistv2](./AIScientistv2_2504.08066)** 
  - arXiv: `2504.08066` · 2026-03-27 · 'scientific' | 'vision' | 'agent' | 'llm'
  - *The AI Scientist-v2 成功实现了 workshop 级别的自动科学发现，标志着 AI 生成研究通过同行评审的重要里程碑。但系统尚未持续达到顶级会议标准，仍需在假设新颖性、实验深度和领域专业知识方面改进。*

</div>

### 金融/交易 {#finance}

<div class="paper-list">

- **[TradingAgents](./TradingAgents_2412.20138)** 
  - arXiv: `2412.20138` · 2026-03-27 · 'multi-agent' | 'social-simulation' | 'scientific' | 'finance' | 'llm'
  - *多 agent LLM 框架通过模拟真实交易公司的协作动态和采用结构化通信协议，能显著提升交易性能，同时在可解释性方面优于传统深度学习方法。*

</div>

### 工具/框架 {#framework}

<div class="paper-list">

- **[SmolDocling](./SmolDocling_2503.11576)** 
  - arXiv: `2503.11576` · 2026-03-27 · 'ocr' | 'framework' | 'efficiency' | 'scientific' | 'optimization' | 'vision' | 'llm'
  - *证明小模型通过统一优化的输出格式可与大模型竞争，为资源高效的多任务文档理解开辟新路径。DocTags 格式有效解耦内容与结构，提升 Image-to-Sequence 模型性能。贡献的新数据集填补了多模态文档理解领域的空白。*

- **[MinerUDiffusion](./MinerUDiffusion_2603.22458)** 
  - arXiv: `2603.22458` · 2026-03-27 · 'ocr' | 'framework' | 'efficiency' | 'scientific' | 'vision'
  - *扩散解码是文档 OCR 的有前景的替代方案，在保持高识别准确率的同时显著提升长序列推理效率，有效缓解自回归解码中的语义幻觉和累积错误传播问题。*

- **[MinerU2.5](./MinerU2.5_2509.22186)** 
  - arXiv: `2509.22186` · 2026-03-27 · 'ocr' | 'framework' | 'efficiency' | 'scientific' | 'optimization' | 'rag' | 'vision' | 'llm'
  - *MinerU2.5 通过解耦架构成功解决了文档解析中性能与效率的权衡问题。其核心价值不仅在于 standalone 能力，更在于作为 LLM 时代的基础工具，能够高效将非结构化文档转化为结构化数据，支持高质量预训练语料构建和 RAG 系统增强。*

- **[LlamaFactory](./LlamaFactory_2403.13372)** 
  - arXiv: `2403.13372` · 2026-03-27 · 'framework' | 'efficiency' | 'scientific' | 'distributed' | 'llm'
  - *LlamaFactory 通过模块化设计最小化了模型、数据集和训练方法之间的依赖，首次支持在单模型上完成完整 RLHF 训练，显著降低了 LLM 微调的门槛，已获 25,000+ GitHub stars 和数百个衍生模型。*

- **[LTX2](./LTX2_2601.03233)** 
  - arXiv: `2601.03233` · 2026-03-27 · 'speech' | 'framework' | 'efficiency' | 'scientific' | 'optimization' | 'vision'
  - *LTX-2 建立了新的开源 T2AV 生成基础，以前所未有的速度生成连贯、富有表现力且细节丰富的音视频内容，所有模型权重和代码已公开。*

</div>

### 记忆系统 {#memory}

<div class="paper-list">

- **[MementoSkills](./MementoSkills_2603.18743)** 
  - arXiv: `2603.18743` · 2026-03-27 · 'optimization' | 'memory' | 'scientific' | 'llm'
  - *技能即记忆的范式使冻结 LLM 能够实现持续学习，无需参数更新。跨任务迁移在领域对齐的结构化基准（如 HLE）上效果最强。系统揭示了三个独立优化维度：更强 LLM、更多训练轮次、更好嵌入模型。*

- **[MemOS](./MemOS_2507.03724)** 
  - arXiv: `2507.03724` · 2026-03-27 · 'knowledge-graph' | 'scientific' | 'rag' | 'memory' | 'llm'
  - *MemOS 成功建立了以记忆为中心的系统框架，为 LLM 带来了可控性 (Controllability)、可塑性 (Plasticity) 和可演化性 (Evolvability)，为持续学习和个性化建模奠定了基础，标志着大模型从感知生成向记忆演化的范式转变。*

- **[Mem0](./Mem0_2504.19413)** 
  - arXiv: `2504.19413` · 2026-03-27 · 'memory' | 'scientific' | 'llm' | 'rag'
  - *Mem0 在保持高级推理能力的同时显著降低计算开销：p95 延迟降低 91%，token 成本节省超 90%。研究证明了结构化、持久化记忆机制对长期对话连贯性的关键作用。*

- **[EverMemOS](./EverMemOS_2601.02163)** 
  - arXiv: `2601.02163` · 2026-03-27 · 'memory' | 'scientific' | 'llm'
  - *通过将记忆建模为动态生命周期而非被动记录存储，EverMemOS 实现了从碎片化事件体验到连贯稳定知识结构的转化，为构建更一致、更具上下文感知能力的交互式代理提供了可扩展的基础。*

</div>

### 多模态 {#multimodal}

<div class="paper-list">

- **[daVinciMagiHuman](./daVinciMagiHuman_2603.21986)** 
  - arXiv: `2603.21986` · 2026-03-27 · 'speech' | 'multimodal' | 'efficiency' | 'scientific' | 'optimization' | 'vision'
  - *单流架构在音视频生成任务中可达到甚至超越复杂多流架构的性能，同时大幅简化模型设计和工程实现。完全开源的模型栈为社区研究提供了实用且可扩展的基础。*

- **[VideoDetective](./VideoDetective_2603.22285)** 
  - arXiv: `2603.22285` · 2026-03-27 · 'knowledge-graph' | 'multimodal' | 'scientific' | 'optimization' | 'rag' | 'vision' | 'llm'
  - *VideoDetective 作为即插即用的推理框架，通过整合外在查询引导先验和内在流形传播，有效补偿了模型规模限制，使开源模型在复杂推理任务上可与专有模型竞争。*

- **[PaddleOCRVL](./PaddleOCRVL_2510.14528)** 
  - arXiv: `2510.14528` · 2026-03-27 · 'ocr' | 'multimodal' | 'efficiency' | 'scientific' | 'optimization' | 'vision'
  - *PaddleOCR-VL 在页面级和元素级文档解析任务上均达到 SOTA 性能，同时保持最小资源消耗，适合实际部署。*

- **[FishAudioS2](./FishAudioS2_2603.08823)** 
  - arXiv: `2603.08823` · 2026-03-27 · 'speech' | 'multimodal' | 'scientific' | 'optimization' | 'vision' | 'llm'
  - *通过 Dual-AR 架构、双用途数据流水线和多奖励 RL 对齐，Fish Audio S2 实现了细粒度自然语言控制、长音频连贯合成和原生多说话人多轮生成能力，在开源 TTS 领域树立了新标杆。*

</div>

### 模型优化 {#optimization}

<div class="paper-list">

- **[SpecEyes](./SpecEyes_2603.23483)** 
  - arXiv: `2603.23483` · 2026-03-27 · 'ocr' | 'efficiency' | 'scientific' | 'optimization' | 'vision' | 'llm'
  - *SpecEyes 成功将推测范式从 token 级提升至 agentic 级，通过跳过不必要的工具链实现延迟降低和吞吐量提升，为 agentic MLLM 的实际部署提供了系统级解决方案。*

- **[PowerInfer](./PowerInfer_2312.12456)** 
  - arXiv: `2312.12456` · 2026-03-27 · 'efficiency' | 'scientific' | 'optimization' | 'llm' | 'quantization'
  - *PowerInfer 通过利用 LLM 推理的 locality 特性，成功在消费级 GPU 上实现高效 LLM 推理，显著降低部署成本（$2000 vs $20000），同时保持模型精度。*

- **[OmniFlatten](./OmniFlatten_2410.17799)** 
  - arXiv: `2410.17799` · 2026-03-27 · 'speech' | 'efficiency' | 'scientific' | 'optimization' | 'rag' | 'vision' | 'llm'
  - *该方法无需修改 LLM 架构或依赖计算密集型预训练，为开发高效自然的全双工语音对话系统提供了简单的建模技术和有前景的研究方向。*

- **[Bitnetcpp](./Bitnetcpp_2502.11880)** 
  - arXiv: `2502.11880` · 2026-03-27 · 'efficiency' | 'scientific' | 'optimization' | 'llm' | 'quantization'
  - *Bitnet.cpp 为 sub-2-bits-per-weight 条件下的三元 LLMs 边缘推理设立了新基准，证明了元素级方法在计算和内存访问方面优于传统 bit-wise 和 MAD-based 方法。*

- **[AttentionResiduals](./AttentionResiduals_2603.15031)** 
  - arXiv: `2603.15031` · 2026-03-27 · 'optimization' | 'llm' | 'efficiency' | 'scientific'
  - *AttnRes 通过将深度方向的信息聚合从固定权重升级为内容依赖的 softmax 注意力，完成了与序列维度从 RNN 到 Transformer 相似的范式转变。该方法可作为标准残差连接的即插即用替换，在大规模训练中实用且高效。*

</div>

### 其他 {#other}

<div class="paper-list">

- **[MetaClaw](./MetaClaw_2603.17187)** 
  - arXiv: `2603.17187` · 2026-03-27 · 'social-simulation' | 'scientific' | 'optimization' | 'other' | 'llm'
  - *MetaClaw 首次统一了技能驱动适应和策略优化，通过支持 - 查询数据分离和机会主义调度，实现了零停机的持续演化。该框架特别适用于部署中等能力模型到生产环境，可大幅缩小与前沿模型的性能差距。*

- **[AutoGaze](./AutoGaze_2603.12254)** 
  - arXiv: `2603.12254` · 2026-03-27 · 'efficiency' | 'other' | 'optimization' | 'vision' | 'llm'
  - *Attend Before Attention (AutoGaze) 双模式研读报告*

</div>

### RAG/检索增强 {#rag}

<div class="paper-list">

- **[LightRAG](./LightRAG_2410.05779)** 
  - arXiv: `2410.05779` · 2026-03-27 · 'knowledge-graph' | 'efficiency' | 'scientific' | 'rag' | 'llm'
  - *LightRAG 通过图增强索引和双层检索范式，实现了更高效、更全面的 RAG 系统，同时显著降低计算成本和响应时间。*

</div>

### 强化学习 {#rl}

<div class="paper-list">

- **[SSPO](./SSPO_2502.06855)** 
  - arXiv: `2502.06855` · 2026-03-27 · 'rl' | 'efficiency' | 'scientific' | 'optimization' | 'llm'
  - *SPO 成功实现了无需外部参考的 prompt 优化，在保持 SOTA 性能的同时大幅降低成本。该方法使 prompt 优化可应用于无标注数据的开放型任务，显著提升了实用性和可及性。*

- **[OpenClawRL](./OpenClawRL_2603.10165)** 
  - arXiv: `2603.10165` · 2026-03-27 · 'optimization' | 'rl' | 'scientific'
  - *Next-state 信号是通用的在线学习源，个人对话、终端执行、GUI 交互、SWE 任务和工具调用轨迹都可以流入同一训练循环。Binary RL 和 OPD 的组合产生显著优化增益，使模型能够同时个性化和改进长视野任务能力。*

</div>

### 世界模型 {#world_model}

<div class="paper-list">

- **[WildWorld](./WildWorld_2603.23497)** 
  - arXiv: `2603.23497` · 2026-03-27 · 'world_model' | 'vision' | 'scientific'
  - *显式状态标注对于动作条件视频生成和世界建模至关重要。现有模型在建模语义丰富动作和保持长时状态一致性方面仍面临显著挑战，需要状态感知的视频生成方法。*

- **[LeWorldModel](./LeWorldModel_2603.19312)** 
  - arXiv: `2603.19312` · 2026-03-27 · 'world_model' | 'llm' | 'scientific'
  - *AttnRes 通过深度方向的 softmax 注意力实现了选择性信息聚合，缓解了 PreNorm 稀释问题，使输出幅度有界、梯度分布更均匀。Block AttnRes 以约 8 个块即可恢复大部分 Full AttnRes 收益，是实际可用的即插即用替换方案。*

</div>

## 🏷️ 标签云

<div class="tag-cloud">

<span class="tag">'agent'</span>
<span class="tag">'distributed'</span>
<span class="tag">'efficiency'</span>
<span class="tag">'finance'</span>
<span class="tag">'framework'</span>
<span class="tag">'knowledge-graph'</span>
<span class="tag">'llm'</span>
<span class="tag">'memory'</span>
<span class="tag">'multi-agent'</span>
<span class="tag">'multimodal'</span>
<span class="tag">'ocr'</span>
<span class="tag">'optimization'</span>
<span class="tag">'other'</span>
<span class="tag">'quantization'</span>
<span class="tag">'rag'</span>
<span class="tag">'rl'</span>
<span class="tag">'scientific'</span>
<span class="tag">'social-simulation'</span>
<span class="tag">'speech'</span>
<span class="tag">'vision'</span>
<span class="tag">'world_model'</span>

</div>
