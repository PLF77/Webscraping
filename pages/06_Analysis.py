import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# get the dataframes from the folder
MUNICIPAL = pd.read_csv(r"dataframes/MUNICIPAL.csv")
# get the list of countries
countries = MUNICIPAL["Country"].unique()


st.subheader("Analysis")
st.subheader("Is GDP related to the amount of waste produced?")

data_MW_CAP = pd.read_csv(r"dataframes/MW_CAP.csv" )
data_GDP = pd.read_csv(r"dataframes/GDP_pcapita.csv", index_col=0)

# slider for the year
year = st.slider("Year", 1990, 2020, 2020)

data_MW_CAP_1 = data_MW_CAP[data_MW_CAP["Year"] == year]
# remove countries starting with "OECD"
data_MW_CAP_1 = data_MW_CAP_1[~data_MW_CAP_1["Country"].str.startswith("OECD")]

data_MW_CAP_1 = data_MW_CAP_1[data_MW_CAP_1["Year"] == year].groupby("Country")["Value"].mean()


data_GDP_1 = data_GDP.loc[:,f"{year}"]
# Replace South-korea with "Korea"
data_GDP_1.index = data_GDP_1.index.str.replace("South-korea", "Korea")
# replace Turkey by Türkiye
data_GDP_1.index = data_GDP_1.index.str.replace("Turkey", "Türkiye")
# In country names replace - with space
data_GDP_1.index = data_GDP_1.index.str.replace("-", " ")
# remove "$" and "," and convert to int
data_GDP_1 = data_GDP_1.str.replace("$", "").str.replace(",", "").astype(float)
# In country names capitalize after space
data_GDP_1.index = data_GDP_1.index.str.title()
# keep only countries that are in MW_CAP
data_GDP_1 = data_GDP_1[data_GDP_1.index.isin(data_MW_CAP_1.index)]


# Side by side bar plot for data_MW_CAP and data_GDP
data_MW_CAP_1 = data_MW_CAP_1.sort_values(ascending=True)
data_GDP_1 = data_GDP_1[data_MW_CAP_1.index]
# Side by side bar plot for data_MW_CAP and data_GDP
fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
fig.add_trace(go.Bar(x=data_MW_CAP_1, y=data_MW_CAP_1.index, orientation="h", name="Municipal Waste per Capita"), row=1, col=1)
fig.add_trace(go.Bar(x=data_GDP_1, y=data_GDP_1.index, orientation="h", name="GDP per capita ($)"), row=1, col=2)
fig.update_layout(height=1000)

# display the correlation between GDP and Municipal Waste per Capita
st.metric("Correlation between GDP per capita and Municipal Waste per Capita", round(data_GDP_1.corr(data_MW_CAP_1), 2))

st.plotly_chart(fig)

st.info("From what we can see, there is a significant correlation between GDP per capita and Municipal Waste per Capita. Also, we can notice that the correlation become increasingly strong throughout the years")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# HDI vs Municipal Waste
st.subheader("Relation between HDI and Municipal Waste per capita")
# slider for the year
year4 = st.slider("Year  ", 1990, 2019, 2019)

# Municipal Waste
data_MW_CAP_2 = data_MW_CAP[data_MW_CAP["Year"] == year]
# remove countries starting with "OECD"
data_MW_CAP_2 = data_MW_CAP_2[~data_MW_CAP_2["Country"].str.startswith("OECD")]

data_MW_CAP_2 = data_MW_CAP_2[data_MW_CAP_2["Year"] == year].groupby("Country")["Value"].mean()

# HDI
data_HDI = pd.read_csv(r"dataframes/HDI.csv", index_col=0)
data_HDI_1 = data_HDI.loc[:,f"{year4}"]
# In country names replace - with space
data_HDI_1.index = data_HDI_1.index.str.replace("-", " ")
# In country names capitalize after space
data_HDI_1.index = data_HDI_1.index.str.title()
# keep only countries that are in the data_MW_CAP
data_HDI_1 = data_HDI_1[data_HDI_1.index.isin(data_MW_CAP_2.index)]

# sort bar chart by HDI
data_HDI_1 = data_HDI_1.sort_values(ascending=True)
data_MW_CAP_2 = data_MW_CAP_2[data_HDI_1.index]

# side by side bar chart
fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
fig.add_trace(go.Bar(x=data_HDI_1, y=data_HDI_1.index, orientation="h", name="HDI"), row=1, col=1)
fig.add_trace(go.Bar(x=data_MW_CAP_2, y=data_MW_CAP_2.index, orientation="h", name="Municipal Waste per capita"), row=1, col=2)
fig.update_layout(height=800)


# Display the correlation coefficient 
st.metric("Correlation between HDI and Municipal Waste per capita", round(data_HDI_1.corr(data_MW_CAP_2), 2))
st.plotly_chart(fig)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# Exception with Spain

