---
title: 论文研读
description: AI 论文研读报告集合
outline: false
---

# 📚 论文研读

本页面收录了 AI 领域的论文研读报告，涵盖 Agent、RAG、多模态、模型优化等方向。

<script setup>
import { ref, computed } from 'vue'
import PaperFilters from '../../.vitepress/theme/components/PaperFilters.vue'
import PaperCard from '../../.vitepress/theme/components/PaperCard.vue'

// 论文数据
const allPapers = ref([
  {
    title: 'OpenDevin: An Open Platform for AI Software Developers as Generalist Agents',
    link: './OpenDevin_2407.16741',
    category: 'Agent',
    tags: ['multi-agent', 'social-simulation', 'scientific', 'llm', 'agent'],
    date: '2026-03-27',
    summary: 'OpenHands 是一个功能完整、立即可用的 AI 智能体平台，支持学术和工业界的多样化研究和应用。'
  },
  {
    title: 'MiroThinker: Learning to Think with a Whiteboard',
    link: './MiroThinker_2511.11793',
    category: 'Agent',
    tags: ['optimization', 'llm', 'agent', 'scientific'],
    date: '2026-03-27',
    summary: '交互深度展现出与模型规模和上下文长度类似的扩展行为，是构建下一代开源研究智能体的第三个关键维度。'
  },
  {
    title: 'HyperAgents: A Unified Framework for Agentic Self-Improvement',
    link: './Hyperagents_2603.19461',
    category: 'Agent',
    tags: ['social-simulation', 'scientific', 'optimization', 'rag', 'agent'],
    date: '2026-03-27',
    summary: 'HyperAgents 首次实现了不依赖对齐假设的通用自改进框架，元认知自改进使系统能够改进"如何改进"的能力。'
  },
  {
    title: 'EvoScientist: Evolving Multi-Agent Systems for Scientific Discovery',
    link: './EvoScientist_2603.08127',
    category: 'Agent',
    tags: ['multi-agent', 'social-simulation', 'scientific', 'llm', 'agent'],
    date: '2026-03-27',
    summary: '持久记忆和多智能体演化机制能有效提升科学想法质量和代码执行可靠性。'
  },
  {
    title: 'AutoDev: Automated Software Development with LLM Agents',
    link: './AutoDev_2403.08299',
    category: 'Agent',
    tags: ['llm', 'agent', 'scientific'],
    date: '2026-03-27',
    summary: 'AutoDev 显著提升了 LLM 在软件工程任务中的性能，同时保持了安全和用户可控的开发环境。'
  },
  {
    title: 'AgentScope: A Flexible and Efficient Multi-Agent Framework',
    link: './AgentScope_2407.17789',
    category: 'Agent',
    tags: ['multi-agent', 'social-simulation', 'efficiency', 'scientific', 'distributed', 'llm', 'agent'],
    date: '2026-03-27',
    summary: 'AgentScope 的增强功能有效解决了大规模多智能体模拟的可扩展性、效率和效率问题。'
  },
  {
    title: 'AgentScope 1.0: A Practical Platform for Building Scalable Multi-Agent Applications',
    link: './AgentScope10_2508.16279',
    category: 'Agent',
    tags: ['multi-agent', 'efficiency', 'scientific', 'optimization', 'llm', 'agent'],
    date: '2026-03-27',
    summary: 'AgentScope 1.0 为构建可扩展、自适应、高效的智能体应用提供了实用基础。'
  },
  {
    title: 'The AI Scientist-v2: Workshop-Level Automated Scientific Discovery',
    link: './AIScientistv2_2504.08066',
    category: 'Agent',
    tags: ['scientific', 'vision', 'agent', 'llm'],
    date: '2026-03-27',
    summary: 'The AI Scientist-v2 成功实现了 workshop 级别的自动科学发现，标志着 AI 生成研究通过同行评审的重要里程碑。'
  },
  {
    title: 'TradingAgents: Multi-Agent LLM Framework for Financial Trading',
    link: './TradingAgents_2412.20138',
    category: 'Finance',
    tags: ['multi-agent', 'social-simulation', 'scientific', 'finance', 'llm'],
    date: '2026-03-27',
    summary: '多 agent LLM 框架通过模拟真实交易公司的协作动态和采用结构化通信协议，能显著提升交易性能。'
  },
  {
    title: 'SmolDocling: Small Models for Document Understanding',
    link: './SmolDocling_2503.11576',
    category: 'Framework',
    tags: ['ocr', 'framework', 'efficiency', 'scientific', 'optimization', 'vision', 'llm'],
    date: '2026-03-27',
    summary: '证明小模型通过统一优化的输出格式可与大模型竞争，为资源高效的多任务文档理解开辟新路径。'
  },
  {
    title: 'MinerUDiffusion: Diffusion-Based Document OCR',
    link: './MinerUDiffusion_2603.22458',
    category: 'Framework',
    tags: ['ocr', 'framework', 'efficiency', 'scientific', 'vision'],
    date: '2026-03-27',
    summary: '扩散解码是文档 OCR 的有前景的替代方案，在保持高识别准确率的同时显著提升长序列推理效率。'
  },
  {
    title: 'MinerU 2.5: A Comprehensive Document Parsing Tool',
    link: './MinerU2.5_2509.22186',
    category: 'Framework',
    tags: ['ocr', 'framework', 'efficiency', 'scientific', 'optimization', 'rag', 'vision', 'llm'],
    date: '2026-03-27',
    summary: 'MinerU2.5 通过解耦架构成功解决了文档解析中性能与效率的权衡问题。'
  },
  {
    title: 'LlamaFactory: Unified Efficient Fine-Tuning of LLMs',
    link: './LlamaFactory_2403.13372',
    category: 'Framework',
    tags: ['framework', 'efficiency', 'scientific', 'distributed', 'llm'],
    date: '2026-03-27',
    summary: 'LlamaFactory 通过模块化设计最小化了模型、数据集和训练方法之间的依赖，显著降低了 LLM 微调的门槛。'
  },
  {
    title: 'LTX-2: A Unified Framework for Text-to-Audio-Video Generation',
    link: './LTX2_2601.03233',
    category: 'Framework',
    tags: ['speech', 'framework', 'efficiency', 'scientific', 'optimization', 'vision'],
    date: '2026-03-27',
    summary: 'LTX-2 建立了新的开源 T2AV 生成基础，以前所未有的速度生成连贯、富有表现力且细节丰富的音视频内容。'
  },
  {
    title: 'MementoSkills: Skills as Memory for Continuous Learning',
    link: './MementoSkills_2603.18743',
    category: 'Memory',
    tags: ['optimization', 'memory', 'scientific', 'llm'],
    date: '2026-03-27',
    summary: '技能即记忆的范式使冻结 LLM 能够实现持续学习，无需参数更新。'
  },
  {
    title: 'MemOS: A Memory-Centric System Framework for LLMs',
    link: './MemOS_2507.03724',
    category: 'Memory',
    tags: ['knowledge-graph', 'scientific', 'rag', 'memory', 'llm'],
    date: '2026-03-27',
    summary: 'MemOS 成功建立了以记忆为中心的系统框架，为 LLM 带来了可控性、可塑性和可演化性。'
  },
  {
    title: 'Mem0: A Structured Memory Layer for LLMs',
    link: './Mem0_2504.19413',
    category: 'Memory',
    tags: ['memory', 'scientific', 'llm', 'rag'],
    date: '2026-03-27',
    summary: 'Mem0 在保持高级推理能力的同时显著降低计算开销，p95 延迟降低 91%，token 成本节省超 90%。'
  },
  {
    title: 'EverMemOS: Dynamic Memory Lifecycle Management',
    link: './EverMemOS_2601.02163',
    category: 'Memory',
    tags: ['memory', 'scientific', 'llm'],
    date: '2026-03-27',
    summary: '通过将记忆建模为动态生命周期而非被动记录存储，EverMemOS 实现了从碎片化事件体验到连贯稳定知识结构的转化。'
  },
  {
    title: 'daVinciMagiHuman: Unified Audio-Video Generation',
    link: './daVinciMagiHuman_2603.21986',
    category: 'Multimodal',
    tags: ['speech', 'multimodal', 'efficiency', 'scientific', 'optimization', 'vision'],
    date: '2026-03-27',
    summary: '单流架构在音视频生成任务中可达到甚至超越复杂多流架构的性能，同时大幅简化模型设计。'
  },
  {
    title: 'VideoDetective: A Video Reasoning Framework with Knowledge Priors',
    link: './VideoDetective_2603.22285',
    category: 'Multimodal',
    tags: ['knowledge-graph', 'multimodal', 'scientific', 'optimization', 'rag', 'vision', 'llm'],
    date: '2026-03-27',
    summary: 'VideoDetective 通过整合外在查询引导先验和内在流形传播，有效补偿了模型规模限制。'
  },
  {
    title: 'PaddleOCR-VL: A Comprehensive OCR Toolkit',
    link: './PaddleOCRVL_2510.14528',
    category: 'Multimodal',
    tags: ['ocr', 'multimodal', 'efficiency', 'scientific', 'optimization', 'vision'],
    date: '2026-03-27',
    summary: 'PaddleOCR-VL 在页面级和元素级文档解析任务上均达到 SOTA 性能，同时保持最小资源消耗。'
  },
  {
    title: 'Fish Audio S2: Advanced Text-to-Speech System',
    link: './FishAudioS2_2603.08823',
    category: 'Multimodal',
    tags: ['speech', 'multimodal', 'scientific', 'optimization', 'vision', 'llm'],
    date: '2026-03-27',
    summary: '通过 Dual-AR 架构、双用途数据流水线和多奖励 RL 对齐，Fish Audio S2 实现了细粒度自然语言控制。'
  },
  {
    title: 'SpecEyes: Speculative Agentic MLLM Inference',
    link: './SpecEyes_2603.23483',
    category: 'Optimization',
    tags: ['ocr', 'efficiency', 'scientific', 'optimization', 'vision', 'llm'],
    date: '2026-03-27',
    summary: 'SpecEyes 成功将推测范式从 token 级提升至 agentic 级，通过跳过不必要的工具链实现延迟降低。'
  },
  {
    title: 'PowerInfer: Efficient LLM Inference on Consumer GPUs',
    link: './PowerInfer_2312.12456',
    category: 'Optimization',
    tags: ['efficiency', 'scientific', 'optimization', 'llm', 'quantization'],
    date: '2026-03-27',
    summary: 'PowerInfer 通过利用 LLM 推理的 locality 特性，成功在消费级 GPU 上实现高效 LLM 推理。'
  },
  {
    title: 'OmniFlatten: Full-Duplex Speech Conversation System',
    link: './OmniFlatten_2410.17799',
    category: 'Optimization',
    tags: ['speech', 'efficiency', 'scientific', 'optimization', 'rag', 'vision', 'llm'],
    date: '2026-03-27',
    summary: '该方法无需修改 LLM 架构或依赖计算密集型预训练，为开发高效自然的全双工语音对话系统提供了简单的建模技术。'
  },
  {
    title: 'Bitnet.cpp: Ternary LLM Inference on Edge Devices',
    link: './Bitnetcpp_2502.11880',
    category: 'Optimization',
    tags: ['efficiency', 'scientific', 'optimization', 'llm', 'quantization'],
    date: '2026-03-27',
    summary: 'Bitnet.cpp 为 sub-2-bits-per-weight 条件下的三元 LLMs 边缘推理设立了新基准。'
  },
  {
    title: 'AttentionResiduals: Content-Dependent Information Aggregation',
    link: './AttentionResiduals_2603.15031',
    category: 'Optimization',
    tags: ['optimization', 'llm', 'efficiency', 'scientific'],
    date: '2026-03-27',
    summary: 'AttnRes 通过将深度方向的信息聚合从固定权重升级为内容依赖的 softmax 注意力，完成了范式转变。'
  },
  {
    title: 'MetaClaw: Unified Skill Adaptation and Policy Optimization',
    link: './MetaClaw_2603.17187',
    category: 'Other',
    tags: ['social-simulation', 'scientific', 'optimization', 'other', 'llm'],
    date: '2026-03-27',
    summary: 'MetaClaw 首次统一了技能驱动适应和策略优化，通过支持查询数据分离和机会主义调度，实现了零停机的持续演化。'
  },
  {
    title: 'AutoGaze: Attend Before Attention',
    link: './AutoGaze_2603.12254',
    category: 'Other',
    tags: ['efficiency', 'other', 'optimization', 'vision', 'llm'],
    date: '2026-03-27',
    summary: 'Attend Before Attention (AutoGaze) 双模式研读报告'
  },
  {
    title: 'LightRAG: Simple and Fast Retrieval-Augmented Generation',
    link: './LightRAG_2410.05779',
    category: 'RAG',
    tags: ['knowledge-graph', 'efficiency', 'scientific', 'rag', 'llm'],
    date: '2026-03-27',
    summary: 'LightRAG 通过图增强索引和双层检索范式，实现了更高效、更全面的 RAG 系统。'
  },
  {
    title: 'SSPO: Self-Improving Prompt Optimization',
    link: './SSPO_2502.06855',
    category: 'RL',
    tags: ['rl', 'efficiency', 'scientific', 'optimization', 'llm'],
    date: '2026-03-27',
    summary: 'SPO 成功实现了无需外部参考的 prompt 优化，在保持 SOTA 性能的同时大幅降低成本。'
  },
  {
    title: 'OpenClawRL: Open-Source Reinforcement Learning for Robotic Manipulation',
    link: './OpenClawRL_2603.10165',
    category: 'RL',
    tags: ['optimization', 'rl', 'scientific'],
    date: '2026-03-27',
    summary: 'Next-state 信号是通用的在线学习源，Binary RL 和 OPD 的组合产生显著优化增益。'
  },
  {
    title: 'WildWorld: Explicit State Annotation for World Modeling',
    link: './WildWorld_2603.23497',
    category: 'World Model',
    tags: ['world_model', 'vision', 'scientific'],
    date: '2026-03-27',
    summary: '显式状态标注对于动作条件视频生成和世界建模至关重要。'
  },
  {
    title: 'LeWorldModel: Learning World Models from Video',
    link: './LeWorldModel_2603.19312',
    category: 'World Model',
    tags: ['world_model', 'llm', 'scientific'],
    date: '2026-03-27',
    summary: 'AttnRes 通过深度方向的 softmax 注意力实现了选择性信息聚合，缓解了 PreNorm 稀释问题。'
  }
])

