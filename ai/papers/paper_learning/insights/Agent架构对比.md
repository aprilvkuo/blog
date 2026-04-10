---
title: Agent 架构对比
type: comparison
---

# Agent 架构对比

阶段一三篇论文 + DeerFlow + OpenClaw 的架构设计对比：OpenDevin、AgentScope、LlamaFactory、DeerFlow、OpenClaw。

> 💡 **扩展对比**: 详见 [[DeerFlow vs OpenClaw对比]]，聚焦 DeerFlow 与 OpenClaw (338K+ Stars) 的深度对比。

---

## 核心架构对比

| 维度 | OpenDevin | AgentScope | LlamaFactory | **DeerFlow 2.0** | **OpenClaw** |
|------|-----------|------------|--------------|------------------|--------------|
| **定位** | 通用 AI 软件工程师 | 大规模社会模拟 | LLM 微调平台 | **AI 工作站（Harness）** | **个人 AI 助手平台** |
| **Stars** | ~50K | ~5K | ~30K | ~2K | **338K+** 🦞 |
| **核心架构** | Event Stream | Actor 分布式 | 三模块 | **LangGraph + Skills** | **Gateway + Nodes** |
| **并行机制** | Docker 沙箱隔离 | Actor 进程隔离 | 无（单机训练） | Sub-Agent 并行 | 串行为主 |
| **扩展上限** | ~10 Agent | **100万 Agent** | 100+ 模型 | ~100 Sub-Agent | 单用户 |
| **交互方式** | 代码/命令行/浏览器 | 消息传递 | 配置文件/Web UI | Web + Telegram + Slack | **20+ 消息渠道** |
| **长期记忆** | ❌ 无 | ❌ 无 | ❌ 无 | ✅ 跨会话记忆 | ⚠️ workspace 文件 |
| **技能系统** | AgentSkills（工具） | 无 | 无 | Skills（工作流） | **5400+ ClawHub** |
| **语音交互** | ❌ | ❌ | ❌ | ❌ | **✅ Voice Wake + Talk** |
| **移动端** | ❌ | ❌ | ❌ | ❌ | **✅ iOS/Android App** |
| **目标用户** | 开发者 | 研究人员 | 开发者 | 开发者 | **普通用户** |

---

## 设计理念对比

### OpenDevin: 事件流解耦

```
用户 → Agent → Event Stream → Runtime → 执行
        ↑                      ↓
        └── Observation ←──────┘
```

**核心思想**: Agent 与执行环境解耦，通过 Event Stream 通信

**优势**:
- 支持回放、中断、恢复
- Agent 实现简单（30 行代码）
- 安全隔离（Docker）

### AgentScope: Actor 并行

```
Agent1 (Actor) ─┐
Agent2 (Actor) ─┼─→ Message Queue ─→ Environment
Agent3 (Actor) ─┘
```

**核心思想**: 每个 Agent 是独立 Actor，无锁并行

**优势**:
- 百万级 Agent 可行
- 进程级隔离
- Placeholder 非阻塞

### DeerFlow: Harness + Context Engineering

```
Lead Agent ──┬── Skills（渐进加载）
             ├── Memory（跨会话）
             ├── Sub-Agent Orchestrator（并行派生）
             │     │
             │     ├─→ Sub-Agent-A（上下文隔离）
             │     ├─→ Sub-Agent-B（上下文隔离）
             │     └─→ Sub-Agent-C（上下文隔离）
             │
             └── Context Engineering（压缩总结）
                    ↓
              Docker Sandbox（执行）
```

**核心思想**: 框架 + 基础设施 + 技能 = Harness，上下文隔离 + 压缩 = 长任务支持

**优势**:
- 开箱即用（Harness）
- 小时级任务可行（Context Engineering）
- 多渠道接入（企业友好）
- 长期记忆（个性化）

---

## 关键技术对比

### 并行/隔离机制

| 技术 | OpenDevin | AgentScope |
|------|-----------|------------|
| **机制** | Docker 容器 | Actor 进程 |
| **隔离级别** | 系统级 | 进程级 |
| **开销** | 较高（启动容器） | 较低（进程切换） |
| **适用规模** | ~10 Agent | 百万 Agent |
| **安全性** | ⭐⭐⭐ | ⭐⭐ |

### Agent 协作机制

| 技术 | OpenDevin | AgentScope |
|------|-----------|------------|
| **方式** | DelegateAction | 消息广播 |
| **模式** | 点对点委托 | 广播订阅 |
| **专家分工** | 静态指定 | 动态参与 |
| **环境角色** | 执行沙箱 | 特殊 Agent |

### 效率优化

| 技术 | OpenDevin | AgentScope | LlamaFactory |
|------|-----------|------------|--------------|
| **优化点** | AgentSkills 缓存 | Placeholder 非阻塞 | QLoRA 量化 |
| **效果** | 减少 LLM 调用 | 40秒跑完100万 | 内存降 96% |

---

## 适用场景

| 场景 | 推荐 | 原因 |
|------|------|------|
| **软件工程自动化** | OpenDevin | 代码执行 + 安全沙箱 |
| **社会模拟/游戏** | AgentScope | 百万级并行 + 环境抽象 |
| **LLM 微调** | LlamaFactory | 100+ 模型 + Web UI |
| **深度研究/内容创作** | **DeerFlow** | **技能库 + 长任务支持 + 记忆** |
| **企业部署** | **DeerFlow** | **多渠道接入 + MIT 协议 + Docker 沙箱** |
| **个人生活助手** | **OpenClaw** | **20+ 渠道 + 语音 + 移动端 + 5400+ 技能** |
| **团队协作工具** | **OpenClaw** | **多渠道 + 配对机制 + Canvas** |
| **语音交互场景** | **OpenClaw** | **Voice Wake + Talk Mode** |
| **多 Agent 协作研究** | OpenDevin + AgentScope + DeerFlow | 对比三种架构 |
| **消费级部署** | LlamaFactory + QLoRA | 低内存需求 |
| **需要沙箱安全** | DeerFlow / OpenDevin | Docker 隔离执行 |

---

## 共性设计模式

三篇论文都体现了以下设计原则：

1. **解耦设计**: Agent 逻辑与执行/通信分离
2. **模块化**: 可插拔组件，易于扩展
3. **抽象接口**: 统一的 Agent/Environment 协议
4. **效率优先**: 都有针对效率的核心创新

---

## 相关原子概念

### 执行层架构
- [[Event Stream]]: OpenDevin 核心架构
- [[Actor 模型]]: AgentScope 并行机制
- [[Placeholder]]: AgentScope 非阻塞设计
- [[环境抽象]]: AgentScope 环境设计
- [[DelegateAction]]: OpenDevin 任务委托
- **[[Super Agent Harness]]**: DeerFlow 核心定位
- **[[Skills技能系统]]**: DeerFlow 技能扩展机制
- **[[Context Engineering]]**: DeerFlow 上下文管理
- **[[ClawHub Skills Registry]]**: OpenClaw 5400+ 技能库
- **[[Voice Wake & Talk Mode]]**: OpenClaw 语音交互
- **[[Canvas & A2UI]]**: OpenClaw 可视化工作区

### 效率技术
- [[QLoRA]]: LlamaFactory 效率技术
- [[Model-Sharing RLHF]]: LlamaFactory RLHF 创新

---

## 延伸思考

1. **融合可能性**: 能否将 Event Stream 与 Actor 模型结合？
2. **统一框架**: 是否存在一个能同时支持软件工程 + 社会模拟的架构？
3. **微调 + Agent**: LlamaFactory 微调的模型如何用于 OpenDevin/AgentScope？