st.info("There are exceptions like Spain which has seen its its production of waste per capita drop since the 2000s while its HDI continued to increase. Proof that it is possible to have a high HDI and reduce the production of waste")

# Spain HDI evolution vs Municipal Waste per capita evolution
st.subheader("HDI evolution vs Municipal Waste per capita evolution in Spain")

# double line plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=data_HDI.columns, y=data_HDI.loc["Spain",:], name="HDI", yaxis="y1"))
fig.add_trace(go.Scatter(x=data_MW_CAP[data_MW_CAP["Country"] == "Spain"]["Year"], y=data_MW_CAP[data_MW_CAP["Country"] == "Spain"]["Value"], name="Municipal Waste per capita", yaxis="y2"))
fig.update_layout(height=800, yaxis2=dict(overlaying="y", side="right"))
st.plotly_chart(fig)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.subheader("Is recycling share and landfill share related to the GDP per capita?")

data_recycling = pd.read_csv(r"dataframes/RECYCLING_SHARE.csv", index_col=0)
data_landfill = pd.read_csv(r"dataframes/LANDF_SHARE.csv", index_col=0)

# slider for the year
year2 = st.slider("Year ", 1990, 2020, 2020)

# recycling 
data_recycling_1 = data_recycling[data_recycling["Year"] == year2]
# In country names replace - with space
data_recycling_1.index = data_recycling_1.index.str.replace("-", " ")
# In country names capitalize after space
data_recycling_1.index = data_recycling_1.index.str.title()
# remove countries starting with "OECD"
data_recycling_1 = data_recycling_1[~data_recycling_1["Country"].str.startswith("OECD")]

data_recycling_1 = data_recycling_1[data_recycling_1["Year"] == year2].groupby("Country")["Value"].mean()


# Same for landfill
data_landfill_1 = data_landfill[data_landfill["Year"] == year2]
# In country names replace - with space
data_landfill_1.index = data_landfill_1.index.str.replace("-", " ")
# In country names capitalize after space
data_landfill_1.index = data_landfill_1.index.str.title()
# remove countries starting with "OECD"
data_landfill_1 = data_landfill_1[~data_landfill_1["Country"].str.startswith("OECD")]

data_landfill_1 = data_landfill_1[data_landfill_1["Year"] == year2].groupby("Country")["Value"].mean()

data_GDP_2 = data_GDP.loc[:,f"{year2}"]
# Replace South-korea with "Korea"
data_GDP_2.index = data_GDP_2.index.str.replace("South-korea", "Korea")
# replace Turkey by Türkiye
data_GDP_2.index = data_GDP_2.index.str.replace("Turkey", "Türkiye")
# In country names replace - with space
data_GDP_2.index = data_GDP_2.index.str.replace("-", " ")
# remove "$" and "," and convert to int
data_GDP_2 = data_GDP_2.str.replace("$", "").str.replace(",", "").astype(float)
# In country names capitalize after space
data_GDP_2.index = data_GDP_2.index.str.title()


# Keep only countries that are in all 3 dataframes
data_recycling_1 = data_recycling_1[data_recycling_1.index.isin(data_landfill_1.index)]
data_recycling_1 = data_recycling_1[data_recycling_1.index.isin(data_GDP_2.index)]
data_landfill_1 = data_landfill_1[data_landfill_1.index.isin(data_recycling_1.index)]
data_landfill_1 = data_landfill_1[data_landfill_1.index.isin(data_GDP_2.index)]
data_GDP_2 = data_GDP_2[data_GDP_2.index.isin(data_recycling_1.index)]
data_GDP_2 = data_GDP_2[data_GDP_2.index.isin(data_landfill_1.index)]


#  order the dataframes by GDP
data_recycling_1 = data_recycling_1[data_GDP_2.sort_values(ascending=True).index]
data_landfill_1 = data_landfill_1[data_GDP_2.sort_values(ascending=True).index]
data_GDP_2 = data_GDP_2.sort_values(ascending=True)
# Side by side bar plot for recycling and landfill and GDP
fig = make_subplots(rows=1, cols=3, shared_yaxes=True)
fig.add_trace(go.Bar(x=data_GDP_2, y=data_GDP_2.index, orientation="h", name="GDP per capita ($)"), row=1, col=1)
fig.add_trace(go.Bar(x=data_recycling_1, y=data_recycling_1.index, orientation="h", name="Recycling Share"), row=1, col=2)
fig.add_trace(go.Bar(x=data_landfill_1, y=data_landfill_1.index, orientation="h", name="Landfill Share"), row=1, col=3)
fig.update_layout(height=1000)


# display the correlation between GDP and recycling/landfill
col1, col2 = st.columns(2)
with col1:
    st.metric("Correlation between GDP per capita and Recycling Share", round(data_GDP_2.corr(data_recycling_1), 2))
