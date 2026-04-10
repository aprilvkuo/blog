---
title: 最小 Agent 实现
created: 2026-03-28
tags:
  - agent
  - note
  - implementation
status: in-progress
---

# 最小 Agent 实现

> 目标：不依赖框架，用 100 行代码实现 Agent 核心，理解本质

---

## 核心认知

Agent = LLM + Tool Call Loop

```
┌─────────────────────────────────────────┐
│                  Agent                   │
│  ┌─────────┐    ┌─────────┐    ┌──────┐│
│  │   LLM   │ ←→ │  Tools  │ ←→ │ Loop ││
│  └─────────┘    └─────────┘    └──────┘│
└─────────────────────────────────────────┘
```

**本质**：
1. LLM 决定调用什么工具
2. 执行工具调用
3. 将结果反馈给 LLM
4. 循环直到任务完成

---

## 实现步骤

### Step 1: 最小 Agent（~50 行）

**目标**：实现核心循环

```python
# TODO: 实现
class Agent(object):
	def __init__(self, model, tools=[]):
		self.llm = model
		self.tools = tools
		self.history = []


	def forward(self, query):
		self.history += query
		resp = self.llm.call(history)
		self.history += resp
		for calling_tool in resp:
			self.history += do(calling_tool,  self.tools)
		for task in resp:
			self.forward(task)
		return history[-1]



```

**关键点**：
- [ ] OpenAI API 调用
- [ ] Tool Definition 结构
- [ ] Tool Call 解析
- [ ] 循环终止条件

**问题分析**（上述代码的 Bug）：

| 问题 | 错误代码 | 正确做法 |
|------|----------|----------|
| 变量引用 | `history` 未定义 | `self.history` |
| 消息格式 | `+= query` | `append({"role": ...})` |
| Tool 解析 | `for x in resp` | `message.tool_calls` |
| 循环逻辑 | 两个循环冲突 | 单循环 + 条件分支 |
| 终止条件 | 无 | 检查 `tool_calls` 是否为空 |
| 递归 | 不必要的递归 | 用 while 循环 |
| 默认参数 | `tools=[]` | `tools=None` → `self.tools = tools or []` |

---

### 伪代码（核心逻辑）

```
function run_agent(user_input):
    history = [user_input]

    loop:
        response = LLM.call(history, tools)

        if response.has_tool_calls:
            history.append(response)

            for each tool_call in response.tool_calls:
                result = execute_tool(tool_call)
                history.append(tool_result)

            continue loop

        else:
            return response.content
```

**核心要点**：
1. `history` 管理消息历史
2. `LLM.call` 可能返回工具调用或最终答案
3. `has_tool_calls` 是终止条件判断
4. 工具执行结果反馈给 LLM，继续循环

---

### 正确实现

```python
import json
from openai import OpenAI

class Agent:
    """最小 Agent 实现 - 正确版本"""

    def __init__(self, model="gpt-4o-mini", tools=None):
        self.client = OpenAI()
        self.model = model
        self.tools = tools or []
        self.tool_functions = {}  # 工具名 → 函数的映射
        self.history = []  # 消息历史

    def register_tool(self, name: str, function: callable, description: str, parameters: dict):
        """注册工具"""
        # 工具定义（给 LLM 看的）
        self.tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })
        # 工具实现（实际执行的）
        self.tool_functions[name] = function

    def run(self, user_input: str) -> str:
        """核心循环"""
        # 1. 添加用户消息
        self.history.append({"role": "user", "content": user_input})

        # 2. 循环直到终止
        while True:
            # 调用 LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=self.tools if self.tools else None,
                tool_choice="auto"
            )
            message = response.choices[0].message

            # 3. 判断是否需要调用工具
            if message.tool_calls:
                # 添加 LLM 的消息到历史
                self.history.append(message)

                # 执行所有工具调用
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    # 执行工具
                    result = self.tool_functions[func_name](**func_args)

                    # 将结果反馈给 LLM
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

            else:
                # 无工具调用 → 返回最终答案
                self.history.append(message)
                return message.content


# 使用示例
if __name__ == "__main__":
    agent = Agent()

    # 注册天气工具
    agent.register_tool(
        name="get_weather",
        function=lambda city: f"{city} 今天晴天，25°C",
        description="获取城市天气",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"}
            },
            "required": ["city"]
        }
    )

    # 运行
    result = agent.run("北京今天天气怎么样？")
    print(result)
```

