import streamlit as st
import json
import requests as r
import numpy as np
import pandas as pd
import plotly.express as px

url = 'https://api.luchtmeetnet.nl/open_api/lki?page=1&order_by=timestamp_measured&order_direction=desc'

data = r.get(url)
print(data.text)


#st.title("🎈 My new app")
#st.write(
#    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)