with col2:
    st.metric("Correlation between GDP per capita and Landfill Share", round(data_GDP_2.corr(data_landfill_1), 2))

st.plotly_chart(fig)

st.info("From what we can see, the correlation between the recycling share of produced waste and GDP per capita become weaker throughout the years. However, the correlation between the landfill share of produced waste and GDP per capita is significant and negative throughout the years. That means that the higher the GDP per capita, the lower the landfill share of produced waste and that less developed countries tend to landfill more of their waste.")



# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Study of the extreme temperature events in relation to waste production
st.subheader("Extreme temperature events in relation to waste production")

# slider for the year

year5 = st.slider("Year   ", 1990, 2019, 2019)

# Municipal Waste
data_MW_CAP_3 = data_MW_CAP[data_MW_CAP["Year"] == year5]
# remove countries starting with "OECD"
data_MW_CAP_3 = data_MW_CAP_3[~data_MW_CAP_3["Country"].str.startswith("OECD")]

# Population exposure to heat stress
data_heat = pd.read_csv(r"dataframes/UTCI_POP_IND.csv", index_col=0)
data_heat = data_heat[data_heat["TIME_PERIOD: Time period"] == year]

# keep  REF_AREA: Reference area, DURATION: Duration, HEAT_STRESS: Heat stress thresholds, TIME_PERIOD: Time period, OBS_VALUE
data_heat = data_heat[["REF_AREA: Reference area", "DURATION: Duration", "HEAT_STRESS: Heat stress thresholds", "TIME_PERIOD: Time period", "OBS_VALUE"]]
# rename columns
data_heat.columns = ["Country", "Duration", "Heat stress thresholds", "Year", "Value"]
# split at : and strip the country names
data_heat["Country"] = data_heat["Country"].str.split(":").str[1].str.strip()
# split at : and strip the duration names
data_heat["Duration"] = data_heat["Duration"].str.split(":").str[1].str.strip()
# split at : and strip the heat stress thresholds names
data_heat["Heat stress thresholds"] = data_heat["Heat stress thresholds"].str.split(":").str[1].str.strip()
data_heat = data_heat.groupby(["Country", "Heat stress thresholds"])[
    "Value"].mean().reset_index()
# only keep the countries that are in both dataframes
data_heat = data_heat[data_heat["Country"].isin(data_MW_CAP_3["Country"])]
# sort bar chart by Municipal Waste per capita
data_MW_CAP_3 = data_MW_CAP_3.sort_values(by="Value", ascending=True)
# sort bar chart by Population exposure to heat stress
data_heat = data_heat.sort_values(by="Value", ascending=True)


data_icing = pd.read_csv(r"dataframes/ID_POP_IND.csv", index_col=0)

data_icing_1 = data_icing[data_icing["TIME_PERIOD: Time period"] == year]
# keep  REF_AREA: Reference area, DURATION: Duration, HEAT_STRESS: Heat stress thresholds, TIME_PERIOD: Time period, OBS_VALUE
data_icing_1 = data_icing_1[["REF_AREA: Reference area", "DURATION: Duration", "TIME_PERIOD: Time period", "OBS_VALUE"]]
# rename columns
data_icing_1.columns = ["Country", "Duration","Year", "Value"]
# split at : and strip the country names
data_icing_1["Country"] = data_icing_1["Country"].str.split(":").str[1].str.strip()
# split at : and strip the duration names
data_icing_1["Duration"] = data_icing_1["Duration"].str.split(":").str[1].str.strip()
data_icing_1 = data_icing_1.groupby(["Country", "Duration"])[
    "Value"].mean().reset_index()

# only keep the countries that are in both dataframes
data_icing_1 = data_icing_1[data_icing_1["Country"].isin(data_MW_CAP_3["Country"])]
# sort bar chart by Municipal Waste per capita
data_MW_CAP_3 = data_MW_CAP_3.sort_values(by="Value", ascending=True)



# Side by side bar chart Municipal Waste per capita vs Population exposure to heat stress
st.subheader("Municipal Waste per capita vs Population exposure to heat stress")
fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
fig.add_trace(go.Bar(x=data_MW_CAP_3["Value"], y=data_MW_CAP_3["Country"], orientation="h", name="Municipal Waste per capita"), row=1, col=1)
fig.add_trace(go.Bar(x=data_heat["Value"], y=data_heat["Country"], orientation="h", name="Population exposure to heat stress"), row=1, col=2)
fig.update_layout(height=800)
st.plotly_chart(fig)

