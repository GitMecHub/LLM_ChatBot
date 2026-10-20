import streamlit as st
st.session_state.update(st.session_state)
for k, v in st.session_state.items():
    st.session_state[k] = v

from PIL import Image
import os

path = os.path.dirname(__file__)
my_file = path+'/pages/images/mechub_logo.png'
img = Image.open(my_file)

st.set_page_config(
    page_title='MH AIChat',
    layout="wide",
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

import pandas as pd
import plotly.express as px
import time
import random

import json
import urllib.request

import openai
from openai import OpenAI


# Busca na OpenRouter a lista atual de modelos gratuitos (IDs terminados em ":free").
# Assim o app nao quebra quando a OpenRouter troca os modelos gratis.
@st.cache_data(ttl=3600)
def get_free_models():
    try:
        with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=15) as r:
            data = json.load(r)["data"]
        return sorted(m["id"] for m in data if m["id"].endswith(":free"))
    except Exception:
        return []


if 'active_page' not in st.session_state:
    st.session_state.active_page = '1_Prompt'

    st.session_state.st_response = False
    st.session_state.st_maxtokens = 1000
    st.session_state.st_total_tokens_used = 0
    st.session_state.st_message_id_list = []
    st.session_state.st_message_list = []
    st.session_state.st_message_img_list = []

    st.session_state.st_api_key = ""


role = ""

# Pesquisar API Groq e Llama se valem mais à pena

user_msg = st.chat_input("Say something")

with st.expander("Get your free API key first", expanded=True):

    st.link_button("FREE API KEYS", 'https://openrouter.ai/keys')

    free_models = get_free_models()
    if free_models:
        ai_model = st.selectbox("Select LLM (free models)", free_models, key="st_ai_model")
    else:
        ai_model = st.text_input("Model ID (ex: modelo:free)", key="st_ai_model",
                                 help="Veja os modelos gratuitos em https://openrouter.ai/models?max_price=0")

    # Logo do assistente de acordo com a empresa do modelo
    logos = {
        "openai": "ChatGPT_logo.png",
        "deepseek": "DeepSeek_logo.png",
        "meta-llama": "meta_logo.png",
        "microsoft": "ms_logo.png",
    }
    company = (ai_model or "").split("/")[0]
    img_ai = Image.open(path + '/pages/images/' + logos.get(company, "mechub_logo.png"))


    api_key = st.text_input("API Key", type="password", key='st_api_key')

    data_limits = {
        "Metric": [
            "Requests per minute",
            "Requests per day",
            "Requests per day (after buying $10 in credits once)",
        ],
        "Value": [20, 50, 1000]
    }

    df_limits = pd.DataFrame(data_limits)
    st.subheader("API Usage Limits (Free Account)",anchor=False)
    st.dataframe(df_limits, hide_index=True)

with st.expander("Options"):
    max_tokens = st.number_input("Max Tokens", format='%i', step = 10, key='st_maxtokens',help='A common estimate is that 1 token corresponds to an average of about 4 characters in English')


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=str(api_key),
    #api_key=
)

if st.session_state['st_message_id_list'] != []:
    for i in range(len(st.session_state['st_message_id_list'])):
        message_user = st.chat_message(st.session_state['st_message_id_list'][i],
                                       avatar=st.session_state['st_message_img_list'][i]) if \
        st.session_state['st_message_id_list'][i] == 'assistant' else st.chat_message(
            st.session_state['st_message_id_list'][i])
        message_user.write(st.session_state['st_message_list'][i])

if user_msg:
    try:
        st.session_state.st_maxtokens = max_tokens
        st.session_state.st_ai_model = ai_model
        st.session_state.st_api_key = str(api_key)

    except:
        pass

    message_user = st.chat_message("user")
    message_ai = st.chat_message("assistant", avatar=img_ai)

    message_user.write(user_msg)

    try:
      with st.spinner("Wait for it..."):

          response = client.chat.completions.create(
              model=ai_model,
              messages=[
                  {"role": "system", "content": role},
                        {"role": "user", "content": user_msg}],
              max_tokens=max_tokens,
              temperature=1,
          )

          message_ai.write(response.choices[0].message.content)

          st.session_state.st_message_id_list = st.session_state['st_message_id_list'] + ["user", "assistant"]
          st.session_state.st_message_list = st.session_state['st_message_list'] + [user_msg, response.choices[0].message.content]
          st.session_state.st_message_img_list = st.session_state['st_message_img_list'] + [img_ai, img_ai]

          with st.expander("Used Tokens"):
              # Attempt to convert the response to a dictionary
              response_dict = response.to_dict() if hasattr(response, "to_dict") else response

              usage = response_dict.get("usage")
              if usage:
                  prompt_tokens = usage.get("prompt_tokens", "N/A")
                  completion_tokens = usage.get("completion_tokens", "N/A")
                  total_tokens = usage.get("total_tokens", "N/A")

                  st.write("Prompt tokens:", prompt_tokens)
                  st.write("Completion tokens:", completion_tokens)
                  st.write("Total tokens:", total_tokens)

                  try:
                    st.session_state.st_total_tokens_used = total_tokens + st.session_state['st_total_tokens_used']

                    st.write("Total tokens used in this section:", st.session_state['st_total_tokens_used'])
                  except:
                    pass

              else:
                  st.write("Token usage details are not available in this response.")

    except Exception as e:
        message_ai.write(e)
