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

def load_and_cache_data():

    df_2019 = pd.read_csv('intensiteit2019.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie'])
    df_2020 = pd.read_csv('intensiteit2020.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie'])
    df_2021 = pd.read_csv('intensiteit2021.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie'])
    df_2022 = pd.read_csv('intensiteit2022.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie'])
    df_2023 = pd.read_csv('intensiteit2023.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie'])
    df_2024 = pd.read_csv('intensiteit2024.csv', usecols=['start_meetperiode', 'gem_intensiteit', 'id_meetlocatie'])

    df = pd.concat([df_2019,df_2020,df_2021,df_2022,df_2023,df_2024], ignore_index=True)

    df['start_meetperiode'] = pd.to_datetime(df['start_meetperiode'])
    df['jaar'] = df['start_meetperiode'].dt.year
    df['dag'] = df['start_meetperiode'].dt.day_name()
    df['tijd'] = df['start_meetperiode'].dt.strftime('%H:%M')
    df['1W_bin'] = df['start_meetperiode'].dt.to_period('W').dt.start_time
    

    return df

df = load_and_cache_data()

###################################
# INTRODUCTIE EN COVID PLOT #######
###################################


###################################
# PLOTS VAN THOMAS MET UITLEG #####
###################################

@st.cache_data
def load_data(year):
    df = pd.read_csv(f'intensiteit{year}_weekly.csv')
    df['week_start'] = pd.to_datetime(df['week_start'])
    return df

# Cache individual DataFrames
df19 = load_data(2019)
df20 = load_data(2020)
df21 = load_data(2021)
df22 = load_data(2022)
df23 = load_data(2023)
df24 = load_data(2024)


dict = {
    2019 : df19,
    2020 : df20,
    2021 : df21,
    2022 : df22,
    2023 : df23,
    2024 : df24
}

st.write('Uitleg')
year = st.selectbox("Selecteer een jaar", [2019,2020,2021,2022,2023,2024])
# yearlyData = df[df['jaar'] == year]

weekFig = px.bar(dict[year], 
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
def calculate_daily_average(df):
    return df.groupby(['dag', 'tijd','jaar'])['gem_intensiteit'].mean().reset_index()

df_daily = calculate_daily_average(df)

#Dropdown box maken en filteren op dag
st.write('Uitleg')
weekday = st.selectbox('Selecteer een dag', df_daily['dag'].unique())
dailyData = df_daily[df_daily['dag'] == weekday]

#Plot
dayFig = px.line(dailyData, x='tijd', y='gem_intensiteit', color='jaar',
              title=f'Traffic Intensity on {weekday} - Comparison Across Years',
              labels={'tijd': 'Time', 'gem_intensiteit': 'Average Intensity', 'year': 'Year'})

dayFig.update_layout(xaxis_title='Time of Day', yaxis_title='Average Intensity', hovermode='x')

st.plotly_chart(dayFig, use_container_width=True)


###################################
# CONCLUSIE? ######################
###################################