import streamlit as st
import pandas as pd
import plotly.express as px


# get the dataframes from the folder
MUNICIPAL = pd.read_csv(".\dataframes\MUNICIPAL.csv")
# get the list of countries
countries = MUNICIPAL["Country"].unique()



# small title 
st.subheader("Human Development Index")
# Little paragraph to explain what the HDI is
st.info("The Human Development Index (HDI) is a composite statistic of life expectancy, education, and per capita income indicators, which are used to rank countries into four tiers of human development. A country scores higher HDI when the lifespan is higher, the education level is higher, and the GDP per capita is higher.")

ds = pd.read_csv("dataframes/HDI.csv", index_col=0)
# In country names replace - with space
ds.index = ds.index.str.replace("-", " ")
# In country names capitalize after space
ds.index = ds.index.str.title()
# keep only countries that are in "countries"
ds = ds[ds.index.isin(countries)]

# Slider for the year
year = st.slider("Year", 1990, 2019, 2019)
ds = ds.loc[:,f"{year}"]

# small title for the plot
st.subheader("HDI (Human Development Index)")

#  bar chart of the HDI per contry for the selected year
fig = px.bar(ds,x=ds, y=ds.index ,orientation="h", text_auto=True, labels={"x": "HDI (Human Development Index)"})
# fit the plot to the screen
fig.update_layout(height=1000)
# sort 
fig.update_layout(yaxis_categoryorder="total ascending")
st.plotly_chart(fig)

#Evolution  of the HDI
st.subheader("HDI evolution")

# dropdown for the country
country = st.selectbox("Country", ds.index)
# line plot of the evolution of the HDI for the selected country
ds = pd.read_csv("dataframes/HDI.csv", index_col=0)

# In country names replace - with space
ds.index = ds.index.str.replace("-", " ")
# In country names capitalize after space
ds.index = ds.index.str.title()
# keep only countries that are in "countries"
ds = ds[ds.index.isin(countries)]
ds = ds.loc[country,:]
fig = px.line(ds, x=ds.index, y=ds, labels={
                "value": "HDI (Human Development Index)"})
st.plotly_chart(fig)