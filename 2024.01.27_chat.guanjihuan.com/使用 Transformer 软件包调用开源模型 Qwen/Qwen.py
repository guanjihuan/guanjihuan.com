"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

choose_load_model = 0  # 选择加载的模型（Qwen-7B 或 Qwen-14B）

if choose_load_model == 0:
    # Qwen-7B（需要8G显存）
    @st.cache_resource
    def load_model_qwen_7B():
        from transformers import AutoTokenizer, AutoModelForCausalLM
        tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat-Int4", trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen-7B-Chat-Int4",
            device_map="auto",
            trust_remote_code=True,
        ).eval()
        return tokenizer, model
    tokenizer_qwen_7B, model_qwen_7B = load_model_qwen_7B()

elif choose_load_model == 1:
    # Qwen-14B（需要12G显存）
    @st.cache_resource
    def load_model_qwen_14B():
        from transformers import AutoTokenizer, AutoModelForCausalLM
        tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-14B-Chat-Int4", trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen-14B-Chat-Int4",
            device_map="auto",
            trust_remote_code=True
        ).eval()
        return tokenizer, model
    tokenizer_qwen_14B, model_qwen_14B = load_model_qwen_14B()

with st.sidebar:
    with st.expander('参数', expanded=True):
        max_length = 409600
        top_p = st.slider('top_p', 0.01, 1.0, step=0.01, value=0.8, key='top_p_session')
        temperature = st.slider('temperature', 0.51, 1.0, step=0.01, value=0.8, key='temperature_session') 
        def reset_parameter():
            st.session_state['top_p_session'] = 0.8
            st.session_state['temperature_session'] = 0.8
        reset_parameter_button = st.button('重置', on_click=reset_parameter)

prompt = st.chat_input("在这里输入您的命令")

from transformers.generation import GenerationConfig

if choose_load_model == 0:
    config_qwen_7b = GenerationConfig.from_pretrained(
        "Qwen/Qwen-7B-Chat-Int4", trust_remote_code=True, resume_download=True, max_length = max_length, top_p = top_p, temperature = temperature
    )
    def chat_response_qwen_7B(query):
        for response in model_qwen_7B.chat_stream(tokenizer_qwen_7B, query, history=st.session_state.history_qwen, generation_config=config_qwen_7b):
            message_placeholder_qwen.markdown(response)
            if stop_button:
                break
        st.session_state.history_qwen.append((query, response))
        st.session_state.ai_response.append({"role": "robot", "content": response, "avatar": "assistant"})
        return response

elif choose_load_model == 1:
    config_qwen_14b = GenerationConfig.from_pretrained(
        "Qwen/Qwen-14B-Chat-Int4", trust_remote_code=True, resume_download=True, max_length = max_length, top_p = top_p, temperature = temperature
    )
    def chat_response_qwen_14B(query):
        for response in model_qwen_14B.chat_stream(tokenizer_qwen_14B, query, history=st.session_state.history_qwen, generation_config=config_qwen_14b):
            message_placeholder_qwen.markdown(response)
            if stop_button:
                break
        st.session_state.history_qwen.append((query, response))
        st.session_state.ai_response.append({"role": "robot", "content": response, "avatar": "assistant"})
        return response

def clear_all():
    st.session_state.history_qwen = []
    st.session_state.ai_response = []

if 'history_qwen' not in st.session_state:
    st.session_state.history_qwen = []
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = []

for ai_response in st.session_state.ai_response:
    with st.chat_message(ai_response["role"], avatar=ai_response.get("avatar")):
        st.markdown(ai_response["content"])

prompt_placeholder = st.chat_message("user", avatar='user')
with st.chat_message("robot", avatar="assistant"):
    message_placeholder_qwen = st.empty()

if prompt:
    prompt_placeholder.markdown(prompt)
    st.session_state.ai_response.append({"role": "user", "content": prompt, "avatar": 'user'})
    stop = st.empty()
    stop_button = stop.button('停止', key='break_response')
    if choose_load_model == 0:
        chat_response_qwen_7B(prompt)
    elif choose_load_model == 1:
        chat_response_qwen_14B(prompt)
    stop.empty()
button_clear = st.button("清空", on_click=clear_all, key='clear')