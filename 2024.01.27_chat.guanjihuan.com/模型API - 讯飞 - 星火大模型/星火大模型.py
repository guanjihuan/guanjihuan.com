"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

# 以下密钥信息从控制台获取
appid = " "     # 填写控制台中获取的 APPID 信息
api_secret = " "   # 填写控制台中获取的 APISecret 信息
api_key =" "    # 填写控制台中获取的 APIKey 信息

with st.sidebar:
    with st.expander('模型', expanded=True):
        API_model = st.radio('选择：', ('讯飞 - 星火大模型 V1.5', '讯飞 - 星火大模型 V2.0', '讯飞 - 星火大模型 V3.0', '讯飞 - 星火大模型 V3.5'), key='choose_API_model')
        if API_model == '讯飞 - 星火大模型 V1.5':
            API_model_0 = '星火大模型 V1.5'
        elif API_model == '讯飞 - 星火大模型 V2.0':
            API_model_0 = '星火大模型 V2.0'
        elif API_model == '讯飞 - 星火大模型 V3.0':
            API_model_0 = '星火大模型 V3.0'
        elif API_model == '讯飞 - 星火大模型 V3.5':
            API_model_0 = '星火大模型 V3.5'
        st.write('当前模型：'+API_model_0)

    with st.expander('参数', expanded=True):
        top_k = st.slider('top_k', 1, 6, value=4, step=1, key='top_k_session')
        temperature = st.slider('temperature', 0.01, 1.0, value=0.5, step=0.01, key='temperature_session')
        def reset_parameter():
            st.session_state['top_k_session'] = 4
            st.session_state['temperature_session'] = 0.5
        reset_parameter_button = st.button('重置', on_click=reset_parameter)

# 云端环境的服务地址
if API_model == '讯飞 - 星火大模型 V1.5':
    domain = "general"   # v1.5版本
    Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
elif API_model == '讯飞 - 星火大模型 V2.0':
    domain = "generalv2"    # v2.0版本
    Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
elif API_model == '讯飞 - 星火大模型 V3.0':
    domain = "generalv3"    # v3.0版本
    Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
elif API_model == '讯飞 - 星火大模型 V3.5':
    domain = "generalv3.5"    # v3.5版本
    Spark_url = "ws://spark-api.xf-yun.com/v3.5/chat"  # v3.5环境的地址

import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket  # 使用websocket_client
answer = ""

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)

# 收到websocket关闭的处理
def on_close(ws,one,two):
    print(" ")

# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))

def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain= ws.domain,question=ws.question))
    ws.send(data)

# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        global answer
        answer += content
        message_placeholder.markdown(answer)
        if status == 2:
            ws.close()

def gen_params(appid, domain,question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "random_threshold": 0.5,
                "temperature": temperature,
                "top_k": top_k,
                "max_tokens": 4096,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data

def main_chat(appid, api_key, api_secret, Spark_url,domain, question):
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def getlength(text):
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def getText(role,content, text):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        text.append(jsoncon)
        return text

prompt_text = st.chat_input("请在这里输入您的命令")

if API_model == '讯飞 - 星火大模型 V1.5':
    if "text" not in st.session_state:
        st.session_state.text = []
    if "messages" not in st.session_state:
        st.session_state.messages = [] 
    def clear_all():
        st.session_state.messages = []
        st.session_state.text = []
    if st.session_state.messages == []:
        with st.chat_message("user", avatar="user"):
            input_placeholder = st.empty()
        with st.chat_message("robot", avatar="assistant"):
            message_placeholder = st.empty()
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])
    if prompt_text:
        if st.session_state.messages != []:
            with st.chat_message("user", avatar="user"):
                input_placeholder = st.empty()
            with st.chat_message("robot", avatar="assistant"):
                message_placeholder = st.empty()
        input_placeholder.markdown(prompt_text)
        st.session_state.messages.append({"role": "user", "content": prompt_text, "avatar": "user"})
        st.session_state.text = getText("user", prompt_text, st.session_state.text)
        question = checklen(st.session_state.text)
        main_chat(appid,api_key,api_secret,Spark_url,domain,question)
        st.session_state.text = getText("assistant", answer, st.session_state.text)
        st.session_state.messages.append({"role": "robot", "content": answer, "avatar": "assistant"})
        st.rerun()
    button_clear = st.button("清空", on_click=clear_all)

