import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

import requests
import json

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[应用API Key]&client_secret=[应用Secret Key]"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


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

def response_of_ernie_speed_128k(prompt):
    st.session_state.messages.append({'role': "user", 'content': prompt})
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": st.session_state.messages,
        "top_p": top_p,
        "temperature": temperature, 
        "stream": True
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    full_content = ''
    for line in response.iter_lines():
        try:
            dict_data = json.loads(line.decode("UTF-8")[5:])
            full_content += dict_data['result']
            message_placeholder.markdown(full_content)
        except:
            pass
        if stop_button:
            break
    st.session_state.messages.append({'role': "assistant",
                        'content': full_content})
    st.session_state.ai_response.append({"role": "robot", "content": full_content, "avatar": "assistant"})
    return full_content

if prompt:
    prompt_placeholder.markdown(prompt)
    st.session_state.ai_response.append({"role": "user", "content": prompt, "avatar": 'user'})
    stop = st.empty()
    stop_button = stop.button('停止', key='break_response')
    response_of_ernie_speed_128k(prompt)
    stop.empty()
button_clear = st.button("清空", on_click=clear_all, key='clear')