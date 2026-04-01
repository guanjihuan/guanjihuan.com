import json
import os
from datetime import datetime
from openai import OpenAI

# --- 1. 配置 ---
import dotenv
dotenv.load_dotenv(".env")
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
)
MODEL = "ark-code-latest"

# --- 2. 工具定义 ---
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

TOOLS = {
    "get_current_time": get_current_time,
    "calculate": calculate
}

# --- 3. 动态构建 Prompt ---
def build_system_prompt():
    # 自动从 TOOLS 字典生成描述
    tool_desc = "\n".join([f"- {name}: {func.__doc__ or '无描述'}" for name, func in TOOLS.items()]) 
    system_prompt = f"""你是一个智能助手。可用工具：
{tool_desc}

请直接返回纯 JSON 格式，不要使用 Markdown 代码块。
注意：input 字段必须是一个 JSON 对象，而不是字符串。
格式：
{{
    "thought": "思考过程 或 最终回复给用户的话"
    "action": "工具名 或 final",
    "input": "参数字典 或 null",
}}"""
    return system_prompt

# --- 4. 核心逻辑 ---
def run_agent(user_input):
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_input}
    ]

    print(f"\n🚀 任务: {user_input}\n" + "-"*50)

    for step in range(5):
        print(f"\n[步骤 {step+1}] 调用大模型...\n")

        try:
            print(f'📄 模型原始输入（Raw Prompt）：\n{json.dumps(messages, indent=4, ensure_ascii=False)}')
        except:
            print(f'📄 模型原始输入（Raw Prompt）：\n{messages}')
        
        # 调用模型
        response = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
        raw_response = response.choices[0].message.content.strip()

        # --- 打印原始回复 ---
        print(f"\n📄 模型原始回复 (Raw Response):\n{raw_response}")

        # 解析与执行
        try:
            data = json.loads(raw_response)
            action = data.get("action")
            thought = data.get("thought")
            input_params = data.get("input")

            print('\n解析得到：')
            print(f"（1）思考: {thought}")
            print(f"（2）动作: {action}")
            print(f"（3）参数: {input_params}")

            if action == "final":
                print()
                print("-" * 50)
                print(f"\n✅ 最终结果: {thought}\n")
                print("-" * 50)
                print()
                return

            # 执行工具
            if action in TOOLS:
                # 自动解包参数，如果没有参数则直接调用
                result = TOOLS[action](**input_params) if input_params else TOOLS[action]()
                print(f"\n工具输出: {result}")

                # 记录历史
                messages.append({"role": "assistant", "content": raw_response})
                messages.append({"role": "user", "content": f"工具执行结果: {result}"})
            else:
                print("❌ 未知工具")
                
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            return

if __name__ == "__main__":
    run_agent("现在几点了？帮我算算 5*20 等于多少？")