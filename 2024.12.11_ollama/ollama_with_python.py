# 直接输出
import ollama
response = ollama.chat(model="llama3.2:latest", messages=[{"role": "user","content": "你好"}], stream=False)
print(response['message']['content'])

# 流式输出
import ollama
response = ollama.chat(model="llama3.2:latest", messages=[{"role": "user", "content": "你好"}], stream=True)
for part in response:
    print(part['message']['content'], end='', flush=True)

# 流式输出，且模型后台常驻（需要手动 ollama stop 关闭）
import ollama
response = ollama.chat(model="llama3.2:latest", messages=[{"role": "user", "content": "你好"}], stream=True, keep_alive=-1)
for part in response:
    print(part['message']['content'], end='', flush=True)
