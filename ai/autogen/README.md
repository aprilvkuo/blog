# AutoGen 学习笔记

> 适合在 Obsidian 中查看的 AutoGen 学习指南

---

## 📖 使用方法

### 在 Obsidian 中打开

1. 打开 Obsidian
2. 点击 "Open folder as vault"
3. 选择 `autogen-learning` 文件夹

### 学习路径

从 [00-Index](00-Index) 笔记开始，按照以下顺序学习：

1. [ Core 核心概念](01-Core 核心概念/00-Core 核心概念总览)
2. [ 实战示例](04-实战示例/00-实战示例总览)
3. [ AgentChat 高层 API](02-AgentChat 高层 API/00-AgentChat 总览)
4. [ Ext 扩展机制](03-Ext 扩展机制/00-Ext 扩展机制总览)

---

## 📁 目录结构

```
autogen-learning/
├── 00-Index.md                    # 主索引（入口）
├── 01-Core 核心概念/
│   ├── 00-Core 核心概念总览.md
│   ├── 01-Agent 和 Runtime.md
│   ├── 02-消息传递机制.md
│   ├── 03-订阅和主题.md
│   └── 04-路由和匹配.md
├── 02-AgentChat 高层 API/
│   ├── 00-AgentChat 总览.md
│   ├── 01-AssistantAgent.md
│   ├── 02-群聊模式.md
│   └── 03-终止条件.md
├── 03-Ext 扩展机制/
│   ├── 00-Ext 扩展机制总览.md
│   ├── 01-模型客户端.md
│   ├── 02-工具和工作台.md
│   └── 03-MCP 集成.md
├── 04-实战示例/
│   ├── 00-实战示例总览.md
│   ├── 01-HelloAgent.md
│   ├── 02-发布订阅.md
│   ├── 03-消息路由.md
│   ├── 04-多 Agent 协作.md
│   └── code/                       # 可运行的示例代码
│       ├── 01_hello_agent.py
│       ├── 02_pubsub_agent.py
│       ├── 03_routed_agent.py
│       └── 04_multi_agent_collab.py
└── attachments/                    # 附件（图片等）
```

---

## 🏃 运行示例代码

```bash
# 1. 进入 Python 目录
cd /path/to/autogen/python

# 2. 设置环境
uv sync --all-extras
source .venv/bin/activate

# 3. 运行示例
python autogen-learning/04-实战示例/code/01_hello_agent.py
python autogen-learning/04-实战示例/code/02_pubsub_agent.py
python autogen-learning/04-实战示例/code/03_routed_agent.py
python autogen-learning/04-实战示例/code/04_multi_agent_collab.py
```

---

## 📝 学习笔记说明

### Core 核心概念

- **01-Agent 和 Runtime**: 讲解 Agent 的基本结构和 Runtime 的工作原理
- **02-消息传递机制**: 对比 RPC 消息和广播消息的区别
- **03-订阅和主题**: 详解 Topic 和 Subscription 的使用
- **04-路由和匹配**: 演示如何使用条件匹配进行消息路由

### AgentChat 高层 API

- **01-AssistantAgent**: 学习最常用的助手 Agent
- **02-群聊模式**: 理解 RoundRobin、Selector、Swarm 三种协作模式
- **03-终止条件**: 学习如何控制 Agent 执行流程

### Ext 扩展机制

- **01-模型客户端**: 了解支持的各種模型客户端
- **02-工具和工作台**: 学习如何添加工具
- **03-MCP 集成**: 理解 MCP 协议和集成方式

### 实战示例

每个实战示例都包含：
- 完整的代码实现
- 关键概念解析
- 运行方法
- 预期输出
- 练习建议

---

## 💡 学习建议

### 第一天：基础入门（2-3 小时）
1. 阅读 [01-Core 核心概念/00-Core 核心概念总览](01-Core 核心概念/00-Core 核心概念总览)
2. 运行 [04-实战示例/01-HelloAgent](04-实战示例/01-HelloAgent) 代码
3. 理解 Agent、Runtime、Message 的关系

### 第二天：深入理解（3-4 小时）
1. 学习 [01-Core 核心概念/02-消息传递机制](01-Core 核心概念/02-消息传递机制) 和 [01-Core 核心概念/03-订阅和主题](01-Core 核心概念/03-订阅和主题)
2. 运行 [04-实战示例/02-发布订阅](04-实战示例/02-发布订阅) 代码
3. 理解 RPC vs 广播的区别

### 第三天：实战应用（3-4 小时）
1. 学习 [02-AgentChat 高层 API/00-AgentChat 总览](02-AgentChat 高层 API/00-AgentChat 总览)
2. 运行 [04-实战示例/04-多 Agent 协作](04-实战示例/04-多 Agent 协作) 代码
3. 尝试修改代码实现自己的逻辑

---

## 🔗 相关资源

- [官方文档](https://microsoft.github.io/autogen/dev/)
- [GitHub 仓库](https://github.com/microsoft/autogen)
- [Discord 社区](https://aka.ms/autogen-discord)

---

## 📌 版本信息

- AutoGen 版本：0.7.5
- Python 版本：3.10+
- 笔记创建日期：2026-03-14
