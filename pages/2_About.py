#
import streamlit as st
from streamlit_player import st_player
for k, v in st.session_state.items():
    st.session_state[k] = v

import pandas as pd
from PIL import Image
import os
path = os.path.dirname(__file__)
my_file = path+'/images/mechub_logo.png'
img = Image.open(my_file)

st.set_page_config(
    page_title='MH AIChat',
    page_icon=img
                   )

st.sidebar.image(img)
st.sidebar.markdown("[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@MecHub?sub_confirmation=1) [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GitMecHub)")

hide_menu = '''
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        '''
st.markdown(hide_menu, unsafe_allow_html=True)

st.header("Tutorial: Get your free API key", divider="gray", anchor=False)
st_player("https://youtu.be/N25rt8F0RPc")

st.markdown('''
## About:

This app is an example of how to use free APIs to create a chat platform with different LLMs. Watch the tutorial video
to learn how to obtain a free api key.

https://github.com/marketplace/models

## Limits (Free Account):

https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits

  '''
            )

# Lista de modelos
llms = ["gpt-4o-mini", "Meta-Llama-3.1-8B-Instruct", "Phi-4", "DeepSeek-R1", "gpt-4o"]

# Dados para cada modelo
data = {
    "Metric": [
        "Requests per minute",
        "Requests per day",
        "Tokens per request (in)",
        "Tokens per request (out)",
        "Concurrent requests"
    ]
}

# Valores correspondentes para cada modelo
for model in llms:
    if model in ["gpt-4o-mini", "Meta-Llama-3.1-8B-Instruct", "Phi-4"]:
        values = [15, 150, 8000, 4000, 5]
    elif model == "DeepSeek-R1":
        values = [1, 8, 4000, 4000, 1]
    else:
        values = [10, 50, 8000, 4000, 2]

    data[model] = values

# Criar DataFrame
st.dataframe(pd.DataFrame(data), hide_index=True)
