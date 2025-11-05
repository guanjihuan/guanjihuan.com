"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/47909
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 创建聊天模型 - 修改为调用 Ollama
llm = ChatOpenAI(
    api_key="ollama",  # 对于 Ollama，API key 可以设为任意值或 "ollama"
    base_url="http://localhost:11434/v1",  # Ollama 的本地 API 地址
    model="qwen2.5:3b",  # 替换为你本地安装的模型名称，如 qwen2.5 等
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