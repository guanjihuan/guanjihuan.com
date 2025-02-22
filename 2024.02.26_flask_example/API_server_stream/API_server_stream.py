from flask import Flask, Response, request

app = Flask(__name__)

def get_response(user_input):
    import time
    ai_response = f"你说了'{user_input}'，我想了想。"
    for char in ai_response:
        yield f"{char}\n\n"
        time.sleep(0.2)

@app.route('/', methods=['POST'])
def API_server():
    try:
        data = request.get_json() # 从请求的 JSON 数据中获取用户输入
        user_input = data.get('prompt', '')  # 获取 'prompt' 字段
    except Exception as e:
        return '请求错误！请联系 API 管理员。' # 如果解析失败，则返回错误信息
    if not user_input:
        return "请求错误！请联系 API 管理员。" # 如果没有输入，则返回错误
    return Response(get_response(user_input), content_type='text/event-stream') # 返回流式响应

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=123)