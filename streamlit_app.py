import streamlit as st
import json
import requests as r
import numpy as np
import pandas as pd
import plotly.express as px


#Luchtmeet API SETUP
stationUrl = 'https://api.luchtmeetnet.nl/open_api/stations'
# LKIUrl = 'https://api.luchtmeetnet.nl/open_api/lki?page=1&order_by=timestamp_measured&order_direction=desc'
concentrationUrl = 'https://api.luchtmeetnet.nl/open_api/concentrations?formula=lki'

#Alle stations in Amsterdam ophalen via API
response = r.get(stationUrl)
data = json.loads(response.text)
df = pd.DataFrame(data['data'])
stations = np.array(df[df['location'].str[:9] == 'Amsterdam'])
print(stations)
# coordinaten = {}
# for number, location in stations:
#     coordinaten[number] = json.loads(r.get(stationUrl+f'/{number}').text)['data']['geometry']['coordinates']

#Meetstation koppelen aan stadsdeel? Of op basis van coordinaten 
latitude = 52.3502761
longitude = 4.9171358
start = '2019-09-16T00:00:00Z'
end = '2019-09-22T23:59:59Z'


response = r.get(concentrationUrl+f'&longitude={longitude}&latitude={latitude}')
print(concentrationUrl+f'&longitude={longitude}&latitude={latitude}&start={start}&end={end}')
print(response.text)
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

