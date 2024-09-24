import streamlit as st
import json
import requests as r
import numpy as np
import pandas as pd
import plotly.express as px

#COVID API
apiKey = 'BT2KC0xm+UHgWAr5kw889A==UlFfvOOZFfy9BkEp'
baseUrl = 'https://api.api-ninjas.com/v1/covid19?country=Netherlands'

response = r.get(baseUrl, headers = { 'X-Api-Key' : apiKey}) 
data = json.loads(response.text)[-1]
df_covid = pd.DataFrame(data)




#Verkeersintensititeit DataFrames inladen
meetpuntenNaarStadsdeel = {
    'RWS01_MONIBAS_0101hrl0033ra' : 'Noord',
    'RWS01_MONIBAS_0101hrr0032ra' : 'Noord',
    'RWS01_MONIBAS_0101hrl0129ra' : 'Oost',
    'RWS01_MONIBAS_0101hrr0129ra' : 'Oost',
    'RWS01_MONIBAS_0101hrl0175ra' : 'Zuid',
    'RWS01_MONIBAS_0101hrr0175ra' : 'Zuid',
    'RWS01_MONIBAS_0101hrl0239ra' : 'West',
    'RWS01_MONIBAS_0101hrr0239ra' : 'West'
    }
#Ma 16-09-2024 - Zo 22-09-2024

df_2024 = pd.read_csv('intensiteit2024.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2024['stadsdeel'] = df_2024['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2024_grouped = df_2024.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

#df_2024_pivot = df_2024_grouped.pivot(index='start_meetperiode', columns='stadsdeel', 
                           # values=['gem_intensiteit', 'gem_snelheid'])

#Ma xx-09-2023 - Zo xx-09-2023
df_2023 = pd.read_csv('intensiteit2023.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2023['stadsdeel'] = df_2023['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2023_grouped = df_2023.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()
#Ma xx-09-2022 - Zo xx-09-2022
df_2022 = pd.read_csv('intensiteit2022.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2022['stadsdeel'] = df_2022['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2022_grouped = df_2022.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()
#Ma xx-09-2021 - Zo xx-09-2021 
df_2021 = pd.read_csv('intensiteit2021.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2021['stadsdeel'] = df_2021['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2021_grouped = df_2021.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()
#Ma xx-09-2020 - Zo xx-09-2020
df_2020 = pd.read_csv('intensiteit2020.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2020['stadsdeel'] = df_2024['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2020_grouped = df_2020.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()
#Ma xx-09-2019 - Zo xx-09-2019
df_2019 = pd.read_csv('intensiteit2019.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2019['stadsdeel'] = df_2019['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2019_grouped = df_2019.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

#print(df_2024.head(500))
#Bewerking voor join







#st.title("🎈 My new app")
#st.write(
#    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)