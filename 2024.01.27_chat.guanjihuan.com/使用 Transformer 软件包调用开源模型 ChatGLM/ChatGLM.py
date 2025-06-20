"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

choose_load_method = 1  # 选择加载模型的方式

if choose_load_method == 0:
    # 默认加载（需要13G显存）
    @st.cache_resource
    def load_model_chatglm3():
        from transformers import AutoModel, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
        model = AutoModel.from_pretrained("THUDM/chatglm3-6b-32k",trust_remote_code=True).half().cuda()
        model = model.eval()
        return  model, tokenizer
    model_chatglm3, tokenizer_chatglm3 = load_model_chatglm3()

elif choose_load_method == 1:
    # 量化加载（需要6G显存）
    @st.cache_resource
    def load_model_chatglm3():
        from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
        tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
        )
        model = AutoModelForCausalLM.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True, quantization_config=nf4_config)
        model = model.eval()
        return  model, tokenizer
    model_chatglm3, tokenizer_chatglm3 = load_model_chatglm3()

elif choose_load_method == 2:
    # 在CPU上加载（需要25G内存，对话速度会比较慢，不推荐）
    @st.cache_resource
    def load_model_chatglm3():
        from transformers import AutoModel, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
        model = AutoModel.from_pretrained("THUDM/chatglm3-6b-32k",trust_remote_code=True).float()
        model = model.eval()
        return  model, tokenizer
    model_chatglm3, tokenizer_chatglm3 = load_model_chatglm3()

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

def chat_response_chatglm3(prompt):
    history, past_key_values = st.session_state.history_ChatGLM3, st.session_state.past_key_values_ChatGLM3
    for response, history, past_key_values in model_chatglm3.stream_chat(tokenizer_chatglm3, prompt, history,
                                                                past_key_values=past_key_values,
                                                                max_length=max_length, top_p=top_p,
                                                                temperature=temperature,
                                                                return_past_key_values=True):
        message_placeholder_chatglm3.markdown(response)
        if stop_button:
            break
    st.session_state.ai_response.append({"role": "robot", "content": response, "avatar": "assistant"})
    st.session_state.history_ChatGLM3 = history
    st.session_state.past_key_values_ChatGLM3 = past_key_values
    return response

def clear_all():
    st.session_state.history_ChatGLM3 = []
    st.session_state.past_key_values_ChatGLM3 = None
    st.session_state.ai_response = []

if 'history_ChatGLM3' not in st.session_state:
    st.session_state.history_ChatGLM3 = []
if 'past_key_values_ChatGLM3' not in st.session_state:
    st.session_state.past_key_values_ChatGLM3 = None
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = []

for ai_response in st.session_state.ai_response:
    with st.chat_message(ai_response["role"], avatar=ai_response.get("avatar")):
        st.markdown(ai_response["content"])

prompt_placeholder = st.chat_message("user", avatar='user')
with st.chat_message("robot", avatar="assistant"):
    message_placeholder_chatglm3 = st.empty()

if prompt:
    prompt_placeholder.markdown(prompt)
    st.session_state.ai_response.append({"role": "user", "content": prompt, "avatar": 'user'})
    stop = st.empty()
    stop_button = stop.button('停止', key='break_response')
    chat_response_chatglm3(prompt)
    stop.empty()
button_clear = st.button("清空", on_click=clear_all, key='clear')