import requests

url = "http://localhost:123" # API 地址
data = {
    "prompt": "Hello, how are you?"   # 请求数据，prompt 为用户输入
} 
response = requests.post(url, json=data, stream=True)  # 发送 POST 请求，传递 JSON 数据并启用流式响应
if response.status_code == 200: # 检查响应是否成功
    for line in response.iter_lines(): # 逐步读取并打印流式响应
        if line:
            print(line.decode('utf-8'), end='', flush=True) # 解码并打印每一行流式返回的数据
else:
    print(f"请求失败，状态码: {response.status_code}")