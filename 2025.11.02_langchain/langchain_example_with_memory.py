import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 加载 .env 中的 API 密钥等配置
load_dotenv()

# 初始化大模型
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    model="qwen-plus",
    temperature=0.7
)

# 定义带历史记录的提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的助手。"),
    MessagesPlaceholder("history"),  # 历史消息占位符
    ("human", "{input}")            # 当前用户输入
])

# 创建基础链
chain = prompt | llm

# 内存存储：用字典模拟会话历史（仅用于演示）
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 包装成带记忆的链
chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

def chat_with_agent(input_message, session_id):
    print(f"用户: {input_message}")
    print("助手: ", end="", flush=True)
    for chunk in chatbot.stream(
        {"input": input_message},
        config={"configurable": {"session_id": session_id}}  # 多轮对话（使用同一个 session_id）
    ):
        print(chunk.content, end="", flush=True)
    print("\n\n---\n")

chat_with_agent(input_message='一句话解释下人工智能。', session_id="user_001") 

chat_with_agent(input_message='我们都聊了什么？', session_id="user_001") 

chat_with_agent(input_message='我们都聊了什么？', session_id="user_002") 

chat_with_agent(input_message='我们都聊了什么？', session_id="user_001") 