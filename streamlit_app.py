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

########################################################
# VERKEERSINTENSITEIT DATA LADEN EN FEATURES TOEVOEGEN #
########################################################

@st.cache_data
def load_daily_data():

    df = pd.read_csv('intensiteit_daily_average.csv')

    return df

df_daily = load_daily_data()

@st.cache_data
def load_weekly_data(year):
    df = pd.read_csv(f'intensiteit{year}_weekly.csv')
    return df

# Cache individual DataFrames
df19 = load_weekly_data(2019)
df20 = load_weekly_data(2020)
df21 = load_weekly_data(2021)
df22 = load_weekly_data(2022)
df23 = load_weekly_data(2023)
df24 = load_weekly_data(2024)

###################################
# INTRODUCTIE EN COVID PLOT #######
###################################


###################################
# PLOTS VAN THOMAS MET UITLEG #####
###################################

data = {
    2019 : df19,
    2020 : df20,
    2021 : df21,
    2022 : df22,
    2023 : df23,
    2024 : df24
}

st.write('Uitleg')

year = st.selectbox("Selecteer een jaar", range(2019,2025))


weekFig = px.bar(data[year], 
             x='week', 
             y='gem_intensiteit',
             title=f"Intensiteit verkeerstromen in {year} (per week)", 
             labels={'week': 'Tijdstip (per week)', 'gem_intensiteit': 'Aantal'}, 
             color_discrete_sequence=['coral'])

# Customize the layout
weekFig.update_layout(xaxis_title='Tijdstip (per week)',
                  yaxis_title='Aantal',
                  hovermode='x unified')

st.plotly_chart(weekFig, use_container_width=True)

###################################
# PLOT VAN WEEKDAG PER JAAR #######
###################################

#Dagelijkse data laden
@st.cache_data
def load_daily_data():

    df = pd.read_csv('intensiteit_daily_average.csv')

    return df

df_daily = load_daily_data()

#Dropdown box maken en filteren op dag
st.write('''Wat was het effect van de COVID-19 pandemie op de verdeling van verkeersintensiteit binnen een dag?
          Daarvoor kijken we naar onderstaande grafiek. Te zien is de berekende gemiddelde verkeersintensiteit per weekdag per jaar.
         Wat op valt is dat de oude vetrouwde spitsuren niet zijn opgeschoven of uitgespreid, 
         wat het geval zou zijn als er een stijging was in het aannemen van flexibele werktijden. 
         Wel is te zien dat over het algemeen de verkeerintensiteit sterk daalde na de start van de COVID-19 pandemie. 
         Kijkende naar de lijnen van 2023 en 2024, blijkt ook dat deze daling in verkeersintensiteit nog niet genihileerd is.
         Mogelijk door het aanhouden van de thuiswerkcultuur.''')

weekday = st.selectbox('Selecteer een dag', df_daily['dag'].unique())

dailyData = df_daily[df_daily['dag'] == weekday]

#Plot
dayFig = px.line(dailyData, x='tijd', y='gem_intensiteit', color='jaar',
              title=f'Intensiteit verkeersstromen op {weekday} - Vergelijking 2019-2024',
              labels={'tijd': 'Time', 'gem_intensiteit': 'Gemiddelde Intensiteit ()', 'year': 'Year'})

dayFig.update_xaxes(rangeslider_visible=True)
dayFig.update_layout(xaxis_title='Time of Day', yaxis_title='Average Intensity', hovermode='x')

st.plotly_chart(dayFig, use_container_width=True)


###################################
# CONCLUSIE? ######################
###################################