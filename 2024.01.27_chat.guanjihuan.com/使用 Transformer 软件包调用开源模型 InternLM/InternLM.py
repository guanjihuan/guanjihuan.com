"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

@st.cache_resource
def load_model_internlm_7B():
    # internlm（需要 7G 显存）
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
    )
    model = AutoModelForCausalLM.from_pretrained("internlm/internlm-chat-7b", trust_remote_code=True, quantization_config=nf4_config)
    tokenizer = AutoTokenizer.from_pretrained("internlm/internlm-chat-7b", trust_remote_code=True, torch_dtype=torch.bfloat16)
    model = model.eval()
    return model, tokenizer
model_internlm_7B, tokenizer_internlm_7B = load_model_internlm_7B()

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

from tools.transformers.interface import GenerationConfig, generate_interactive

def prepare_generation_config():
    generation_config = GenerationConfig(max_length=max_length, top_p=top_p, temperature=temperature)
    return generation_config

def combine_history(prompt, messages):
    total_prompt = ""
    for message in messages:
        cur_content = message["content"]
        if message["role"] == "user":
            cur_prompt = user_prompt.replace("{user}", cur_content)
        elif message["role"] == "robot":
            cur_prompt = robot_prompt.replace("{robot}", cur_content)
        else:
            raise RuntimeError
        total_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.replace("{user}", prompt)
    return total_prompt

user_prompt = "<|User|>:{user}<eoh>\n"
robot_prompt = "<|Bot|>:{robot}<eoa>\n"
cur_query_prompt = "<|User|>:{user}<eoh>\n<|Bot|>:"
generation_config = prepare_generation_config()

if "messages_internlm_7B" not in st.session_state:
    st.session_state.messages_internlm_7B = []

from dataclasses import asdict

def chat_response_internlm_7B(prompt):
    real_prompt = combine_history(prompt, messages = st.session_state.messages_internlm_7B)
    st.session_state.messages_internlm_7B.append({"role": "user", "content": prompt, "avatar": 'user'})
    for cur_response in generate_interactive(
        model=model_internlm_7B,
        tokenizer=tokenizer_internlm_7B,
        prompt=real_prompt,
        additional_eos_token_id=103028,
        **asdict(generation_config),
    ):
        message_placeholder_internlm_7B.markdown(cur_response + "▌")
        if stop_button:
            break
    message_placeholder_internlm_7B.markdown(cur_response)
    st.session_state.messages_internlm_7B.append({"role": "robot", "content": cur_response, "avatar": "assistant"})
    st.session_state.ai_response.append({"role": "robot", "content": cur_response, "avatar": "assistant"})
    return cur_response


def clear_all():
    st.session_state.messages_internlm_7B = []
    st.session_state.ai_response = []

if 'messages_internlm_7B' not in st.session_state:
    st.session_state.messages_internlm_7B = []
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = []

for ai_response in st.session_state.ai_response:
    with st.chat_message(ai_response["role"], avatar=ai_response.get("avatar")):
        st.markdown(ai_response["content"])

prompt_placeholder = st.chat_message("user", avatar='user')
with st.chat_message("robot", avatar="assistant"):
    message_placeholder_internlm_7B = st.empty()

if prompt:
    prompt_placeholder.markdown(prompt)
    st.session_state.ai_response.append({"role": "user", "content": prompt, "avatar": 'user'})
    stop = st.empty()
    stop_button = stop.button('停止', key='break_response')
    chat_response_internlm_7B(prompt)
    stop.empty()
button_clear = st.button("清空", on_click=clear_all, key='clear')