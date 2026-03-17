# Ext 扩展机制总览

> 集成第三方模型、工具和服务

---

## 📖 概述

`autogen-ext` 提供了丰富的扩展，包括：

- 模型客户端（Model Clients）
- 工具（Tools）
- 代码执行器（Code Executors）
- MCP 集成
- 记忆系统（Memory）

---

## 1. 模型客户端

### OpenAI

```python
from autogen_ext.models.openai import OpenAIChatCompletionClient

client = OpenAIChatCompletionClient(
    model="gpt-4.1",
    api_key="sk-..."
)
```

### Azure OpenAI

```python
from autogen_ext.models.azure import AzureOpenAIChatCompletionClient

client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-4",
    azure_endpoint="https://...",
    api_version="2024-01-01"
)
```

### Ollama

```python
from autogen_ext.models.ollama import OllamaChatCompletionClient

client = OllamaChatCompletionClient(
    model="llama3.1",
    base_url="http://localhost:11434"
)
```

### Anthropic

```python
from autogen_ext.models.anthropic import AnthropicChatCompletionClient

client = AnthropicChatCompletionClient(
    model="claude-sonnet-4-20250514",
    api_key="..."
)
```

---

## 2. 工具 (Tools)

### FunctionTool

```python
from autogen_core.tools import FunctionTool

def add(a: int, b: int) -> int:
    """计算两数之和"""
    return a + b

tool = FunctionTool(add)
```

### MCP 工具

```python
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams

server_params = StdioServerParams(
    command="npx",
    args=["@playwright/mcp@latest"]
)

async with McpWorkbench(server_params) as workbench:
    tools = await workbench.list_tools()
```

### LangChain 工具

```python
from autogen_ext.tools.langchain import LangChainAdapter
from langchain_community.tools import DuckDuckGoSearchRun

tool = LangChainAdapter(DuckDuckGoSearchRun())
```

---

## 3. 代码执行器

### Docker 执行器

```python
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

executor = DockerCommandLineCodeExecutor(
    work_dir="coding",
    container_name="autogen-code-exec"
)
```

### Jupyter 执行器

```python
from autogen_ext.code_executors.jupyter import JupyterCodeExecutor

executor = JupyterCodeExecutor()
```

### Azure 执行器

```python
from autogen_ext.code_executors.azure import AzureContainerCodeExecutor

executor = AzureContainerCodeExecutor(
    pool_management_endpoint="...",
    credential=credential
)
```

---

## 4. 记忆系统

### ChromaDB 记忆

```python
from autogen_ext.memory.chromadb import ChromaDBMemory

memory = ChromaDBMemory(
    collection_name="my_memory"
)
```

### Redis 记忆

```python
from autogen_ext.memory.redis import RedisMemory

memory = RedisMemory(
    redis_url="redis://localhost:6379"
)
```

---

## 5. 缓存

### DiskCache

```python
from autogen_ext.cache_store.diskcache import DiskCacheStore

cache = DiskCacheStore(cache_dir="./cache")
```

### Redis 缓存

```python
from autogen_ext.cache_store.redis import RedisStore

cache = RedisStore(redis_url="redis://localhost:6379")
```

---

## 6. 安装

### 完整安装

```bash
pip install "autogen-ext[all]"
```

### 按需安装

```bash
# OpenAI
pip install "autogen-ext[openai]"

# MCP
pip install "autogen-ext[mcp]"

# 代码执行
pip install "autogen-ext[docker]"

# 记忆
pip install "autogen-ext[chromadb]"
```

---

## 7. 创建自定义扩展

### 自定义模型客户端

```python
from autogen_core.models import ChatCompletionClient, CreateResult

class MyModelClient(ChatCompletionClient):
    async def create(self, messages, tools=None, **kwargs) -> CreateResult:
        # 实现创建逻辑
        return result
```

### 自定义工具

```python
from autogen_core.tools import BaseTool

class MyTool(BaseTool[InputModel, OutputModel]):
    def __init__(self):
        super().__init__(
            InputModel,
            OutputModel,
            name="my_tool",
            description="我的工具"
        )

    async def run(self, args: InputModel, cancellation_token) -> OutputModel:
        # 实现工具逻辑
        return result
```

---

## 🔗 相关链接

- [01-模型客户端](01-模型客户端.md) - 深入了解模型客户端
- [02-工具和工作台](02-工具和工作台.md) - 学习工具系统
- [03-MCP 集成](03-MCP 集成.md) - MCP 协议详解
