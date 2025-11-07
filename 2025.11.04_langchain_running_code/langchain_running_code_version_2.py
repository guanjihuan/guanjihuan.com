"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/47925
"""

import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.globals import set_debug

# 开启调试日志输出
set_debug(True)
dotenv.load_dotenv()

# -----------------------
# 定义工具
# -----------------------
@tool
def execute_python(code: str) -> str:
    """执行 Python 代码并返回输出"""
    import sys, io
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        exec(code, {})
    except Exception as e:
        return f"Error: {e}"
    finally:
        sys.stdout = old_stdout
    return mystdout.getvalue().strip()

tools = [execute_python]

# -----------------------
# 创建 LLM
# -----------------------
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    model="qwen-plus",
    temperature=0,
)

# -----------------------
# 创建 Agent
# -----------------------
agent = create_agent(llm, tools)

# -----------------------
# 系统消息，模拟 ReAct 风格
# -----------------------
system_message = """
你是一个严谨的 Python 编程助手，必须通过工具执行代码来验证逻辑。
每次只能执行一个 Action，所有 Python 代码必须通过工具执行，不得假设输出结果。
Action Input 必须是纯 Python 代码，不要包含 Markdown 代码块符号。
如果测试失败（如 assert 报错），请根据错误信息修正代码并重新测试。
输出必须严格遵循以下格式：
Thought: <你的思考>
Action: <工具名称>
Action Input: <纯 Python 代码>
Observation: <工具返回结果>
Final Answer: <最终答案>
"""

# -----------------------
# 用户问题：编写 Fibonacci 函数
# -----------------------
user_message = """
请编写一个 Python 函数 fibonacci(n)，返回第 n 个斐波那契数。
先测试代码正确性，如果测试通过再进行优化，并给出最终代码。
"""

# -----------------------
# 调用 Agent
# -----------------------
response = agent.invoke(
    {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    }
)

# -----------------------
# 输出结果
# -----------------------
print("\n--- Agent 输出 ---\n")
print(response["messages"][-1].content)