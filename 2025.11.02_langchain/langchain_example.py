"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/47909
"""

import langchain_openai
from langchain_core.prompts import ChatPromptTemplate
import dotenv
import os

# 加载环境变量（包含API密钥）
dotenv.load_dotenv()

# 创建聊天模型
llm = langchain_openai.ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 从环境变量获取 API 密钥
    base_url=os.getenv("DASHSCOPE_BASE_URL"),  # 指定 API 端点
    model="qwen-plus",  # 使用通义千问 Plus 模型
    temperature=0.7,  # 控制回复的随机性（0-1，越高越有创意）
    streaming=True,  # 启用流式模式
)

# 创建简单的提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的聊天助手。"),  # 系统角色设定
    ("human", "{question}")   # 用户输入占位符
])

# 创建处理链
chain = prompt | llm  # 使用管道操作符连接组件

# 使用 stream() 实现流式输出
for chunk in chain.stream({"question": "你好"}):
    print(chunk.content, end="", flush=True)
print()  # 换行

# # 非流式输出
# response = chain.invoke({"question": "你好"})
# print(response.content)