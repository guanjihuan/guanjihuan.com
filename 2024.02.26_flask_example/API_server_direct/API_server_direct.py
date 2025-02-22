from flask import Flask, request

app = Flask(__name__)

def get_response(user_input):
    response = f"你说了'{user_input}'，我想了想。"
    return response

@app.route('/', methods=['POST'])
def API_server():
    try:
        data = request.get_json()  # 从请求的 JSON 数据中获取用户输入
        user_input = data.get('prompt', '')  # 获取 'prompt' 字段
    except Exception as e:
        return '请求错误！请联系 API 管理员。'  # 如果解析失败，则返回错误信息
    if not user_input:
        return "请求错误！请联系 API 管理员。"  # 如果没有输入，则返回错误
    ai_response = get_response(user_input)
    return ai_response

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=123)