st.subheader("Municipal Waste per capita vs Population exposure to heat stress")
fig = make_subplots(rows=1, cols=4, shared_yaxes=True)
fig.add_trace(go.Bar(x=data_MW_CAP_3["Value"], y=data_MW_CAP_3["Country"], orientation="h", name="Municipal Waste per capita"), row=1, col=1)
fig.add_trace(go.Bar(x=data_heat[data_heat["Heat stress thresholds"] == "Strong heat stress (32°C - 38°C)"]["Value"], y=data_heat[data_heat["Heat stress thresholds"] == "Strong heat stress (32°C - 38°C)"]["Country"], orientation="h", name="Strong heat stress (32°C - 38°C)"), row=1, col=2)
fig.add_trace(go.Bar(x=data_heat[data_heat["Heat stress thresholds"] == "Very strong heat stress (38°C - 46°C)"]["Value"], y=data_heat[data_heat["Heat stress thresholds"] == "Very strong heat stress (38°C - 46°C)"]["Country"], orientation="h", name="Very strong heat stress (38°C - 46°C)"), row=1, col=3)
fig.add_trace(go.Bar(x=data_heat[data_heat["Heat stress thresholds"] == "Extreme heat stress (> 46°C)"]["Value"], y=data_heat[data_heat["Heat stress thresholds"] == "Extreme heat stress (> 46°C)"]["Country"], orientation="h", name="Extreme heat stress (> 46°C)"), row=1, col=4)
fig.update_layout(height=800)

st.plotly_chart(fig)

# Same but with stacked bar chart for the Population exposure to icing
st.subheader("Municipal Waste per capita vs Population exposure to icing")
fig = make_subplots(rows=1, cols=5, shared_yaxes=True)
fig.add_trace(go.Bar(x=data_MW_CAP_3["Value"], y=data_MW_CAP_3["Country"], orientation="h", name="Municipal Waste per capita"), row=1, col=1)
fig.add_trace(go.Bar(x=data_icing_1[data_icing_1["Duration"] == "over 8 weeks"]["Value"], y=data_icing_1[data_icing_1["Duration"] == "over 8 weeks"]["Country"], orientation="h", name="over 8 weeks"), row=1, col=2)
fig.add_trace(go.Bar(x=data_icing_1[data_icing_1["Duration"] == "from 4 to 6 weeks"]["Value"], y=data_icing_1[data_icing_1["Duration"] == "from 4 to 6 weeks"]["Country"], orientation="h", name="from 4 to 6 weeks"), row=1, col=3)
fig.add_trace(go.Bar(x=data_icing_1[data_icing_1["Duration"] == "from 2 to 4 weeks"]["Value"], y=data_icing_1[data_icing_1["Duration"] == "from 2 to 4 weeks"]["Country"], orientation="h", name="from 2 to 4 weeks"), row=1, col=4)
fig.add_trace(go.Bar(x=data_icing_1[data_icing_1["Duration"] == "less than 2 week"]["Value"], y=data_icing_1[data_icing_1["Duration"] == "less than 2 week"]["Country"], orientation="h", name="less than 2 week"), row=1, col=5)
fig.update_layout(height=800)
st.plotly_chart(fig)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Population density vs Waste production
st.subheader("Population density vs Waste production")

#  slider for the year
year6 = st.slider("Year     ", 1990, 2020, 2020)

data_pop_den = pd.read_csv(r"dataframes/population-density.csv", index_col=0)
data_pop_den = data_pop_den[data_pop_den["Year"] == year6]
data_pop_den = data_pop_den["Population density"]

data_MW_CAP_5 = data_MW_CAP[data_MW_CAP["Year"] == year6]
data_MW_CAP_5 = data_MW_CAP_5[~data_MW_CAP_5["Country"].str.startswith("OECD")]
data_MW_CAP_5 = data_MW_CAP_5.groupby("Country")["Value"].mean()

# keep only the countries that are in both dataframes
data_MW_CAP_5 = data_MW_CAP_5[data_MW_CAP_5.index.isin(data_pop_den.index)]
data_pop_den = data_pop_den[data_pop_den.index.isin(data_MW_CAP_5.index)]

# order by data_MW_CAP_4
data_MW_CAP_5 = data_MW_CAP_5.sort_values(ascending=True)

# Side by side bar chart Municipal Waste per capita vs Population density
st.subheader("Municipal Waste per capita vs Population density")
fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
fig.add_trace(go.Bar(x=data_MW_CAP_5, y=data_MW_CAP_5.index, orientation="h", name="Municipal Waste per capita"), row=1, col=1)
fig.add_trace(go.Bar(x=data_pop_den, y=data_pop_den.index, orientation="h", name="Population density"), row=1, col=2)
fig.update_layout(height=800)

# display the correlation coefficient
st.metric("Correlation coefficient", round(data_MW_CAP_5.corr(data_pop_den),2))
st.plotly_chart(fig)

st.info("The correlation coefficient is very low, so there is no significant correlation between the population density and the emited waste.")

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
