import streamlit as st
import json
import requests as r
import numpy as np
import pandas as pd
import plotly.express as px

#COVID API
#De covid API van api-ninjas.com geeft de COVID cijfers per dag aan.
#De API is openbaar en gratis maar er is wel een Key vereist. Deze key heb ik in de code gezet zodat iedereen het kan runnen.
#Het land van interesse kan worden aangepaste door de parameter ?country=Land aan te passen. Hier hebben we hem op Netherlands gezet.
#De API response is een lijst van dictionaries, elke met een regio van het land. In dit geval betekent het aparte cijfers voor
#de caribische gemeenten van het koninkrijk. Deze zijn zodanig klein dat ze verwaarloosbaar zijn.
apiKey = 'BT2KC0xm+UHgWAr5kw889A==UlFfvOOZFfy9BkEp'
baseUrl = 'https://api.api-ninjas.com/v1/covid19?country=Netherlands'
#GET request
response = r.get(baseUrl, headers = { 'X-Api-Key' : apiKey}) 
#Selecteer met index [-1] de laatste dictionary in de lijst, dit zijn de cijfers voor heel Nederland, zonder caribische gemeenten
data = json.loads(response.text)[-1]
#Laadt de data in een panda's dataframe.
df_covid = pd.DataFrame(data) #DEZE VEREIST NOG AANPASSING




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

df_2024 = pd.read_csv('intensiteit2024.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie', 'gem_snelheid'])
df_2024['stadsdeel'] = df_2024['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2024_grouped = df_2024.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2024['start_meetperiode'] = pd.to_datetime(df_2024['start_meetperiode'])
df_2024['1W_bin'] = df_2024['start_meetperiode'].dt.to_period('W').dt.start_time

fig_2024 = px.bar(df_2024, 
             x='1W_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2024 (per week)", 
             labels={'1W_bin': 'Tijdstip (per week)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
#fig_2024.show()

#df_2024_pivot = df_2024_grouped.pivot(index='start_meetperiode', columns='stadsdeel', 
                           # values=['gem_intensiteit', 'gem_snelheid'])

#Ma xx-09-2023 - Zo xx-09-2023
df_2023 = pd.read_csv('intensiteit2023.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie', 'gem_snelheid'])
df_2023['stadsdeel'] = df_2023['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2023_grouped = df_2023.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2023['start_meetperiode'] = pd.to_datetime(df_2024['start_meetperiode'])
df_2023['1W_bin'] = df_2023['start_meetperiode'].dt.to_period('W').dt.start_time

fig_2023 = px.bar(df_2023, 
             x='1W_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2023 (per week)", 
             labels={'1W_bin': 'Tijdstip (per week)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
#fig_2023.show()

#Ma xx-09-2022 - Zo xx-09-2022
df_2022 = pd.read_csv('intensiteit2022.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie', 'gem_snelheid'])
df_2022['stadsdeel'] = df_2022['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2024_grouped = df_2022.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2022['start_meetperiode'] = pd.to_datetime(df_2022['start_meetperiode'])
df_2022['1W_bin'] = df_2022['start_meetperiode'].dt.to_period('W').dt.start_time

fig_2022 = px.bar(df_2022, 
             x='1W_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2022 (per week)", 
             labels={'1W_bin': 'Tijdstip (per week)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
#fig_2022.show()

#Ma xx-09-2021 - Zo xx-09-2021 
df_2021 = pd.read_csv('intensiteit2024.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie', 'gem_snelheid'])
df_2021['stadsdeel'] = df_2021['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2021_grouped = df_2021.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2021['start_meetperiode'] = pd.to_datetime(df_2021['start_meetperiode'])
df_2021['1W_bin'] = df_2021['start_meetperiode'].dt.to_period('W').dt.start_time

fig_2021 = px.bar(df_2021, 
             x='1W_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2021 (per week)", 
             labels={'1W_bin': 'Tijdstip (per week)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
#fig_2021.show()

#Ma xx-09-2020 - Zo xx-09-2020
df_2020 = pd.read_csv('intensiteit2020.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie', 'gem_snelheid'])
df_2020['stadsdeel'] = df_2020['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2020_grouped = df_2020.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2020['start_meetperiode'] = pd.to_datetime(df_2020['start_meetperiode'])
df_2020['1W_bin'] = df_2020['start_meetperiode'].dt.to_period('W').dt.start_time

fig_2020 = px.bar(df_2020, 
             x='1W_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2020 (per week)", 
             labels={'1W_bin': 'Tijdstip (per week)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
#fig_2020.show()

#Ma xx-09-2019 - Zo xx-09-2019
df_2019 = pd.read_csv('intensiteit2019.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie', 'gem_snelheid'])
df_2019['stadsdeel'] = df_2019['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2019_grouped = df_2019.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2019['start_meetperiode'] = pd.to_datetime(df_2019['start_meetperiode'])
df_2019['1W_bin'] = df_2019['start_meetperiode'].dt.to_period('W').dt.start_time

fig_2019 = px.bar(df_2019, 
             x='1W_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2019 (per week)", 
             labels={'1W_bin': 'Tijdstip (per week)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
#fig_2019.show()

#print(df_2024.head(500))
#Bewerking voor join

#Streamlit app 
st.title("Verkeersintensiteit tijdens COVID")
st.markdown("_visualisatie_")

figures = {"2019":fig_2019, "2020":fig_2020, "2021":fig_2021, "2022":fig_2022, "2023":fig_2023, "2024":fig_2024}
option = st.selectbox("Selecteer een figuur om te weergeven", list(figures.keys()))
st.plotly_chart(figures[option])

