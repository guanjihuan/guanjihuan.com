"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38502
"""

import streamlit as st
st.set_page_config(
    page_title="Chat",
    layout='wide'
)

choose_load_method = 1

if choose_load_method == 0:
    # GPU加载（需要5G显存）
    @st.cache_resource
    def load_bark_model():
        from transformers import AutoProcessor, AutoModel
        processor = AutoProcessor.from_pretrained("suno/bark")
        model = AutoModel.from_pretrained("suno/bark").to("cuda")
        return model, processor
    model, processor = load_bark_model()

elif choose_load_method == 1:
    # GPU加载bark-small模型（需要3G显存）
    @st.cache_resource
    def load_bark_model():
        from transformers import AutoProcessor, AutoModel
        processor = AutoProcessor.from_pretrained("suno/bark-small")
        model = AutoModel.from_pretrained("suno/bark-small").to("cuda")
        return model, processor
    model, processor = load_bark_model()

elif choose_load_method == 2:
    # CPU加载bark模型（需要9G内存，运行速度慢，不推荐）
    @st.cache_resource
    def load_bark_model():
        from transformers import AutoProcessor, AutoModel
        processor = AutoProcessor.from_pretrained("suno/bark")
        model = AutoModel.from_pretrained("suno/bark")
        return model, processor
    model, processor = load_bark_model()

elif choose_load_method == 3:
    # CPU加载bark-small模型（需要5G内存，运行速度慢，不推荐）
    @st.cache_resource
    def load_bark_model():
        from transformers import AutoProcessor, AutoModel
        processor = AutoProcessor.from_pretrained("suno/bark-small")
        model = AutoModel.from_pretrained("suno/bark-small")
        return model, processor
    model, processor = load_bark_model()
    
prompt = st.chat_input("在这里输入您的命令")

prompt_placeholder = st.empty()
with prompt_placeholder.container():
    with st.chat_message("user", avatar='user'):
        pass

if prompt:
    with prompt_placeholder.container():
        with st.chat_message("user", avatar='user'):
            st.write(prompt)
    st.write('正在转换中，请稍后。')

    inputs = processor(
        text=[prompt],
        return_tensors="pt",
    )
    if choose_load_method == 0 or choose_load_method == 1:
        inputs = {key: value.to("cuda") for key, value in inputs.items()}

    speech_values = model.generate(**inputs, do_sample=True)

    import scipy
    sampling_rate = 24_000
    scipy.io.wavfile.write('./a.wav', rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())

    audio_file = open('./a.wav', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')