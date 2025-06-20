"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

from zhipuai import ZhipuAI  # 在这个版本中测试有效：Version-2.1.5.20250106
 
client = ZhipuAI(api_key="")

with st.sidebar:
    with st.expander('参数', expanded=True):
        top_p = st.slider('top_p', 0.01, 1.0, value=0.7, step=0.01, key='top_p_session')
        temperature = st.slider('temperature', 0.01, 1.0, value=0.95, step=0.01, key='temperature_session')
        def reset_parameter():
            st.session_state['top_p_session'] = 0.7
            st.session_state['temperature_session'] = 0.95
        reset_parameter_button = st.button('重置', on_click=reset_parameter)

def chatglm_chat(prompt=[]):
    response = client.chat.completions.create(
        model="glm-4-air",
        messages=prompt,
        top_p= top_p,
        temperature= temperature,
        stream=True
    )
    return response

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

answer = ""
if "text0" not in st.session_state:
    st.session_state.text0 = []
if "messages0" not in st.session_state:
    st.session_state.messages0 = [] 
def clear_all0():
    st.session_state.messages0 = []
    st.session_state.text0 = []
if st.session_state.messages0 == []:
    with st.chat_message("user", avatar="user"):
        input_placeholder = st.empty() 
    with st.chat_message("robot", avatar="assistant"):
        message_placeholder = st.empty()
for message in st.session_state.messages0:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])
prompt_text = st.chat_input("请在这里输入您的命令")

if prompt_text:
    if st.session_state.messages0 != []:
        with st.chat_message("user", avatar="user"):
            input_placeholder = st.empty()
        with st.chat_message("robot", avatar="assistant"):
            message_placeholder = st.empty()
    input_placeholder.markdown(prompt_text)
    st.session_state.messages0.append({"role": "user", "content": prompt_text, "avatar": "user"})
    st.session_state.text0 = getText("user", prompt_text, st.session_state.text0)
    question = checklen(st.session_state.text0)
    response  = chatglm_chat(question)
    for chunk in response:
        answer += chunk.choices[0].delta.content or ""
        message_placeholder.markdown(answer)
    st.session_state.text0 = getText("assistant", answer, st.session_state.text0)
    st.session_state.messages0.append({"role": "robot", "content": answer, "avatar": "assistant"})
    st.rerun()
button_clear = st.button("清空", on_click=clear_all0, key='clear0')