// 筛选后的论文
const filteredPapers = ref(allPapers.value)

// 处理筛选事件
function handleFilter(papers) {
  filteredPapers.value = papers
}

// 按分类分组
const papersByCategory = computed(() => {
  const groups = {}
  filteredPapers.value.forEach(paper => {
    if (!groups[paper.category]) {
      groups[paper.category] = []
    }
    groups[paper.category].push(paper)
  })
  return groups
})

// 统计信息
const stats = computed(() => {
  const categories = {}
  allPapers.value.forEach(p => {
    categories[p.category] = (categories[p.category] || 0) + 1
  })
  return {
    total: allPapers.value.length,
    categories: Object.keys(categories).length,
    byCategory: categories
  }
})

// 论文数量
const papersCount = computed(() => filteredPapers.value.length)
</script>

## 📊 统计信息

<div class="paper-stats">

- **总计**: {{ stats.total }} 篇论文
- **分类**: {{ stats.categories }} 个类别

<div class="category-grid">
  <div v-for="(count, category) in stats.byCategory" :key="category" class="category-stat">
    <span class="category-name">{{ category }}</span>
    <span class="category-count">{{ count }}</span>
  </div>
</div>

</div>

## 🔍 筛选与搜索

<PaperFilters :papers="allPapers" @filter="handleFilter" />

