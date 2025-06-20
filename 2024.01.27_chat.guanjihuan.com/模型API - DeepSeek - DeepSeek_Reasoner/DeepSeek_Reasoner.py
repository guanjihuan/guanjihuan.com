"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

import openai
API_BASE = "https://api.deepseek.com"
API_KEY = "your key"


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
    message_placeholder = st.empty()

def response_of_deepseek_chat(prompt):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    client = openai.OpenAI(
        api_key=API_KEY,
        base_url=API_BASE
    )
    completion = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=st.session_state.messages,
        stream=True,
        temperature=temperature, 
        top_p=top_p,
    )
    full_content = ''
    all_full_content = ''
    think_or_not = 1
    answer_or_not = 1
    for chunk in completion:
        response = chunk.choices[0].delta.content
        reasoning_content = chunk.choices[0].delta.reasoning_content
        if response == None:
            if think_or_not == 1:
                all_full_content += '[开始思考]\n\n'
                think_or_not = 0
            all_full_content += reasoning_content
        else:
            if answer_or_not == 1:
                all_full_content += '\n\n[结束思考]\n\n'
                answer_or_not = 0
            all_full_content += response
            full_content += response
        message_placeholder.markdown(all_full_content)
        if stop_button:
            break
    st.session_state.messages.append({'role': 'assistant',
                        'content': full_content})
    st.session_state.ai_response.append({"role": "robot", "content": all_full_content, "avatar": "assistant"})
    return all_full_content
    
if prompt:
    prompt_placeholder.markdown(prompt)
    st.session_state.ai_response.append({"role": "user", "content": prompt, "avatar": 'user'})
    stop = st.empty()
    stop_button = stop.button('停止', key='break_response')
    response_of_deepseek_chat(prompt)
    stop.empty()
button_clear = st.button("清空", on_click=clear_all, key='clear')
  