---

### Step 2: 添加 Memory（~30 行）

**目标**：实现简单的对话记忆

#### 初版实现（有 Bug）

```python
# TODO: 实现

import json
from openai import OpenAI


class Rag:
	def __init__(self, docs, embding_model):
		self.database = viking.build(embding_model, docs)

	def search(self, query, threshold=0.5, num=10):
		return self.database.search(query, threshold, num)


class Agent:
    """最小 Agent 实现 - 正确版本"""

    def __init__(self, model="gpt-4o-mini", tools=None, docs=None, embding_model=None):
        self.client = OpenAI()
        self.model = model
        self.tools = tools or []
        self.tool_functions = {}  # 工具名 → 函数的映射
        self.history = []  # 消息历史
        self.max_history_len = 50
        self.rag = Rag(docs, embding_model)

    def register_tool(self, name: str, function: callable, description: str, parameters: dict):
        """注册工具"""
        # 工具定义（给 LLM 看的）
        self.tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })
        # 工具实现（实际执行的）
        self.tool_functions[name] = function

    def run(self, user_input: str) -> str:
        """核心循环"""
        # 1. 添加用户消息
        self.history.append({"role": "user", "content": user_input})

        # 2. 循环直到终止
        while True:
            # 调用 LLM
            if self.history > self.max_history_len:
	           self.history = self.history[:50]
	        recall_docs = self.rag(history[-1]
	        if len(recall_docs) > 0:
		        self.history["content"] = self.history["content"] + "\n".join(recall_docs)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=self.tools if self.tools else None,
                tool_choice="auto"
            )
            message = response.choices[0].message

            # 3. 判断是否需要调用工具
            if message.tool_calls:
                # 添加 LLM 的消息到历史
                self.history.append(message)

                # 执行所有工具调用
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    # 执行工具
                    result = self.tool_functions[func_name](**func_args)

                    # 将结果反馈给 LLM
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

            else:
                # 无工具调用 → 返回最终答案
                self.history.append(message)
                self.history = self.history[:50]
                return message.content


# 使用示例
if __name__ == "__main__":
    agent = Agent()

    # 注册天气工具
    agent.register_tool(
        name="get_weather",
        function=lambda city: f"{city} 今天晴天，25°C",
        description="获取城市天气",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"}
            },
            "required": ["city"]
        }
    )

    # 运行
    result = agent.run("北京今天天气怎么样？")
    print(result)
```

**问题分析**（上述代码的 Bug）：

| 问题 | 错误代码 | 正确做法 |
|------|----------|----------|
| 未定义库 | `viking.build(...)` | 使用真实向量库如 chromadb/faiss |
| 类型比较 | `self.history > 50` | `len(self.history) > self.max_history_len` |
| 方法调用 | `self.rag(history[-1]` | `self.rag.search(self.history[-1]["content"])` |
| 缺括号 | `self.rag(...` | 缺少右括号 |
| 列表索引 | `self.history["content"]` | `self.history[-1]["content"]` |
| 消息类型 | 直接修改最后一条 | 应区分 user/assistant/tool 消息 |
| None 处理 | `Rag(docs, embding_model)` | 检查参数是否为 None |
| 检索时机 | 每次循环都检索 | **只在用户输入时检索一次** |
| 缩进混乱 | 混用 tab/space | 统一缩进 |

---

#### 正确实现（Memory 版本）