<div class="papers-count">当前显示 {{ papersCount }} 篇论文</div>

## 📁 分类目录

<div v-if="Object.keys(papersByCategory).length === 0" class="no-results">
  没有找到匹配的论文，请调整筛选条件
</div>

<div v-for="(papers, category) in papersByCategory" :key="category" class="category-section">
  <h3 :id="category.toLowerCase()">{{ category }}</h3>
  <div class="paper-grid">
    <PaperCard
      v-for="paper in papers"
      :key="paper.link"
      :paper="paper"
    />
  </div>
</div>

<style scoped>
.paper-stats {
  background: var(--vp-c-bg-soft);
  padding: var(--vp-space-6);
  border-radius: var(--vp-radius-xl);
  margin-bottom: var(--vp-space-8);
}

.papers-count {
  text-align: right;
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  margin-bottom: var(--vp-space-4);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: var(--vp-space-3);
  margin-top: var(--vp-space-4);
}

.category-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--vp-space-3);
  background: var(--vp-c-bg);
  border-radius: var(--vp-radius-md);
  border: 1px solid var(--vp-c-divider);
}

.category-name {
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
  font-weight: 500;
}

.category-count {
  font-size: 1.5rem;
  font-weight: 700;
  background: var(--vp-gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.category-section {
  margin-bottom: var(--vp-space-10);
}

.category-section h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: var(--vp-space-4);
  padding-bottom: var(--vp-space-2);
  border-bottom: 2px solid var(--vp-c-divider);
}

.paper-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--vp-space-4);
}

.no-results {
  text-align: center;
  padding: var(--vp-space-12);
  color: var(--vp-c-text-2);
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .paper-grid {
    grid-template-columns: 1fr;
  }

  .category-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .paper-stats {
    padding: var(--vp-space-4);
  }
}
</style>
