"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/47925
"""

import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_experimental.tools import PythonREPLTool

# 加载环境变量
dotenv.load_dotenv()

# 初始化 LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    model="qwen-plus",
    temperature=0,
)

# 使用官方 PythonREPLTool（⚠️ 注意：此工具可执行任意代码，仅用于安全环境）
tools = [PythonREPLTool()]  # 直接实例化即可，它已是 Tool 类型

# 构建 ReAct Prompt
template = """你是一个严谨的 Python 编程助手，必须通过工具执行代码来验证逻辑，不能仅靠推理得出结论。

## 工具
你可以使用以下工具：
{tools}

## 规则
- 每次只能执行一个 Action。
- 所有 Python 代码必须通过工具执行，不得假设输出结果。
- **Action Input 必须是纯 Python 代码，不要包含 Markdown 代码块符号（如 ``` 或 ```python）。**
- 如果测试失败（如 assert 报错），请根据错误信息修正代码并重新测试。
- 最终答案必须基于工具返回的正确执行结果。
- 输出必须严格遵循以下格式，不要添加额外内容：

Question: <用户问题>
Thought: <你的思考>
Action: <工具名称>
Action Input: <纯 Python 代码（不要 Markdown 代码块）>
Observation: <工具返回结果>
...（重复以上步骤）
Final Answer: <最终答案，包含正确函数和简要说明>

## 可用工具
{tool_names}

当前问题: {input_message}
{agent_scratchpad}"""


prompt = PromptTemplate.from_template(template)

# 创建并执行 Agent
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True
)

# 运行任务
if __name__ == "__main__":
    response = executor.invoke({
        "input_message": "请编写一个 Python 函数 fibonacci(n)，返回第 n 个斐波那契数。测试通过后做代码的优化，并给出最终代码。"
    })
    print(response["output"])