"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

import json
import types
# 安装：pip install --upgrade tencentcloud-sdk-python
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

with st.sidebar:
    with st.expander('参数', expanded=True):
        top_p = st.slider('top_p', 0.01, 1.0, step=0.01, value=0.8, key='top_p_session')
        temperature = st.slider('temperature', 0.51, 1.0, step=0.01, value=0.85, key='temperature_session') 
        def reset_parameter():
            st.session_state['top_p_session'] = 0.8
            st.session_state['temperature_session'] = 0.85
        reset_parameter_button = st.button('重置', on_click=reset_parameter)

prompt = st.chat_input("在这里输入您的命令")

def clear_all():
    st.session_state.messages = []
    st.session_state.ai_response = []

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = []

for ai_response in st.session_state.ai_response:
    with st.chat_message(ai_response["role"], avatar=ai_response.get("avatar")):
        st.markdown(ai_response["content"])

prompt_placeholder = st.chat_message("user", avatar='user')
with st.chat_message("robot", avatar="assistant"):
    message_placeholder_hunyuan = st.empty()

def response_of_hunyuan(prompt):
    st.session_state.messages.append({'Role': 'user', 'Content': prompt})
    # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
    # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
    # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
    cred = credential.Credential("SecretId", "SecretKey")
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = hunyuan_client.HunyuanClient(cred, "", clientProfile)

    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.ChatCompletionsRequest()
    params = {
        "Model": "hunyuan-lite",
        "Messages": st.session_state.messages,
        "TopP": top_p,
        "Temperature": temperature,
        "Stream": True,
    }
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个ChatCompletionsResponse的实例，与请求对象对应
    resp = client.ChatCompletions(req)
    # 输出json格式的字符串回包
    response = ''
    if isinstance(resp, types.GeneratorType):  # 流式响应
        for event in resp:
            answer = json.loads(event['data'])
            response += answer["Choices"][0]['Delta']['Content']
            message_placeholder_hunyuan.markdown(response)
            if stop_button:
                break
        st.session_state.messages.append({'Role': 'assistant', 'Content': response})
        st.session_state.ai_response.append({"role": "robot", "content": response, "avatar": "assistant"})
    return response


if prompt:
    prompt_placeholder.markdown(prompt)
    st.session_state.ai_response.append({"role": "user", "content": prompt, "avatar": 'user'})
    stop = st.empty()
    stop_button = stop.button('停止', key='break_response')
    response_of_hunyuan(prompt)
    stop.empty()
button_clear = st.button("清空", on_click=clear_all, key='clear')