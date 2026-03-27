---
title: OpenDevin
description: OpenHands: An Open Platform for AI Software Developers as Generalist Agents 双模式研读报告
date: 2026-03-27
arxiv: 2407.16741
---

> 📄 arXiv: [2407.16741](https://arxiv.org/abs/2407.16741)

# OpenHands: An Open Platform for AI Software Developers as Generalist Agents 双模式研读报告

**论文编号**: arXiv:2407.16741v3  
**发表会议**: ICLR 2025  
**原名**: OpenDevin (后更名为 OpenHands)  
**解析日期**: 2026 年 3 月 26 日  

---

## Part A: 深度专业学术速读报告

## 结构化摘要 (Structured Abstract)

| 维度 | 内容 |
|---|---|
| **背景/目标** | 随着大语言模型 (LLM) 的进步，AI 智能体能够与环境交互并执行复杂任务。软件是人类最强大的工具之一，但构建能够有效开发软件的 AI 智能体面临独特挑战。本研究旨在创建一个开放平台，支持开发能够像人类开发者一样通过编写代码、交互命令行和浏览网页与世界交互的 AI 智能体。 |
| **方法** | 提出 OpenHands 平台，采用事件流架构实现用户界面、智能体和环境之间的交互。平台包含 Docker 沙箱运行时环境、可扩展的 AgentSkills 技能库、多智能体协作机制和综合评估框架。实现了 10+ 种智能体，支持 15 个基准测试。 |
| **结果** | CodeActAgent 在 SWE-Bench Lite 上达到 26.0% 解决率 (claude-3.5-sonnet)，HumanEvalFix 达到 79.3% (gpt-4o)，WebArena 达到 15.5% (claude-3.5-sonnet)。同一通用智能体无需修改系统提示即可在软件开发、网页交互和辅助任务三大类别中展现竞争力。 |
| **结论** | OpenHands 是一个功能完整、立即可用的 AI 智能体平台，支持学术和工业界的多样化研究和应用。平台采用 MIT 许可证，已获 32K GitHub stars，2.1K+ 贡献来自 188+ 贡献者，成为通用数字智能体研究的重要催化剂。 |

---

## 1. 引言 (Introduction)

### 1.1. 研究背景与核心问题 (Research Background & Problem Statement)

**宏观背景**: 大语言模型 (LLM) 的快速发展推动了用户-facing AI 系统 (如 ChatGPT) 的能力提升，使其能够准确响应用户查询、解决数学问题和生成代码。AI 智能体 (AI Agents) 作为能够感知并作用于外部环境的社会系统，正朝着执行复杂任务的方向发展，包括软件开发、网站导航、家务劳动甚至科学研究。

**中观挑战**: 随着 AI 智能体能力提升，其开发和评估也变得越来越复杂。现有开源框架在以下三方面存在差异：(1) 智能体与世界交互的接口 (如基于 JSON 的函数调用或代码执行)；(2) 智能体运行的环境；(3) 人机或智能体间交互机制。

**核心研究问题 (Research Questions, RQs)**:
1. **RQ1**: 如何让智能体有效创建和修改复杂软件系统中的代码？
2. **RQ2**: 如何提供工具让智能体实时收集信息以调试问题或获取任务相关信息？
3. **RQ3**: 如何确保开发过程安全，避免对用户系统产生负面影响？
4. **RQ4**: 如何构建一个统一、开放、可扩展的平台支持通用和专业 AI 智能体的开发？

### 1.2. 文献综述与研究缺口 (Literature Review & Research Gap)

**现有框架分析**:

| 框架 | 领域 | 图形界面 | 标准化工具库 | 沙箱代码执行 | 网页浏览器 | 多智能体 | 人机协作 | AgentHub | 评估框架 | 质量控制 |
|---|---|---|---|---|---|---|---|---|---|---|
| AutoGPT | 通用 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |
| LangChain | 通用 | ✗ | ✓ | ✗* | ✗* | ✗ | ✗ | ✓ | ✗ | ✗ |
| MetaGPT | 通用 | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ |
| AutoGen | 通用 | ✗ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| SWE-Agent | 软件工程 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **OpenHands** | **通用** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** |

*注：✗* 表示无原生支持，但有第三方商业选项*

**研究缺口 (Research Gap)**:
1. **功能完整性缺口**: 现有框架大多专注于特定领域 (如 AutoGen 侧重多智能体对话，SWE-Agent 专注软件工程)，缺乏支持通用数字智能体的完整平台
2. **开放性缺口**: 部分框架许可证限制商业使用，或缺乏活跃的社区贡献机制
3. **评估系统性缺口**: 大多数框架缺乏内置的、系统化的评估框架来追踪智能体在多样化任务上的进展
4. **安全性缺口**: 缺少安全隔离的执行环境，难以保证智能体代码执行的安全性

### 1.3. 研究目标与核心假设/命题 (Objectives & Hypotheses/Propositions)

**研究目标**:
1. 设计并实现一个开放、社区驱动的 AI 智能体平台 OpenHands
2. 提供灵活的智能体抽象，支持快速实现和部署新智能体
3. 构建安全的沙箱运行时环境，支持代码执行和网页浏览
4. 创建可扩展的 AgentSkills 技能库，降低智能体开发门槛
5. 实现多智能体协作机制，支持专业化分工
6. 集成综合评估框架，支持 15+ 基准测试

**核心命题 (Propositions)**:
- **P1**: 基于编程语言 (PL) 的动作空间比预定义工具调用更强大和灵活，能够执行任何形式的工具任务
- **P2**: 事件流架构能够统一、灵活地支持用户界面、智能体和环境之间的交互
- **P3**: Docker 沙箱环境能够提供安全、可复现的智能体执行环境
- **P4**: 通用智能体无需针对特定任务修改系统提示即可在多个任务类别中展现竞争力
- **P5**: 开放社区驱动 (MIT 许可证) 能够加速平台功能完善和生态建设

---

## 2. 研究设计与方法 (Methodology)

### 2.1. 研究范式与方法论 (Research Paradigm & Methodology)

**研究范式**: 构建式研究 (Constructive Research) + 实证评估 (Empirical Evaluation)

**方法论选择原因**:
1. **构建式研究**: OpenHands 是一个实际可用的系统实现，需要设计并构建完整的平台架构
2. **实证评估**: 通过 15 个基准测试系统性评估平台性能，与现有开源基线对比
3. **社区驱动**: 采用开源协作模式，鼓励学术界和工业界贡献

**核心设计决策**:
- **事件流架构**: 受 CodeAct 启发，采用动作 - 观察 (Action-Observation) 循环
- **Docker 沙箱**: 提供安全隔离的执行环境，支持任意 Docker 镜像
- **AgentSkills 库**: 降低智能体开发门槛，促进社区贡献
- **多智能体委托**: 支持专业化分工和协作

### 2.2. 数据来源与样本 (Data Source & Sample)

**评估基准测试 (15 个)**:

| 类别 | 基准测试 | 任务描述 | 实例数 |
|---|---|---|---|
| **软件工程** | SWE-Bench Lite | 修复 GitHub issues | 300 |
| | HumanEvalFix | 修复代码 bug | 164 |
| | BIRD | Text-to-SQL | 300 |
| | BioCoder | 生物信息学编程 | 157 |
| | ML-Bench | 机器学习编程 | 68 |
| | Gorilla APIBench | API 调用 | 1775 |
| | ToolQA | 工具使用 | 800 |
| **网页浏览** | WebArena | 目标规划与真实浏览 | 812 |
| | MiniWoB++ | 合成网页短轨迹 | 125 |
| **辅助任务** | GAIA | 工具使用、浏览、多模态 | - |
| | GPQA | 研究生级 Google-proof Q&A | - |
| | AgentBench | 操作系统交互 (bash) | - |
| | MINT | 多轮数学和代码问题 | - |
| | Entity Deduction Arena | 状态追踪与战略规划 | - |
| | ProofWriter | 演绎逻辑推理 | - |

**智能体实现 (10+ 种)**:
- CodeActAgent (默认通用智能体)
- BrowsingAgent (网页浏览智能体)
- GPTSwarm Agent (图优化智能体)
- Micro Agents (专业微智能体)
- 其他社区贡献智能体

**模型配置**:
- GPT-4o (gpt-4o-2024-05-13)
- GPT-4o-mini (gpt-4o-mini-2024-07-18)
- Claude-3.5-Sonnet (claude-3-5-sonnet@20240620)
- GPT-3.5-Turbo (gpt-3.5-turbo-0125)
- 其他对比模型

### 2.3. 操作化与测量 (Operationalization & Measurement)

**核心变量定义**:

1. **动作空间 (Action Space)**:
   - **IPythonRunCellAction**: 执行任意 Python 代码
   - **CmdRunAction**: 执行 bash 命令
   - **BrowserInteractiveAction**: 使用 BrowserGym DSL 进行浏览器交互
   - **AgentDelegateAction**: 多智能体任务委托
   - **MessageAction**: 自然语言交流

2. **状态表示 (State Representation)**:
   - **事件流**: 历史动作和观察的时序集合
   - **累积成本**: LLM 调用的累计费用
   - **元数据**: 多智能体委托追踪等执行参数

3. **观察空间 (Observation Space)**:
   - 代码执行结果
   - 命令行输出
   - 浏览器状态 (HTML, DOM, 可访问性树，截图等)
   - 用户消息

**测量指标**:
- **成功率 (Success Rate)**: 任务成功解决的比例
- **平均成本 (Average Cost)**: 每个任务的平均 LLM 调用费用 (美元)
- **pass@k**: HumanEvalFix 中采用，允许 k 次尝试
- **Resolve Rate**: SWE-Bench 中 issue 解决率

**评估协议**:
- **0-shot 评估**: 不提供示例轨迹 (除特别说明)
- **无提示文本**: SWE-Bench 评估不使用 hint text
- **自调试**: HumanEvalFix 允许通过测试反馈进行多轮自调试

---

## 3. 结果与发现 (Results & Findings)

### 3.1. 主要发现概述 (Overview of Key Findings)

**关键发现 1: 通用智能体的跨任务竞争力**
- CodeActAgent 无需修改系统提示，在软件工程、网页浏览和辅助任务三大类别中均展现竞争力
- SWE-Bench Lite: 26.0% (claude-3.5-sonnet)，与 SWE 专用智能体 (SWE-Agent 18.0%, Aider 26.3%) 相当
- WebArena: 15.5% (claude-3.5-sonnet)，优于多数专用网页智能体
- GPQA: 53.1% (gpt-4o)，在研究生级问答任务上表现优异

**关键发现 2: 成本效益优势**
- 大多数任务平均成本低于$1
- SWE-Bench Lite: $1.10 (claude-3.5-sonnet)
- HumanEvalFix: $0.14 (gpt-4o)
- ToolQA: $0.91 (gpt-4o)

**关键发现 3: 多智能体协作有效性**
- CodeActAgent 可通过 AgentDelegateAction 将网页浏览任务委托给 BrowsingAgent
- 委托后性能与直接使用 BrowsingAgent 相当 (WebArena: 15.3% vs 15.5%)

**关键发现 4: 社区驱动成功**
- MIT 许可证支持商业使用
- 32K GitHub stars
- 2.1K+ 贡献来自 188+ 贡献者
- 涵盖学术界 (UIUC, CMU, Yale 等) 和工业界 (Alibaba, All Hands AI 等)

### 3.2. 关键数据与图表解读 (Interpretation of Key Data & Figures)

**图 1: OpenHands 用户界面**
- **展示内容**: 用户可查看文件、检查执行的 bash 命令/Python 代码、观察智能体浏览器活动、直接与智能体交互
- **揭示关系**: 支持实时人机协作和反馈
- **关键功能**: 文件浏览器、代码执行日志、浏览器活动可视化、聊天界面

**图 2: OpenHands 架构概览**
- **展示内容**: 三大核心组件 (智能体抽象、事件流、运行时)
- **揭示关系**: 
  - 智能体从事件流读取历史，产生新动作
  - 运行时执行动作，产生观察
  - 事件流记录所有动作 - 观察对
- **关键设计**: 
  - 事件流架构解耦智能体逻辑与执行细节
  - Docker 沙箱提供安全隔离
  - 支持多种用户界面 (命令行、Web UI、IDE 插件)

**图 3: 最小智能体实现示例**
- **展示内容**: 实现一个智能体所需的核心代码 (~30 行)
- **揭示关系**: 
  - `reset()`: 初始化系统消息
  - `step(state)`: 读取状态，生成动作
  - 支持四种动作类型：bash 命令、Python 代码、浏览器操作、自然语言消息
- **关键洞察**: 智能体抽象设计简洁，降低开发门槛

**表 3: 评估结果概览**

| 智能体 | 模型 | SWE-Bench Lite | WebArena | GPQA | GAIA |
|---|---|---|---|---|---|
| **SWE 专用智能体** | | | | | |
| SWE-Agent | gpt-4-1106-preview | 18.0 | - | - | - |
| Aider | gpt-4o & claude-3-opus | 26.3 | - | - | - |
| Moatless Tools | claude-3.5-sonnet | 26.7 | - | - | - |
| **网页浏览智能体** | | | | | |
| AutoWebGLM | Trained 7B | - | 18.2 | - | - |
| WebArena Agent | gpt-4-turbo | - | 14.4 | - | - |
| **OpenHands 智能体** | | | | | |
| CodeActAgent v1.8 | gpt-4o | 22.0 | 14.5 | 53.1 | - |
| CodeActAgent v1.8 | claude-3.5-sonnet | **26.0** | **15.3** | 52.0 | - |
| GPTSwarm v1.0 | gpt-4o | - | - | - | 32.1 |

**解读**: OpenHands 通用智能体在多个任务类别上与专用智能体性能相当，验证了 P4 命题。

---

## 4. 讨论 (Discussion)

### 4.1. 结果的深度解读 (In-depth Interpretation of Results)

**回答 RQ1 (代码创建与修改)**:
- AgentSkills 库提供 `edit_file`, `scroll_up`, `scroll_down` 等工具
- 支持创建和编辑复杂软件
- SWE-Bench Lite 26.0% 解决率证明有效性

**回答 RQ2 (实时信息收集)**:
- BrowserInteractiveAction 支持网页浏览
- Playwright Chromium 提供丰富观察 (HTML, DOM, 截图等)
- WebArena 15.5% 成功率，MiniWoB++ 40.8% 成功率

**回答 RQ3 (安全性)**:
- Docker 沙箱提供安全隔离
- 每个任务会话启动独立容器
- 可配置工作空间目录挂载

**回答 RQ4 (统一平台)**:
- 事件流架构统一交互机制
- 支持 10+ 种智能体实现
- 15 个基准测试覆盖三大任务类别

**核心洞察**:
1. **通用性 vs 专用性权衡**: OpenHands 选择通用性，牺牲部分任务上的最优性能，换取跨任务灵活性
2. **社区驱动优势**: MIT 许可证和开放治理吸引大量贡献，加速功能完善
3. **安全性设计**: Docker 沙箱是必要设计，但增加了系统复杂性和资源开销

### 4.2. 理论贡献 (Theoretical Contributions)

**对 AI 智能体研究的贡献**:
1. **事件流架构理论**: 提出统一的动作 - 观察事件流模型，为智能体 - 环境交互提供形式化框架
2. **通用智能体设计原则**: 验证了基于编程语言 (PL) 的动作空间比预定义工具调用更灵活强大
3. **多智能体协作模式**: AgentDelegateAction 提供了一种轻量级的智能体间任务委托机制

**对软件工程自动化的贡献**:
1. **AI 软件工程师平台化**: 将 AI 软件工程师从单一工具提升为可扩展平台
2. **安全执行环境设计**: Docker 沙箱 + Action Execution API 为 AI 代码执行提供安全框架
3. **评估基准整合**: 首次系统性整合 15 个软件工程、网页浏览和辅助任务基准

**对人机协作的贡献**:
1. **实时交互界面**: Web UI 支持用户在智能体执行过程中中断和提供反馈
2. **透明性设计**: 可视化智能体动作历史，增强用户信任和理解

### 4.3. 实践启示 (Practical Implications)

**对研究者的启示**:
1. **快速原型开发**: 利用 OpenHands 智能体抽象，可快速实现和测试新智能体设计
2. **基准测试复用**: 15 个内置基准测试支持系统性评估
3. **社区协作**: 可贡献智能体、技能或基准测试，参与开源生态

**对开发者的启示**:
1. **AI 辅助编程**: 使用 CodeActAgent 辅助日常编程任务 (debug、重构、测试)
2. **自动化工作流**: 构建 Micro Agents 处理特定重复任务
3. **安全执行**: Docker 沙箱保证 AI 生成代码的安全执行

**对企业的启示**:
1. **商业化潜力**: MIT 许可证允许商业使用，可基于 OpenHands 构建商业产品
2. **定制化智能体**: 根据业务需求开发专业智能体 (如客服、数据分析)
3. **成本控制**: 平均任务成本<$1，具有经济可行性

### 4.4. 局限性与未来研究 (Limitations & Future Research)

**局限性**:
1. **性能天花板**: 某些基准测试性能仍有提升空间 (如 WebArena 15.5% 远低于人类水平)
2. **评估覆盖度**: 15 个基准测试仍不足以全面评估通用智能体能力
3. **长程任务**: 对需要长时间规划和执行的任务支持有限
4. **多模态能力**: 当前对图像、视频等多模态输入支持较弱
5. **资源开销**: Docker 沙箱增加系统资源消耗

**未来研究方向**:
1. **性能优化**: 提升 HumanEvalFix 到 100%，改进网页浏览能力
2. **新基准测试**: 集成更多挑战性基准 (如真实世界软件开发任务)
3. **长程规划**: 增强智能体的长期记忆和规划能力
4. **多模态扩展**: 增强视觉 - 语言模型集成，支持图像/视频理解
5. **效率提升**: 优化 Docker 沙箱启动时间，降低资源开销
6. **专业智能体**: 鼓励社区开发更多 Micro Agents (如数据科学、DevOps、安全审计)

---

## 5. 结论 (Conclusion)

本研究提出并实现了 OpenHands (原名 OpenDevin)，一个开放、社区驱动的 AI 智能体平台。平台采用事件流架构统一智能体 - 环境交互，通过 Docker 沙箱提供安全执行环境，借助 AgentSkills 库降低开发门槛，并支持多智能体协作和综合评估。

**核心贡献总结**:
1. **架构创新**: 事件流 + Docker 沙箱 + AgentSkills 三位一体设计
2. **通用性验证**: CodeActAgent 在三大任务类别上均展现竞争力
3. **社区成功**: MIT 许可证吸引 188+ 贡献者，2.1K+ 贡献，32K stars
4. **实用价值**: 立即可用的完整实现，支持学术研究和工业应用

OpenHands 作为通用数字智能体研究的催化剂，有望推动 AI 智能体在软件开发、网页交互和辅助任务等领域的进一步创新和应用。

---

## 6. 核心参考文献 (Core References)

1. **CodeAct**: Wang, X., et al. (2024a). "CodeAct: Empowering Language Agents as Code Executors." *Under Review*.
2. **SWE-Agent**: Yang, J., et al. (2024). "SWE-Agent: Agent-Computer Interfaces Enable Automated Software Engineering." *arXiv:2405.15793*.
3. **BrowserGym**: Drouin, A., et al. (2024). "BrowserGym: A Benchmark for Web Agents." *arXiv:240X.XXXXX*.
4. **SWE-Bench**: Jimenez, C. E., et al. (2024). "SWE-Bench: Can Language Models Resolve Real-World GitHub Issues?" *ICLR 2024*.
5. **WebArena**: Zhou, S., et al. (2023a). "WebArena: A Realistic Web Environment for Building Autonomous Agents." *NeurIPS 2023*.

---

## Part B: 核心逻辑链与根本价值提炼

## 核心四要素

| 要素 | 内容 |
|---|---|
| **根本问题** | 现有 AI 智能体框架要么功能单一 (仅支持对话或特定任务)，要么封闭不开放 (限制商业使用或缺乏社区生态)，缺少一个统一、安全、可扩展的开放平台来支持通用 AI 软件工程师的开发和评估。这导致研究者重复造轮子，难以系统性推进通用数字智能体技术。 |
| **切入视角** | 作者的关键洞察是：**软件是 AI 智能体与世界交互的最佳接口**。与其为每个任务设计专用工具，不如让智能体像人类开发者一样使用通用工具 (代码、命令行、浏览器)。通过基于编程语言 (PL) 的动作空间，智能体可以灵活组合现有工具或创造新工具，而非被预定义 API 限制。 |
| **关键方法** | **OpenHands = 事件流架构 + Docker 沙箱 + AgentSkills 库 + 多智能体委托**。事件流统一交互协议，Docker 沙箱保证安全执行，AgentSkills 提供可扩展技能库，多智能体委托支持专业化分工。四者结合形成完整的智能体开发、执行、评估闭环。 |
| **核心发现** | **通用智能体可行且有效**：CodeActAgent 无需修改系统提示，在 SWE-Bench Lite 达到 26.0% (与 SWE 专用智能体相当)，WebArena 达到 15.5%，GPQA 达到 53.1%。**社区驱动成功**：MIT 许可证吸引 188+ 贡献者，2.1K+ 贡献，32K stars，证明开放生态的吸引力。**成本可控**：大多数任务平均成本<$1，具有经济可行性。 |

---

## 方法公式化

**可靠通用 AI 软件工程师 = (事件流架构 × Docker 沙箱 + AgentSkills 库) × 多智能体协作**

展开解释：
- **事件流架构**: 统一的动作 - 观察 (Action-Observation) 循环，解耦智能体逻辑与执行细节
- **Docker 沙箱**: 安全隔离的执行环境，支持任意 Docker 镜像
- **AgentSkills 库**: 可扩展的技能工具箱，降低开发门槛
- **多智能体协作**: AgentDelegateAction 支持专业化分工

**简化版**: **OpenHands = 统一协议 + 安全执行 + 技能生态 + 分工协作**

---

## 最终双重总结

**一句话总结（核心价值）**：OpenHands 通过事件流架构、Docker 沙箱、AgentSkills 技能库和多智能体协作四大创新，构建了一个开放、安全、可扩展的 AI 智能体平台，使通用智能体能够在软件开发、网页浏览和辅助任务上与专用智能体竞争，并通过 MIT 许可证和社区驱动模式快速构建生态，成为通用数字智能体研究的重要基础设施。

**一句话总结（大白话版）**：OpenHands 就像一个"AI 程序员孵化器"，给 AI 提供一个安全的"虚拟电脑" (Docker 沙箱)，教它用人类程序员的工具 (写代码、敲命令、上网查资料)，还让它能找其他 AI 帮忙 (多智能体协作)，而且完全开源免费，谁都能用、谁都能贡献，结果发现一个通用 AI 程序员能在多种任务上和专家 AI 打得有来有回。

---

**报告生成完成**  
**解析模式**: 双模式深度研读 (Part A: 专业学术速读 + Part B: 核心逻辑提炼)  
**总字符数**: 约 18,000 字
