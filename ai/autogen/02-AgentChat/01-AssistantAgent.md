# AssistantAgent

> 通用助手 Agent，支持工具调用和多轮对话

---

## 📖 概述

`AssistantAgent` 是 AgentChat 中最常用的 Agent，能够：

- 进行多轮对话
- 调用工具（Function Calling）
- 使用 MCP 服务器
- 支持流式响应

---

## 1. 基本用法

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 创建模型客户端
model_client = OpenAIChatCompletionClient(model="gpt-4.1")

# 创建助手 Agent
agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    system_message="你是一个有用的助手",
)

# 运行
result = await agent.run(task="说你好")
print(result.messages[-1].content)
```

---

## 2. 关键参数

```python
AssistantAgent(
    name: str,                    # Agent 名称
    model_client: ChatCompletionClient,  # 模型客户端
    tools: List[Tool],           # 工具列表（可选）
    workbench: Workbench,        # 工作台（可选，如 MCP）
    handoffs: List[Handoff],     # 交接配置（可选）
    model_context: ChatCompletionContext,  # 上下文管理（可选）
    system_message: str,         # 系统消息
    model_client_stream: bool,   # 是否启用流式
    reflect_on_tool_use: bool,   # 工具使用后是否反思
    max_tool_iterations: int,    # 最大工具迭代次数
)
```

---

## 3. 工具调用

### 定义工具

```python
from autogen_core.tools import FunctionTool

def add(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b

tool = FunctionTool(add)
```

### 使用工具

```python
agent = AssistantAgent(
    name="math_assistant",
    model_client=model_client,
    tools=[tool],
    max_tool_iterations=5,  # 最多 5 次工具调用
)

result = await agent.run(task="计算 123 + 456")
```

---

## 4. 流式模式

```python
agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    model_client_stream=True,  # 启用流式
)

# 流式运行
async for message in agent.run_stream(task="写一首诗"):
    print(message)
```

---

## 5. 工具使用行为

### reflect_on_tool_use

- `False` (默认): 工具调用结果直接返回
- `True`: 工具调用后再次推理，生成自然语言响应

```python
# 不反思（返回工具结果）
agent = AssistantAgent(
    ...,
    reflect_on_tool_use=False,
    tool_call_summary_format="工具执行结果：{result}"
)

# 反思（生成自然语言响应）
agent = AssistantAgent(
    ...,
    reflect_on_tool_use=True
)
```

---

## 6. Handoff（交接）

将对话移交给其他 Agent。

```python
from autogen_agentchat.base import Handoff

# 定义 handoff
handoff = Handoff(target="expert_agent", name="转交专家")

agent = AssistantAgent(
    name="general_assistant",
    model_client=model_client,
    handoffs=[handoff]
)
```

---

## 7. 模型上下文管理

限制上下文大小：

```python
from autogen_core.model_context import BufferedChatCompletionContext

agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    model_context=BufferedChatCompletionContext(buffer_size=5)  # 只保留 5 条消息
)
```

---

## 8. 完整示例

### 带工具的助手

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city} 的天气：晴朗，25°C"

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4.1")

    agent = AssistantAgent(
        name="weather_assistant",
        model_client=model_client,
        tools=[FunctionTool(get_weather)],
        reflect_on_tool_use=True,
    )

    await Console(agent.run_stream(task="北京天气怎么样？"))

asyncio.run(main())
```

---

## 9. 状态管理

```python
# 保存状态
state = await agent.save_state()

# 加载状态
await agent.load_state(state)
```

---

## 📝 练习

1. 创建一个带计算器工具的 Agent
2. 创建一个使用天气查询工具的 Agent
3. 尝试流式模式

---

## 🔗 相关链接

- [00-AgentChat 总览](00-AgentChat 总览)
- [../03-Ext 扩展机制/02-工具和工作台](../03-Ext 扩展机制/02-工具和工作台)
- [../04-实战示例/01-HelloAgent](../04-实战示例/01-HelloAgent)
