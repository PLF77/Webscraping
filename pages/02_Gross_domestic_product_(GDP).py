import streamlit as st
import pandas as pd
import plotly.express as px

# get the dataframes from the folder
MUNICIPAL = pd.read_csv(r"dataframes/MUNICIPAL.csv")
# get the list of countries
countries = MUNICIPAL["Country"].unique()


# small title 
st.header("GDP per capita")

# Little paragraph explaining what GDP per capita is
st.info("GDP is the total value of goods and services produced by a country in a year. It is used as a way to compare the economic development of different countries and to track trends over time. GDP per capita is a measure of the average income of a country's citizens. It is calculated by dividing the country's GDP by its population.")

ds = pd.read_csv(r"dataframes/GDP_pcapita.csv", index_col=0)

# Replace South-korea with "Korea"
ds.index = ds.index.str.replace("South-korea", "Korea")
# replace Turkey by Türkiye
ds.index = ds.index.str.replace("Turkey", "Türkiye")
# In country names replace - with space
ds.index = ds.index.str.replace("-", " ")
# In country names capitalize after space
ds.index = ds.index.str.title()
# keep only countries that are in "countries"
ds = ds[ds.index.isin(countries)]

# Slider for the year
year = st.slider("Year", 1990, 2020, 2020)
ds = ds.loc[:,f"{year}"]

# small title for the plot
st.subheader("GDP per capita (USD)")

#  bar chart of the GDP per contry for the selected year
fig = px.bar(ds,x=ds, y=ds.index ,orientation="h", text_auto=True, labels={"x": "GDP per capita (USD)"})
# fit the plot to the screen
fig.update_layout(height=1000)
# sort 
fig.update_layout(yaxis_categoryorder="total ascending")
st.plotly_chart(fig)

#Evolution  of the GDP per capita
st.subheader("GDP per capita evolution")

# dropdown for the country
country = st.selectbox("Country", ds.index)
# line plot of the evolution of the GDP per capita for the selected country
ds = pd.read_csv(r"dataframes/GDP_pcapita.csv", index_col=0)
# Replace South-korea with "Korea"
ds.index = ds.index.str.replace("South-korea", "Korea")
# replace Turkey by Türkiye
ds.index = ds.index.str.replace("Turkey", "Türkiye")
# In country names replace - with space
ds.index = ds.index.str.replace("-", " ")
# In country names capitalize after space
ds.index = ds.index.str.title()
# keep only countries that are in "countries"
ds = ds[ds.index.isin(countries)]
ds = ds.loc[country,:]
fig = px.line(ds, x=ds.index, y=ds, labels={
                "value": "GDP per capita (USD)"})
st.plotly_chart(fig)