```python
import json
from openai import OpenAI


class RAG:
    """简单的向量检索"""

    def __init__(self, docs=None):
        if docs is None:
            self.enabled = False
            return

        self.enabled = True
        self.docs = docs
        # TODO: 实际应该用 chromadb/faiss 建立向量索引
        # 示例：
        # import chromadb
        # client = chromadb.Client()
        # self.collection = client.create_collection("docs")
        # self.collection.add(documents=docs, ids=[str(i) for i in range(len(docs))])

    def search(self, query: str, top_k: int = 3) -> list:
        """检索相关文档"""
        if not self.enabled:
            return []

        # TODO: 实际向量检索
        # results = self.collection.query(query_texts=[query], n_results=top_k)
        # return results["documents"][0]

        return []  # 返回相关文档列表


class AgentWithMemory:
    """带 Memory 的 Agent - 正确版本"""

    def __init__(self, model="gpt-4o-mini", tools=None, docs=None):
        self.client = OpenAI()
        self.model = model
        self.tools = tools or []
        self.tool_functions = {}
        self.history = []
        self.max_history_len = 20  # 保留最近 20 条
        self.rag = RAG(docs)

    def register_tool(self, name: str, function: callable, description: str, parameters: dict):
        """注册工具"""
        self.tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })
        self.tool_functions[name] = function

    def _truncate_history(self):
        """截断历史，保留最近对话"""
        if len(self.history) > self.max_history_len:
            # 保留最近的对话
            self.history = self.history[-self.max_history_len:]

    def _inject_context(self, query: str) -> str:
        """RAG 检索并注入上下文（只在用户输入时做一次）"""
        docs = self.rag.search(query)
        if docs:
            return query + "\n\n相关文档：\n" + "\n".join(docs)
        return query

    def run(self, user_input: str) -> str:
        """核心循环"""

        # 1. RAG 增强（只在输入时检索一次）
        enhanced_input = self._inject_context(user_input)
        self.history.append({"role": "user", "content": enhanced_input})

        # 2. 截断历史
        self._truncate_history()

        # 3. 循环执行
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=self.tools if self.tools else None,
                tool_choice="auto"
            )
            message = response.choices[0].message

            if message.tool_calls:
                # 添加 LLM 消息
                self.history.append(message)

                # 执行工具调用
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    # 执行工具
                    if func_name in self.tool_functions:
                        result = self.tool_functions[func_name](**func_args)
                    else:
                        result = f"Error: Tool '{func_name}' not found"

                    # 反馈结果
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

                # 工具调用后也截断
                self._truncate_history()

            else:
                # 返回最终答案
                self.history.append(message)
                return message.content


# 使用示例
if __name__ == "__main__":
    # 带文档的 Agent
    docs = ["北京今天晴天，温度 25°C", "上海今天多云，温度 22°C"]
    agent = AgentWithMemory(docs=docs)

    # 注册天气工具
    agent.register_tool(
        name="get_weather",
        function=lambda city: f"{city} 今天晴天，25°C",
        description="获取城市天气",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"}
            },
            "required": ["city"]
        }
    )

    # 运行（RAG 会检索相关文档注入）
    result = agent.run("北京今天天气怎么样？")
    print(result)
```

**关键点**：
- [x] 消息历史管理（`_truncate_history`）
- [x] 上下文窗口限制（`max_history_len`）
- [x] RAG 检索时机正确（**只在用户输入时**）
- [x] 向量检索抽象清晰（`RAG` 类）

**核心认知**：

| 记忆类型 | 存储方式 | 检索时机 |
|----------|----------|----------|
| 短期记忆 | history list | 每次调用 LLM |
| 长期记忆 | 向量数据库 | **用户输入时** |
| 工作记忆 | 当前对话上下文 | 自动（在 history 中） |

---

### Step 3: Multi-Agent 路由（~20 行）

**目标**：多个 Agent 之间的协作

#### 初版实现（思路）

```python
# TODO: 实现

query

def read_agent_md(filename):
	return open(filename).read()
main_agent = agent(read_agent_md("main_agent.md"))
sub_agents = [agent(read_agent_md(f"sub_agent_{%d}.md")) for i in range(10)]

main_agent.run(query)
```

**问题分析**：

