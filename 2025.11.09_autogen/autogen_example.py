"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/48024
"""

import os
import autogen
import dotenv

dotenv.load_dotenv()

config_list = [
    {
        "model": "qwen-plus",
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "base_url": os.getenv("DASHSCOPE_BASE_URL"),
        "price": [0.0008, 0.002],
    }
]

# 数学专家
math_expert = autogen.AssistantAgent(
    name="MathExpert",
    system_message="你是一个数学专家，擅长解决各种数学问题。",
    llm_config={"config_list": config_list},
)

# 物理专家
physics_expert = autogen.AssistantAgent(
    name="PhysicsExpert",
    system_message="你是一个物理专家，擅长解决各种物理问题。",
    llm_config={"config_list": config_list},
)

# 人工智能专家
AI_expert = autogen.AssistantAgent(
    name="AIExpert",
    system_message="你是一个人工智能专家，擅长解决各种人工智能问题。",
    llm_config={"config_list": config_list},
)

# 用户代理
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding", "use_docker": False},
)

# 简单群聊
groupchat = autogen.GroupChat(
    agents=[math_expert, physics_expert, AI_expert, user_proxy],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin", # 轮流发言
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list},
)

# 启动任务
user_proxy.initiate_chat(
    manager,
    message="随便讨论一个话题，多相互讨论，每个人每次发言不超过200字。"
)