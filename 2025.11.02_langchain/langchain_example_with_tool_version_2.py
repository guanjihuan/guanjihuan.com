"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/47909
"""

import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.globals import set_debug # ✅ 用于开启详细日志

# 开启调试日志输出
set_debug(True)

# 加载环境变量
dotenv.load_dotenv()

# 定义工具
@tool
def get_current_time() -> str:
    """获取当前日期和时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def add_numbers(a: float, b: float) -> float:
    """将两个数字相加"""
    return a + b

tools = [get_current_time, add_numbers]

# 创建 LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    model="qwen-plus",
    temperature=0.7,
)

# 创建 agent
agent = create_agent(llm, tools)

# 执行调用（此时会打印详细步骤）
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "现在几点了？然后把 123 和 456 加起来。"}
        ]
    }
)

print("\n---\n")
print(response["messages"][-1].content)