| 问题 | 你的代码 | 缺失 |
|------|----------|------|
| 变量未定义 | `query` | 应该是参数 |
| 函数未定义 | `agent()` | 需要实现 |
| 无路由逻辑 | `main_agent.run(query)` | 主 agent 如何分配任务？ |
| 无消息传递 | 没有 | 子 agent 结果如何返回？ |
| 无终止条件 | 没有 | 什么时候结束协作？ |
| 格式字符串 | `f"sub_agent_{%d}.md"` | 应该是 `f"sub_agent_{i}.md"` |

---

#### 正确实现（Multi-Agent 版本）

```python
import json
from openai import OpenAI
from typing import Dict, List, Callable


class Agent:
    """单个 Agent"""

    def __init__(self, name: str, system_prompt: str, model: str = "gpt-4o-mini"):
        self.name = name
        self.client = OpenAI()
        self.model = model
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": system_prompt}]

    def run(self, user_input: str) -> str:
        """执行任务"""
        self.history.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history
        )

        message = response.choices[0].message
        self.history.append(message)
        return message.content


class MultiAgentRouter:
    """Multi-Agent 路由器 - Supervisor 模式"""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.workers: Dict[str, Agent] = {}

    def register_worker(self, name: str, agent: Agent):
        """注册 Worker Agent"""
        self.workers[name] = agent

    def _route(self, query: str) -> str:
        """路由决策：决定由哪个 Worker 处理"""
        worker_names = list(self.workers.keys())

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"""你是一个路由器。根据用户问题，选择最合适的 Agent 处理。
可用的 Agent：{worker_names}
只返回 Agent 名称，不要其他内容。"""
                },
                {"role": "user", "content": query}
            ]
        )

        return response.choices[0].message.content.strip()

    def run(self, query: str, max_handoffs: int = 5) -> str:
        """
        执行 Multi-Agent 协作

        流程：
        1. 路由器决定由哪个 Worker 处理
        2. Worker 执行任务
        3. 返回结果（或继续路由）
        """
        handoffs = 0
        current_query = query
        results = []

        while handoffs < max_handoffs:
            # 1. 路由决策
            worker_name = self._route(current_query)

            # 检查 Worker 是否存在
            if worker_name not in self.workers:
                return f"Error: Unknown agent '{worker_name}'"

            # 2. Worker 执行
            worker = self.workers[worker_name]
            result = worker.run(current_query)
            results.append(f"[{worker_name}]: {result}")

            # 3. 判断是否需要继续（简化：只路由一次）
            # 实际应用可以让 Supervisor 决定是否继续
            break

        return "\n\n".join(results)


# 使用示例
if __name__ == "__main__":
    # 创建路由器
    router = MultiAgentRouter()

    # 注册 Worker Agents
    router.register_worker(
        "code_agent",
        Agent(
            name="code_agent",
            system_prompt="你是一个代码专家，帮助用户解决编程问题。"
        )
    )

    router.register_worker(
        "weather_agent",
        Agent(
            name="weather_agent",
            system_prompt="你是一个天气助手，帮助用户查询天气信息。"
        )
    )

    router.register_worker(
        "search_agent",
        Agent(
            name="search_agent",
            system_prompt="你是一个搜索助手，帮助用户查找信息。"
        )
    )

    # 运行
    result = router.run("北京今天天气怎么样？")
    print(result)
    # 输出: [weather_agent]: 北京今天晴天...
```

**关键点**：
- [x] Agent 路由逻辑（`_route` 方法）
- [x] Agent 间消息传递（`results` 收集）
- [x] 协作终止条件（`max_handoffs`）
- [x] Worker 注册机制

**核心认知**：

| 模式 | 适用场景 | 实现方式 |
|------|----------|----------|
| **Supervisor** | 需要协调多个专家 | 主 Agent 分配任务 |
| **Handoff** | 任务需要在 Agent 间传递 | Agent 互相调用 |
| **Group Chat** | 需要自由讨论 | 所有 Agent 共享消息 |

**终止保障**：
- `max_handoffs` 防止无限路由
- 每次 handoff 记录结果
- Supervisor 可以决定是否继续

---

## 完整实现

