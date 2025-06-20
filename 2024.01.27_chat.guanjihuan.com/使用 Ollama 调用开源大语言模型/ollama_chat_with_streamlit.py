"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
import ollama

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

model_name = 'llama3.2' 

prompt = st.chat_input("在这里输入您的内容")

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
    message_placeholder = st.empty()

def response_of_chat(prompt):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    response = ollama.chat(model=model_name, messages=st.session_state.messages, stream=True)
    full_content = ''
    for part in response:
        full_content += part['message']['content']
        message_placeholder.markdown(full_content)
        if stop_button:
            break
    st.session_state.messages.append({'role': 'assistant',
                        'content': full_content})
    st.session_state.ai_response.append({"role": "robot", "content": full_content, "avatar": "assistant"})
    return full_content
    
if prompt:
    prompt_placeholder.markdown(prompt)
    st.session_state.ai_response.append({"role": "user", "content": prompt, "avatar": 'user'})
    stop = st.empty()
    stop_button = stop.button('停止', key='break_response')
    response = response_of_chat(prompt)
    stop.empty()
button_clear = st.button("清空", on_click=clear_all, key='clear')
  