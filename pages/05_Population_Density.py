import streamlit as st
import pandas as pd
import plotly.express as px


# get the dataframes from the folder
MUNICIPAL = pd.read_csv(".\dataframes\MUNICIPAL.csv")
# get the list of countries
countries = MUNICIPAL["Country"].unique()


# Small title for the page
st.subheader("Extreme temperatures")
# Little paragraph to explain what the Extreme temperatures is
st.info("Extreme temperatures are the highest and lowest temperatures recorded in a given area. It is used to compare the extreme temperatures of different countries and to track trends over time.")


# drop down for category mesurement
st.subheader("Type of mesurement related to extreme temperatures")

df_list = {'Annual temperature change':'TEMP_C',
    'Mean number of days with above average temperatures':'DA_TEMP_C',
    'Mean number of days with below-average temperatures':'DB_TEMP_C',
    'Population exposure to hot summer days':'HD_POP_IND',
    'Population exposure to tropical nights':'TN_POP_IND',
    'Population exposure to days identified to be a hot summer day and tropical night':'HD_TN_POP_IND',
    'Mean population exposure to heat stress':'UTCI_POP_IND',
    'Population exposure to icing days':'ID_POP_IND'}

df_definitions = {'Annual temperature change means the average change in temperature over the course of a year.',
                'Mean number of days with above average temperatures',
                'Mean number of days with below-average temperatures',
                'Population exposure to hot summer days',
                'Population exposure to tropical nights',
                'Population exposure to days identified to be a hot summer day and tropical night',
                'Mean population exposure to heat stress',
                'Population exposure to icing days'}

df_definitions = {'Annual temperature change':'Annual temperature change (°C) over the course of a year is the average change in temperature, in degrees Celsius, over the course of a year.',
                'Mean number of days with above average temperatures':'Mean number of days with above average temperatures is the average number of days in a year with temperatures above the average for that location.',
                'Mean number of days with below-average temperatures':'Mean number of days with below-average temperatures is the average number of days in a year with temperatures below the average for that location.',
                'Population exposure to hot summer days':'Population exposure to hot summer days is the percentage of the population that is exposed to hot summer days, which are defined as days with temperatures above a certain threshold.',
                'Population exposure to tropical nights':'Population exposure to tropical nights is the percentage of the population that is exposed to tropical nights, which are defined as nights with temperatures above a certain threshold.',
                'Population exposure to days identified to be a hot summer day and tropical night':'Population exposure to days identified to be a hot summer day and tropical night is the percentage of the population that is exposed to both hot summer days and tropical nights.',
                'Mean population exposure to heat stress':'Mean population exposure to heat stress is the average amount of days per year of heat stress experienced by the population, as measured by the Universal Thermal Climate Index (UTCI). The UTCI is a temperature-humidity index that is used to assess the physiological impact of heat on humans.',
                'Population exposure to icing days':'Population exposure to icing days is the percentage of the population that is exposed to icing days, which are defined as days with temperatures below a certain threshold and high humidity.'}

# dropdown for the mesurement
mesurement = st.selectbox("Mesurement", list(df_list.keys()))

# write the appropriate definition

st.info("%s" % df_definitions[mesurement])

# load the appropriate dataframe
data = pd.read_csv(".\dataframes\%s.csv" % df_list[mesurement])

# slider for the year
year = st.slider("Year", 1990, 2020, 2020)
# keep the data for the selected year
data = data[data["TIME_PERIOD: Time period"] == year]

# keep  REF_AREA: Reference area, DURATION: Duration, HEAT_STRESS: Heat stress thresholds, TIME_PERIOD: Time period, OBS_VALUE
data = data[["REF_AREA: Reference area", "DURATION: Duration", "HEAT_STRESS: Heat stress thresholds", "TIME_PERIOD: Time period", "OBS_VALUE"]]
# rename columns
data.columns = ["Country", "Duration", "Heat stress thresholds", "Year", "Value"]
# split at : and strip the country names
data["Country"] = data["Country"].str.split(":").str[1].str.strip()
# split at : and strip the duration names
data["Duration"] = data["Duration"].str.split(":").str[1].str.strip()
# split at : and strip the heat stress thresholds names
data["Heat stress thresholds"] = data["Heat stress thresholds"].str.split(":").str[1].str.strip()

# keep only countries that are in "countries"
data = data[data["Country"].isin(countries)]
# remove countries that start with "OECD"
data = data[~data["Country"].str.startswith("OECD")]
# group by country and duration and take the mean
if mesurement in ["Population exposure to hot summer days","Population exposure to tropical nights","Population exposure to days identified to be a hot summer day and tropical night","Population exposure to icing days"]:
    data = data.groupby(["Country", "Duration"])[
    "Value"].mean().reset_index()
    # don't plot if the value is 0
    data = data[data["Value"] != 0]
    # bar plot average for each country
    fig = px.bar(data, y="Country", x="Value", barmode="stack",color= "Duration",orientation="h", text_auto=True)

elif mesurement in ["Mean population exposure to heat stress"]:
    data = data.groupby(["Country", "Heat stress thresholds"])[
    "Value"].mean().reset_index()
    # don't plot if the value is 0
    data = data[data["Value"] != 0]
    # bar plot average for each country
    fig = px.bar(data, y="Country", x="Value", barmode="stack",color= "Heat stress thresholds",orientation="h", text_auto=True)

else:
    data = data.groupby(["Country"])[
    "Value"].mean().reset_index()
    # don't plot if the value is 0
    data = data[data["Value"] != 0]
    # bar plot average for each country
    fig = px.bar(data, y="Country", x="Value", barmode="stack",orientation="h", text_auto=True)

fig.update_layout(height=1000)


fig.update_layout(yaxis_categoryorder="total ascending")
st.plotly_chart(fig)