elif  API_model == '讯飞 - 星火大模型 V2.0':
    if "text2" not in st.session_state:
        st.session_state.text2 = []
    if "messages2" not in st.session_state:
        st.session_state.messages2 = [] 
    def clear_all2():
        st.session_state.messages2 = []
        st.session_state.text2 = []
    if st.session_state.messages2 == []:
        with st.chat_message("user", avatar="user"):
            input_placeholder = st.empty()
        with st.chat_message("robot", avatar="assistant"):
            message_placeholder = st.empty()
    for message in st.session_state.messages2:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])
    if prompt_text:
        if st.session_state.messages2 != []:
            with st.chat_message("user", avatar="user"):
                input_placeholder = st.empty()
            with st.chat_message("robot", avatar="assistant"):
                message_placeholder = st.empty()
        input_placeholder.markdown(prompt_text)
        st.session_state.messages2.append({"role": "user", "content": prompt_text, "avatar": "user"})
        st.session_state.text2 = getText("user", prompt_text, st.session_state.text2)
        question = checklen(st.session_state.text2)
        main_chat(appid,api_key,api_secret,Spark_url,domain,question)
        st.session_state.text2 = getText("assistant", answer, st.session_state.text2)
        st.session_state.messages2.append({"role": "robot", "content": answer, "avatar": "assistant"})
        st.rerun()
    button_clear = st.button("清空", on_click=clear_all2, key='clear2')

elif  API_model == '讯飞 - 星火大模型 V3.0':
    if "text3" not in st.session_state:
        st.session_state.text3 = []
    if "messages3" not in st.session_state:
        st.session_state.messages3 = [] 
    def clear_all3():
        st.session_state.messages3 = []
        st.session_state.text3 = []
    if st.session_state.messages3 == []:
        with st.chat_message("user", avatar="user"):
            input_placeholder = st.empty()
        with st.chat_message("robot", avatar="assistant"):
            message_placeholder = st.empty()
    for message in st.session_state.messages3:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])
    if prompt_text:
        if st.session_state.messages3 != []:
            with st.chat_message("user", avatar="user"):
                input_placeholder = st.empty()
            with st.chat_message("robot", avatar="assistant"):
                message_placeholder = st.empty()
        input_placeholder.markdown(prompt_text)
        st.session_state.messages3.append({"role": "user", "content": prompt_text, "avatar": "user"})
        st.session_state.text3 = getText("user", prompt_text, st.session_state.text3)
        question = checklen(st.session_state.text3)
        main_chat(appid,api_key,api_secret,Spark_url,domain,question)
        st.session_state.text3 = getText("assistant", answer, st.session_state.text3)
        st.session_state.messages3.append({"role": "robot", "content": answer, "avatar": "assistant"})
        st.rerun()
    button_clear = st.button("清空", on_click=clear_all3, key='clear3')

elif  API_model == '讯飞 - 星火大模型 V3.5':
    if "text4" not in st.session_state:
        st.session_state.text4 = []
    if "messages4" not in st.session_state:
        st.session_state.messages4 = [] 
    def clear_all4():
        st.session_state.messages4 = []
        st.session_state.text4 = []
    if st.session_state.messages4 == []:
        with st.chat_message("user", avatar="user"):
            input_placeholder = st.empty()
        with st.chat_message("robot", avatar="assistant"):
            message_placeholder = st.empty()
    for message in st.session_state.messages4:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])
    if prompt_text:
        if st.session_state.messages4 != []:
            with st.chat_message("user", avatar="user"):
                input_placeholder = st.empty()
            with st.chat_message("robot", avatar="assistant"):
                message_placeholder = st.empty()
        input_placeholder.markdown(prompt_text)
        st.session_state.messages4.append({"role": "user", "content": prompt_text, "avatar": "user"})
        st.session_state.text4 = getText("user", prompt_text, st.session_state.text4)
        question = checklen(st.session_state.text4)
        main_chat(appid,api_key,api_secret,Spark_url,domain,question)
        st.session_state.text4 = getText("assistant", answer, st.session_state.text4)
        st.session_state.messages4.append({"role": "robot", "content": answer, "avatar": "assistant"})
        st.rerun()
    button_clear = st.button("清空", on_click=clear_all4, key='clear4')