```python
# 最终代码放在这里
```

---

## 测试用例

### 基础测试

```python
# 测试简单问答
# 测试工具调用
# 测试多轮对话
```

### 边界测试

```python
# 测试上下文溢出
# 测试工具调用失败
# 测试循环终止
```

---

## 关键学习

### 框架做了什么

| 框架提供的     | 我们手动实现的          |
| --------- | ---------------- |
| Tool 定义封装 | 手写 JSON Schema   |
| 消息历史管理    | 手写 messages list |
| 循环控制      | 手写 while loop    |
| 错误处理      | 手写 try-catch     |
| 可观测性      | 自己加 logging      |

### 框架没做什么

- **Planning 能力** - 由模型决定，框架只是封装
- **工具执行** - 框架调用你提供的函数
- **终止判断** - 框架有默认策略，但你可以自定义

---

### JSON Schema 深入理解

#### 什么是 JSON Schema？

JSON Schema 是描述 JSON 数据结构的标准格式。在 Agent 中，它定义工具参数结构，告诉 LLM 需要什么参数、参数类型是什么。

#### 结构示例

```python
{
    "type": "object",           # 参数整体是个对象
    "properties": {             # 对象有哪些属性
        "city": {
            "type": "string",   # 属性类型
            "description": "城市名"  # 帮助 LLM 理解
        },
        "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]  # 枚举限制
        }
    },
    "required": ["city"]        # 必填字段
}
```

#### LLM 如何使用

```
用户："北京今天天气怎么样？"

LLM 看到工具定义：
├── name: get_weather
├── parameters.city: string, required
└── parameters.unit: string, optional, enum

LLM 生成调用：
{"name": "get_weather", "arguments": {"city": "北京"}}

Agent 解析并执行：
get_weather(city="北京")
```

#### 常见参数类型

| 类型 | JSON Schema | 示例值 |
|------|-------------|--------|
| 字符串 | `"type": "string"` | `"北京"` |
| 数字 | `"type": "number"` | `25` |
| 布尔 | `"type": "boolean"` | `true` |
| 数组 | `"type": "array"` | `["北京", "上海"]` |
| 枚举 | `"enum": ["a", "b"]` | 只能是 "a" 或 "b" |

---

### tools 参数 vs Function Calling

#### 概念关系

| 术语 | 层面 | 含义 |
|------|------|------|
| **Function Calling** | 概念/能力 | LLM 能够"识别并调用函数"的能力 |
| **tools 参数** | API 实现 | OpenAI API 中传递工具定义的字段名 |

```
Function Calling（能力）
    │
    ├── OpenAI 的实现：tools 参数
    ├── Anthropic 的实现：tools 参数
    ├── Google Gemini：function_declarations 参数
    └── 纯 Prompt 实现：写在 system prompt 里
```

#### 历史演变

```python
# 2023 年初：functions 参数（已废弃）
response = client.chat.completions.create(
    functions=[{...}]  # 旧参数名
)

# 2023 年末：tools 参数（当前标准）
response = client.chat.completions.create(
    tools=[{
        "type": "function",  # 指明是函数类型
        "function": {...}
    }]
)
```

---

### tools 的底层实现原理

#### 三层架构

```
┌─────────────────────────────────────┐
│ 1. API 层（你看到的）                   │
│    tools 参数 → 结构化输入             │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 2. 内部转换层（OpenAI 黑盒）            │
│    tools → 注入系统 Prompt             │
│    格式化工具描述                       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ 3. 模型层（实际处理）                   │
│    看到 Prompt → 推理                  │
│    输出 tool_calls 或文本              │
└─────────────────────────────────────┘
```

#### OpenAI 内部处理（推测）

```
你的请求
├── messages: [{"role": "user", "content": "北京天气"}]
├── tools: [{JSON Schema}]
│
↓ OpenAI 内部转换
│
实际发给模型的 Prompt
┌─────────────────────────────────────
│ # Tools
│
│ You have access to the following tools:
│
│ ## get_weather
│ Description: 获取城市天气
│ Parameters:
│   - city (string, required): 城市名
│
│ Output format:
│ {"name": "get_weather", "arguments": {"city": "北京"}}
└─────────────────────────────────────
```

