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

# Aviso: o video mostra o GitHub Models, que foi desativado
st.warning('''
**Note:** this video shows **GitHub Models**, which was shut down in July 2026.
The app now uses **OpenRouter**, which also offers free models:

1. Get your free API key at [openrouter.ai/keys](https://openrouter.ai/keys)
2. Paste it in the "API Key" field on the main page
3. Choose one of the free models in the list (their IDs end in `:free`)

To see all free models, go to [openrouter.ai/models](https://openrouter.ai/models)
and type "free" in the search bar, or open
[this filtered list](https://openrouter.ai/models?max_price=0).
''')

# Print da pagina de API Keys da OpenRouter (botao "New Key" no canto superior direito)
st.image(path + '/new_apikey_tutorial.png',
         caption='OpenRouter API Keys page: click "+ New Key" to create your free key')

st_player("https://youtu.be/N25rt8F0RPc")

st.markdown('''
## About:

This app is an example of how to use free APIs to create a chat platform with different LLMs.
Get your free API key here:

https://openrouter.ai/keys

## Limits (Free Account):

Free models (IDs ending in `:free`) cost nothing per token, but have request limits.
The free model list changes often, so if a model stops working, just pick another one.

More details: https://openrouter.ai/docs/api/reference/limits
  '''
            )

# Limites dos modelos gratuitos da OpenRouter (valem para todos os modelos ":free")
data = {
    "Metric": [
        "Requests per minute",
        "Requests per day",
        "Requests per day (after buying $10 in credits once)",
    ],
    "Free models (:free)": [20, 50, 1000],
}

st.dataframe(pd.DataFrame(data), hide_index=True)
