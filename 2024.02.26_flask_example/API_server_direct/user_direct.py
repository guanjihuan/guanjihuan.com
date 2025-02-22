import requests

url = "http://localhost:123"  # API 地址
data = {
    "prompt": "Hello, how are you?"  # 请求数据，prompt 为用户输入
} 
response = requests.post(url, json=data)  # 发送 POST 请求，传递 JSON 数据
if response.status_code == 200:  # 检查响应是否成功
    print(response.text)  # 直接获取并打印返回的完整响应
else:
    print(f"请求失败，状态码: {response.status_code}")