**关键**：tools 最终是 Prompt，但由 API 内部转换，格式保密。

#### 为什么用 tools 参数而不是自己写 Prompt？

| 对比 | tools API 参数 | 自己写 Prompt |
|------|---------------|---------------|
| 格式 | OpenAI 内部标准化 | 你自己定义 |
| 稳定性 | ✅ 保证格式稳定 | ❌ 可能变化 |
| 微调 | ✅ 模型专门优化 | ❌ 模型未优化 |
| 解析 | ✅ API 返回结构化对象 | ❌ 需手动解析文本 |
| 可靠性 | ✅ 高 | ❌ 低 |

#### 模型层面的微调

OpenAI 对模型做了专门的 Function Calling 微调：

```
微调数据：
Input: 用户问题 + 工具定义
Output: 结构化的 tool_call（不是自由文本）

训练目标：
1. 识别何时需要调用工具
2. 生成正确格式的 JSON
3. 不是随意输出文本，而是精确的 tool_calls
```

#### 不同模型的 tools 支持

| 模型 | tools 支持 | 效果 |
|------|-----------|------|
| gpt-4o | ✅ 完整支持 | 高可靠 |
| gpt-4o-mini | ✅ 支持 | 较可靠 |
| o1（推理模型） | ❌ 不支持 | 只能 Prompt 实现 |
| 开源 Llama | ⚠️ 部分 | 需要 Prompt 实现 |

**o1 不支持 tools**：推理模型的训练目标不同，没有 Function Calling 微调。

---

### 核心结论

| 问题 | 答案 |
|------|------|
| tools 是 Function Calling 吗？ | tools 是 OpenAI 对 Function Calling 的 API 实现 |
| JSON Schema 在 Prompt 哪里？ | 不在 messages 里，通过 tools API 参数传递 |
| tools 最终是 Prompt 吗？ | 是的，但由 API 内部转换，格式保密 |
| 为什么用 tools 参数？ | 标准化协议 + 专门微调 = 高可靠 Function Calling |

**一句话**：
> tools 参数是 OpenAI 把"Prompt + 微调"打包成的 API，让你不用关心内部实现，直接获得可靠的 Function Calling。

---

## 面试问题

### Q: 你能不依赖框架从头实现一个 Agent 吗？

**回答要点**：
1. Agent 本质是 LLM + Tool Call Loop
2. 核心是消息管理和工具调用解析
3. 框架只是封装了这些逻辑，提供更好的工程实践

### Q: 框架的价值是什么？

**回答要点**：
1. 工程化：错误处理、持久化、可观测性
2. 抽象：隐藏复杂性，提供简洁 API
3. 生态：工具库、集成、社区

### Q: 什么时候不用框架？

**回答要点**：
1. 简单场景：直接 API 调用更清晰
2. 特殊需求：框架抽象不匹配
3. 学习目的：理解本质

### Q: tools 和 Function Calling 的区别？

**回答要点**：
1. Function Calling 是 LLM 的能力——识别并调用函数
2. tools 是 OpenAI API 暴露这个能力的参数名
3. 不同平台实现方式不同（Anthropic 也叫 tools，Gemini 叫 function_declarations）

### Q: JSON Schema 在 Prompt 里是如何工作的？

**回答要点**：
1. JSON Schema 通过 tools 参数传递，不是放在 messages 里
2. OpenAI 内部将其转换为系统 Prompt（你看不到这个过程）
3. LLM 经过专门微调，能够理解并生成正确格式的 tool_call

### Q: 为什么用 tools 参数而不是自己写 Prompt？

**回答要点**：
1. 模型专门微调过 Function Calling 能力
2. API 返回结构化的 tool_calls 对象，易于解析
3. 格式稳定，不会因为 Prompt 写法不同而变化

---

## 相关笔记

- [[../insights/三大框架对比]]
- [[../insights/框架设计模式]]
- [[../insights/框架边界认知]]