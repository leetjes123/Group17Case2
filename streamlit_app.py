import streamlit as st
import json
import requests as r
import numpy as np
import pandas as pd
import plotly.express as px


luchtmeetnet_url = 'https://api.luchtmeetnet.nl/open_api/components/NO2'

data = r.get(luchtmeetnet_url)

<<<<<<< Updated upstream
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)


HOI
=======
print(data.text)

#st.title("🎈 My new app")
#st.write(
#    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)
>>>>>>> Stashed changes
