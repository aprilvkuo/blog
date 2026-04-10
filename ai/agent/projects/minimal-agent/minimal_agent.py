"""
Minimal Agent Implementation
目标：不依赖框架，用 ~100 行代码实现 Agent 核心

Agent = LLM + Tool Call Loop
"""

import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================
# Step 1: Tool Definition
# ============================================================

# 工具定义（Function Calling 格式）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    # TODO: 添加更多工具
]

# 工具实现（实际执行的函数）
def get_weather(city: str) -> str:
    """模拟天气查询"""
    # TODO: 实现真实逻辑
    return f"{city} 今天晴，温度 25°C"

# 工具映射表
tool_functions = {
    "get_weather": get_weather,
}


# ============================================================
# Step 2: Core Agent Loop
# ============================================================

def run_agent(user_input: str, model: str = "gpt-4o-mini") -> str:
    """
    最小 Agent 实现

    核心循环：
    1. LLM 决定是否调用工具
    2. 如果调用工具，执行并反馈结果
    3. 重复直到 LLM 返回最终答案
    """

    # 消息历史
    messages = [{"role": "user", "content": user_input}]

    # 循环执行
    while True:
        # 1. 调用 LLM
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # 让 LLM 自己决定
        )

        message = response.choices[0].message

        # 2. 检查是否需要调用工具
        if message.tool_calls:
            # 将 LLM 的消息加入历史
            messages.append(message)

            # 3. 执行所有工具调用
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments

                # TODO: 解析 arguments（JSON）
                # TODO: 调用对应函数
                # TODO: 将结果加入消息历史

                print(f"[Tool Call] {function_name}({function_args})")

                # 执行工具
                import json
                args = json.loads(function_args)
                result = tool_functions[function_name](**args)

                # 将结果反馈给 LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                print(f"[Tool Result] {result}")

        else:
            # LLM 返回最终答案，退出循环
            return message.content


# ============================================================
# Step 3: 添加 Memory（可选）
# ============================================================

class AgentWithMemory:
    """
    带 Memory 的 Agent

    Memory 类型：
    - 短期记忆：对话历史（messages）
    - 长期记忆：向量检索（TODO）
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.messages = []  # 短期记忆

    def chat(self, user_input: str) -> str:
        """多轮对话"""
        self.messages.append({"role": "user", "content": user_input})

        # TODO: 实现核心循环（同上）
        # TODO: 处理上下文溢出（截断或摘要）

        pass

    def add_long_term_memory(self, content: str):
        """添加长期记忆（向量存储）"""
        # TODO: 实现向量检索
        pass


# ============================================================
# Step 4: Multi-Agent（可选）
# ============================================================

def route_agent(user_input: str) -> str:
    """
    Multi-Agent 路由

    根据任务类型选择不同的 Agent：
    - 天气 Agent：处理天气查询
    - 代码 Agent：处理代码问题
    - 通用 Agent：其他任务
    """

    # TODO: 实现 Agent 路由逻辑
    # 1. 分析用户输入
    # 2. 选择合适的 Agent
    # 3. 执行并返回结果

    pass


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    # 基础测试
    print("=== Test 1: Basic Agent ===")
    result = run_agent("北京今天天气怎么样？")
    print(f"Result: {result}")

    # TODO: 更多测试
    # - 多轮对话
    # - 多工具调用
    # - 边界情况