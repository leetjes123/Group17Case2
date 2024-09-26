import streamlit as st
import json
import requests as r
import numpy as np
import pandas as pd
import plotly.express as px

#########################
# API COVID DATA ########
#########################

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
df_grouped = pd.read_csv('intensiteit_daily_average.csv')

data = {
    2019: df_grouped[df_grouped['jaar'] == 2019],
    2020: df_grouped[df_grouped['jaar'] == 2020],
    2021: df_grouped[df_grouped['jaar'] == 2021],
    2022: df_grouped[df_grouped['jaar'] == 2022],
    2023: df_grouped[df_grouped['jaar'] == 2023],
    2024: df_grouped[df_grouped['jaar'] == 2024]
}

st.write('Uitleg')

year = st.selectbox("Selecteer een jaar", range(2019,2025))
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


weekFig = px.bar(data[year], 
             x='dag', 
             y='gem_intensiteit',
             title=f"Intensiteit verkeerstromen in {year} (per week)", 
             labels={'dag': 'Dag van de week', 'gem_intensiteit': 'Aantal'}, 
             color='week',
             category_orders={'dag': day_order},
             color_discrete_sequence=['coral'])

# Customize the layout
weekFig.update_layout(xaxis_title='Dag van de week',
                  yaxis_title='Aantal',
                  hovermode='x unified')

st.plotly_chart(weekFig, use_container_width=True)

#Data naast elkaar per jaar 
all_years_data = df_grouped.groupby(['dag', 'jaar'])['gem_intensiteit'].mean().reset_index()

all_years_fig = px.bar(all_years_data, 
                        x='dag', 
                        y='gem_intensiteit',
                        color='jaar',
                        title="Gemiddelde intensiteit per dag over alle jaren",
                        labels={'dag': 'Dag van de Week', 'gem_intensiteit': 'Aantal Gemiddelde Intensiteit'},
                        category_orders={'dag': day_order})
                

all_years_fig.update_layout(barmode='group',
                            xaxis_title='Dag van de Week',
                             yaxis_title='Gemiddelde Intensiteit',
                             hovermode='x unified')
all_years_fig.update_xaxes(type='category')


st.plotly_chart(all_years_fig, use_container_width=True)

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