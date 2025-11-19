"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/48066
"""

from modelscope import AutoModelForCausalLM, AutoTokenizer
import time

class QwenChatbot:
    def __init__(self, model_name="D:/models/Qwen/Qwen3-0.6B"):
        """
        初始化 Qwen 聊天机器人
        :param model_name: 模型路径
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)  # 加载分词器
        self.model = AutoModelForCausalLM.from_pretrained(model_name)  # 加载模型
        self.history = []  # 存储对话历史

    def generate_response(self, user_input):
        """
        生成模型回复
        :param user_input: 用户输入
        :return: 模型回复
        """
        # 将历史对话和当前用户输入组合成消息列表
        messages = self.history + [{"role": "user", "content": user_input}]

        # 使用聊天模板格式化输入文本
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,  # 不进行分词，返回字符串
            add_generation_prompt=True  # 添加生成提示
        )

        # 对文本进行分词，并返回PyTorch张量
        inputs = self.tokenizer(text, return_tensors="pt")
        
        # 生成回复，最多生成32768个新token
        response_ids = self.model.generate(**inputs, max_new_tokens=32768)[0][len(inputs.input_ids[0]):].tolist()
        
        # 解码生成的token，跳过特殊token
        response = self.tokenizer.decode(response_ids, skip_special_tokens=True)

        # 更新对话历史
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response})

        return response

# 示例使用
if __name__ == "__main__":
    chatbot = QwenChatbot()  # 创建聊天机器人实例

    # 第一次输入（不带/think或/no_think标签，默认启用思考模式）
    start_time = time.time()
    user_input_1 = "计算：1+1"
    print(f"用户: {user_input_1}")
    response_1 = chatbot.generate_response(user_input_1)
    print(f"机器人: {response_1}")
    end_time = time.time()
    print(f"\n--- 分割线（耗时：{end_time-start_time:.2f} 秒） ---\n")

    # 第二次输入带/no_think标签
    start_time = time.time()
    user_input_2 = "确定吗？/no_think"
    print(f"用户: {user_input_2}")
    response_2 = chatbot.generate_response(user_input_2)
    print(f"机器人: {response_2}") 
    end_time = time.time()
    print(f"\n--- 分割线（耗时：{end_time-start_time:.2f} 秒） ---\n")

    # 第三次输入带/think标签
    start_time = time.time()
    user_input_3 = "确定吗？/think"
    print(f"用户: {user_input_3}")
    response_3 = chatbot.generate_response(user_input_3)
    print(f"机器人: {response_3}")
    end_time = time.time()
    print(f"\n--- 分割线（耗时：{end_time-start_time:.2f} 秒） ---\n")