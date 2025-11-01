import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_openai_tools_agent, AgentExecutor

# 加载环境变量
dotenv.load_dotenv()

# 定义工具（Tool）
@tool
def get_current_time() -> str:
    """获取当前日期和时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def add_numbers(a: float, b: float) -> float:
    """将两个数字相加"""
    return a + b

# 注意：你可以添加更多工具，比如天气查询、网络搜索等

tools = [get_current_time, add_numbers]

# 创建 LLM（必须支持 function calling）
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    model="qwen-plus",
    temperature=0.7,
    streaming=True,
)

# 构建提示模板（LangChain 会自动注入工具信息）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手，可以使用工具来回答问题。"),
    ("human", "{input_message}"),
    ("placeholder", "{agent_scratchpad}"),  # 必须包含这个占位符
])

# 创建 OpenAI 工具型智能体（兼容 function calling）
agent = create_openai_tools_agent(llm, tools, prompt)

# 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 打印中间步骤（可选）
    handle_parsing_errors=True,
)

# 非流式调用（AgentExecutor 目前对流式支持有限，尤其在工具调用场景）
response = agent_executor.invoke({"input_message": "现在几点了？然后把 123 和 456 加起来。"})
print('\n---\n')
print(response["output"])