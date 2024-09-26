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
df_covid = pd.DataFrame(data) 
# Splits de 'cases' kolom in twee nieuwe kolommen: 'Total Cases' en 'New Cases'
df_covid['Total Cases'] = df_covid['cases'].apply(lambda x: x['total'])
df_covid['New Cases'] = df_covid['cases'].apply(lambda x: x['new'])

# Verwijder de oorspronkelijke 'cases' kolom als je die niet meer nodig hebt
df_covid = df_covid.drop(columns=['cases'])
# verwijder de kolom 'region'
df_covid = df_covid.drop(columns=["region"])
# Zet de index (datums) om in een aparte kolom genaamd 'Date'
df_covid = df_covid.reset_index()
# Zet de index om in een aparte kolom genaamd 'Date'
df_covid = df_covid.rename(columns={'index': 'Date'})

#Histogram van nieuwe COVID gevallen per week
# Zorg ervoor dat de 'Date' kolom in datetime-formaat staat
df_covid['Date'] = pd.to_datetime(df_covid['Date'])

# Groepeer de data per week en sommeer de nieuwe gevallen per week
df_weekly_new = df_covid.resample('W', on='Date').sum().reset_index()

# Maak een histogram van de nieuwe gevallen per week
fig_hist = px.bar(df_weekly_new, x='Date', y='New Cases',
                  title='COVID-19 gevallen per week in Nederland 2020-2023',
                  labels={'New Cases': 'Nieuwe Gevallen', 'Date': 'Datum'},
                  template='plotly_dark', color_discrete_sequence=['#F23E2E'])

fig_hist.update_layout(
    title={
        'text': "COVID-19 gevallen per week in Nederland 2020-2023",
        'x': 0.5,  # Zorgt ervoor dat de titel in het midden wordt geplaatst
        'xanchor': 'center',  # Anker de titel in het midden
        'yanchor': 'top'  # Houd de titel aan de bovenkant
    }
)

# Update de x-as om deze in maanden te tonen met geroteerde labels
fig_hist.update_xaxes(dtick="M1", tickformat="%b %Y", tickangle=-45)

fig_hist.update_layout(
    autosize=False,  # Schakel autosize uit om zelf de afmetingen te specificeren
    width=1000,  # Breder formaat
    height=500,  # Hoger formaat
    yaxis_range=[0, max(df_weekly_new['New Cases']) * 1.1],  # Y-as iets hoger om ruimte te creëren
    margin=dict(l=38, r=40, t=50, b=80)  # Pas de marges aan voor een betere weergave
)

# Voeg annotaties toe voor moment lockdown
fig_hist.add_vline(x='2020-03-15', line_width=2, line_dash="dash", line_color="yellow")
fig_hist.add_annotation(x='2020-03-15', y=700000, text="Start lockdown", showarrow=True, arrowhead=1)

# Meer annotaties toe voor moment vaccinaties
fig_hist.add_vline(x='2021-01-06', line_width=2, line_dash="dash", line_color="yellow")
fig_hist.add_annotation(x='2021-01-06', y=700000, text="Vaccinatie gestart", showarrow=True, arrowhead=1)

st.plotly_chart(fig_hist)


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

df_2024['start_meetperiode'] = pd.to_datetime(df_2024['start_meetperiode'])
df_2024['4h_bin'] = df_2024['start_meetperiode'].dt.floor('4H')

fig_2024 = px.bar(df_2024, 
             x='4h_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2024 (per 4 uur)", 
             labels={'4h_bin': 'Tijdstip (per 4 uur)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
fig_2024.show()

#df_2024_pivot = df_2024_grouped.pivot(index='start_meetperiode', columns='stadsdeel', 
                           # values=['gem_intensiteit', 'gem_snelheid'])

#Ma xx-09-2023 - Zo xx-09-2023
df_2023 = pd.read_csv('intensiteit2023.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2023['stadsdeel'] = df_2023['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2023_grouped = df_2023.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2023['start_meetperiode'] = pd.to_datetime(df_2023['start_meetperiode'])
df_2023['4h_bin'] = df_2024['start_meetperiode'].dt.floor('4H')

fig_2023 = px.bar(df_2023, 
             x='4h_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2023 (per 4 uur)", 
             labels={'4h_bin': 'Tijdstip (per 4 uur)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
fig_2023.show()

#Ma xx-09-2022 - Zo xx-09-2022
df_2022 = pd.read_csv('intensiteit2022.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2022['stadsdeel'] = df_2022['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2022_grouped = df_2022.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2022['start_meetperiode'] = pd.to_datetime(df_2022['start_meetperiode'])
df_2022['4h_bin'] = df_2024['start_meetperiode'].dt.floor('4H')

fig_2022 = px.bar(df_2022, 
             x='4h_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2022 (per 4 uur)", 
             labels={'4h_bin': 'Tijdstip (per 4 uur)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
fig_2022.show()

#Ma xx-09-2021 - Zo xx-09-2021 
df_2021 = pd.read_csv('intensiteit2021.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2021['stadsdeel'] = df_2021['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2021_grouped = df_2021.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2021['start_meetperiode'] = pd.to_datetime(df_2021['start_meetperiode'])
df_2021['4h_bin'] = df_2024['start_meetperiode'].dt.floor('4H')

fig_2021 = px.bar(df_2021, 
             x='4h_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2021 (per 4 uur)", 
             labels={'4h_bin': 'Tijdstip (per 4 uur)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
fig_2021.show()
#Ma xx-09-2020 - Zo xx-09-2020
df_2020 = pd.read_csv('intensiteit2020.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2020['stadsdeel'] = df_2024['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2020_grouped = df_2020.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2020['start_meetperiode'] = pd.to_datetime(df_2020['start_meetperiode'])
df_2020['4h_bin'] = df_2024['start_meetperiode'].dt.floor('4H')

fig_2020 = px.bar(df_2020, 
             x='4h_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2020 (per 4 uur)", 
             labels={'4h_bin': 'Tijdstip (per 4 uur)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
fig_2020.show()
#Ma xx-09-2019 - Zo xx-09-2019
df_2019 = pd.read_csv('intensiteit2019.csv', usecols=['start_meetperiode','gem_intensiteit', 'id_meetlocatie','gem_snelheid'])
df_2019['stadsdeel'] = df_2019['id_meetlocatie'].map(meetpuntenNaarStadsdeel)
df_2019_grouped = df_2019.groupby(['start_meetperiode', 'stadsdeel']).agg({
    'gem_intensiteit': 'sum',
    'gem_snelheid': 'mean'
}).reset_index()

df_2019['start_meetperiode'] = pd.to_datetime(df_2019['start_meetperiode'])
df_2019['4h_bin'] = df_2024['start_meetperiode'].dt.floor('4H')

fig_2019 = px.bar(df_2019, 
             x='4h_bin', 
             y='gem_intensiteit',
             title="Intensiteit verkeerstromen in 2019 (per 4 uur)", 
             labels={'4h_bin': 'Tijdstip (per 4 uur)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])
fig_2019.show()

#print(df_2024.head(500))
#Bewerking voor join

st.title("Verkeersintensiteit tijdens COVID")
st.markdown("_visualisatie_")

figures = {"2019":fig_2019, "2020":fig_2020, "2021":fig_2021, "2022":fig_2022, "2023":fig_2023, "2024":fig_2024}
option = st.selectbox("Selecteer een figuur om te weergeven", list(figures.keys()))
st.plotly_chart(figures[option])



#st.title("🎈 My new app")
#st.write(
#    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)