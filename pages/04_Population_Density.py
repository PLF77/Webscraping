import streamlit as st
import pandas as pd
import plotly.express as px


# get the dataframes from the folder
MUNICIPAL = pd.read_csv(r"dataframes/MUNICIPAL.csv")
# get the list of countries
countries = MUNICIPAL["Country"].unique()

# Small title for the page
st.subheader("Population Density")

# Little paragraph to explain what the Population Density is
st.info("Population density is the number of people living in a given area. It is used to compare the population of different countries and to track trends over time.")

ds = pd.read_csv(r"dataframes/population-density.csv", index_col=0)
# In country names replace - with space
ds.index = ds.index.str.replace("-", " ")
# In country names capitalize after space
ds.index = ds.index.str.title()
# keep only countries that are in "countries"
ds = ds[ds.index.isin(countries)]
# pivot the dataframe to have the years as columns
ds = ds.pivot_table(index="Entity", columns="Year", values="Population density")
# Slider for the year
year = st.slider("Year", 1990, 2020, 2020)
ds = ds.loc[:,year]

#  bar chart of the Population Density per contry for the selected year
# fig = px.bar(ds,x=ds, y=ds.index ,orientation="h", text_auto=True, labels={"x": "Population Density (People per km²)"})
fig = px.bar(ds,orientation="h", text_auto=True, labels={"value": "Population Density (People per km²)"})
# fit the plot to the screen
fig.update_layout(height=1000)
# sort 
fig.update_layout(yaxis_categoryorder="total ascending")
st.plotly_chart(fig)

#Evolution  of the Population Density
st.subheader("Population Density evolution")

# dropdown for the country
country = st.selectbox("Country", ds.index)
# line plot of the evolution of the Population Density for the selected country
ds = pd.read_csv(r"dataframes/population-density.csv", index_col=0)

# In country names replace - with space
ds.index = ds.index.str.replace("-", " ")
# In country names capitalize after space
ds.index = ds.index.str.title()
# keep only countries that are in "countries"
ds = ds[ds.index.isin(countries)]
# pivot the dataframe to have the years as columns
ds = ds.pivot_table(index="Entity", columns="Year", values="Population density")
# only keep year between 1990 and 2020
ds = ds.loc[:,1990:2020]
ds = ds.loc[country,:]
fig = px.line(ds, labels={
                "value": "Population Density (People per km²)"})
st.plotly_chart(fig)
