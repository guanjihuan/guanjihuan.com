"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/48066
"""

from llama_cpp import Llama
import time

class QwenChatbotGGUF:
    def __init__(self, model_path="D:/models/Qwen/Qwen3-0.6B-GGUF/Qwen3-0.6B-Q8_0.gguf", n_ctx=32768):
        """
        初始化基于 GGUF 的 Qwen3 聊天机器人
        :param model_path: GGUF 模型文件路径（必须是 Qwen3 的 GGUF 文件）
        :param n_ctx: 上下文长度（Qwen3 支持长上下文，最大可设 32768）
        """
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            verbose=False,
            chat_format="chatml",  # Qwen 使用 ChatML 格式
            logits_all=False
        )
        self.history = []

    def generate_response(self, user_input):
        """
        生成模型回复
        :param user_input: 用户输入文本
        :return: 模型回复文本
        """
        # 将当前输入加入历史（role=user）
        self.history.append({"role": "user", "content": user_input})

        # 使用 llama.cpp 内置的 chat completion（自动处理模板）
        response = self.llm.create_chat_completion(
            messages=self.history,
            max_tokens=2048,
            temperature=0.6,
            top_p=0.95,
            repeat_penalty=1.5,
        )

        # 提取助手回复内容
        assistant_message = response["choices"][0]["message"]["content"].strip()

        # 将助手回复加入历史
        self.history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

# 示例使用
if __name__ == "__main__":
    chatbot = QwenChatbotGGUF()  # 创建聊天机器人实例

    # 第一次输入
    start_time = time.time()
    user_input_1 = "计算：1+1"
    print(f"用户: {user_input_1}")
    response_1 = chatbot.generate_response(user_input_1)
    print(f"机器人: {response_1}")
    end_time = time.time()
    print(f"\n--- 分割线（耗时：{end_time - start_time:.2f} 秒） ---\n")

    # 第二次输入（带 /no_think）
    start_time = time.time()
    user_input_2 = "确定吗？/no_think"
    print(f"用户: {user_input_2}")
    response_2 = chatbot.generate_response(user_input_2)
    print(f"机器人: {response_2}")
    end_time = time.time()
    print(f"\n--- 分割线（耗时：{end_time - start_time:.2f} 秒） ---\n")

    # 第三次输入（带 /think）
    start_time = time.time()
    user_input_3 = "确定吗？/think"
    print(f"用户: {user_input_3}")
    response_3 = chatbot.generate_response(user_input_3)
    print(f"机器人: {response_3}")
    end_time = time.time()
    print(f"\n--- 分割线（耗时：{end_time - start_time:.2f} 秒） ---\n")