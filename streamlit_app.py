import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# get the dataframes from the folder
MUNICIPAL = pd.read_csv(".\dataframes\MUNICIPAL.csv")
# get the list of countries
countries = MUNICIPAL["Country"].unique()

# add a title to the page
st.title("Waste emission, GDP, HDI and other metrics")


st.sidebar.title("Menu")
# less margin on the left
# st.markdown("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)

# same but with dropdown
page = st.sidebar.selectbox("Go to", ["Waste Emission", "GDP", "HDI", "Population Density", "Extreme temperatures", "Analysis"])

# In the home page, we will have a title and a subtitle
if page == "Waste Emission":
    
    # drop down for category of waste
    st.subheader("Waste emission by category")


    df_list = ["MUNICIPAL",
            "HOUSEHOLD",
            "RECYCLING",
            "LANDFILL",
            "COMPOST",
            "INCINERATION",
            "INCINERATION_WITH",
            "INCINERATION_WITHOUT",
            "BULKY",
            "MW_CAP",
            "WEEE",
            "RECYCLING_SHARE",
            "LANDF_SHARE",
            "COMPST_SHARE",
            "INC_SHARE",
            "INC_WITH_SHARE",
            "INC_WITHOUT_SHARE",
            ]

    # Same but with string and only first letter capitalized
    df_list_str = ["Municipal",
                "Household",
                "Recycling",
                "Landfill",
                "Compost",
                "Incineration",
                "Incineration with energy recovery",
                "Incineration without energy recovery",
                "Bulky",
                "Municipal waste per capita",
                "WEEE",
                "Recycling share (%)",
                "Landfill share (%)",
                "Compost share (%)",
                "Incineration share (%)",
                "Incineration with energy recovery share (%)",
                "Incineration without energy recovery share (%)"
                ]
    df_definitions= {"Municipal": "Municipal waste is defined as waste collected and treated by or for municipalities. It covers waste from households, including bulky waste, similar waste from commerce and trade, office buildings, institutions and small businesses, as well as yard and garden waste, street sweepings, the contents of litter containers, and market cleansing waste if managed as household waste. The definition excludes waste from municipal sewage networks and treatment, as well as waste from construction and demolition activities.",
                    "Household": "Household waste refers to waste material usually generated in the residential environment. Waste with similar characteristics may be generated in other economic activities and can thus be treated and disposed of together with household waste.",
                    "Recycling": "Recycling waste is waste that has been collected, processed, and reused. It can include materials like paper, metal, and plastic that have been recovered from the waste stream and used to make new products.",
                    "Landfill": "Landfill waste is waste that is deposited in a landfill, which is a site where waste is placed and then covered with soil. Landfills are used to dispose of solid waste, including household trash, construction and demolition debris, and industrial waste.",
                    "Compost": "Compost waste is organic waste that has been decomposed and recycled as a fertilizer and soil conditioner. Compost is made by breaking down organic waste, such as food scraps and yard waste, through the process of decomposition.",
                    "Incineration": "Incineration waste is waste that has been burned in order to reduce its volume and reduce the risk of disease. Incineration can be used to dispose of solid, liquid, or gaseous waste.",
                    "Incineration with energy recovery": "Incineration with energy recovery waste is waste that has been burned in order to generate electricity or steam. The heat generated during the burning process is used to power a generator or produce steam, which can be used to heat buildings or power industrial processes.",
                    "Incineration without energy recovery": "Incineration without energy recovery is waste that has been burned in order to reduce its volume and reduce the risk of disease. Incineration can be used to dispose of solid, liquid, or gaseous waste.",
                    "Bulky": "Bulky waste is waste that is too large or heavy to be easily handled or transported. It can include items like furniture, appliances, and construction debris.",
                    "Municipal waste per capita": "Municipal waste per capita is a measure of the amount of municipal waste generated per person in a community. It is used as a way to compare the waste generation of different communities and to track trends over time.",
                    "WEEE": "WEEE (Waste Electrical and Electronic Equipment) is waste generated by electronic devices, such as computers, cellphones, and TVs. It can contain hazardous materials and is often difficult to recycle.",
                    "Recycling share (%)": "Recycling share is the percentage of waste that has been collected, processed, and reused. It can include materials like paper, metal, and plastic that have been recovered from the waste stream and used to make new products.",
                    "Incineration with energy recovery share (%)": "Incineration with energy recovery share is the percentage of waste that has been burned in order to generate electricity or steam. The heat generated during the burning process is used to power a generator or produce steam, which can be used to heat buildings or power industrial processes.",
                    "Landfill share (%)": "Landfill share is the percentage of waste that is deposited in a landfill, which is a site where waste is placed and then covered with soil. Landfills are used to dispose of solid waste, including household trash, construction and demolition debris, and industrial waste.",
                    "Compost share (%)": "Compost share is the percentage of organic waste that has been decomposed and recycled as a fertilizer and soil conditioner. Compost is made by breaking down organic waste, such as food scraps and yard waste, through the process of decomposition.",
                    "Incineration without energy recovery share (%)": "Incineration without energy recovery share is the percentage of waste that has been burned in order to reduce its volume and reduce the risk of disease. Incineration can be used to dispose of solid, liquid, or gaseous waste.",
                    "Incineration share (%)": "Incineration share is the percentage of waste that has been burned in order to reduce its volume and reduce the risk of disease. Incineration can be used to dispose of solid, liquid, or gaseous waste.",
                    }
    
    # dropdown for the dataframe to display
    category = st.selectbox("Category", df_list_str)
    # write the appropriate definition

    st.markdown("<span style='color:lightblue'>%s</span>" % df_definitions[category], unsafe_allow_html=True)

    # load the appropriate dataframe
    data = pd.read_csv(".\dataframes\%s.csv" % df_list[df_list_str.index(category)])
    # slider for the year
    year = st.slider("Year", 1990, 2020, 2020)
    # bar plot for the selected year
    data = data[data["Year"] == year]
    # remove countries starting with "OECD"
    data = data[~data["Country"].str.startswith("OECD")]

    data = data[data["Year"] == year].groupby("Country")[
        "Value"].mean()
        
    fig = px.bar(data, orientation="h", text_auto=True)
    # sort the values in descending order
    fig.update_layout(yaxis_categoryorder="total ascending")
    fig.update_xaxes(tickformat=".0f")
    # bigger plot size
    fig.update_layout(height=1000)
    # add values on top of the bars
    fig.update_traces(textposition='outside')



    # no legend
    fig.update_layout(showlegend=False)
    # restrict max length of bar to not overlap with the text
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    # match color of the streamlit slider for the bars
    
    # fit the plot to the screen
    st.plotly_chart(fig)


    # subtitle for the line plot
    st.subheader("Waste emission evolution")

    # dropdown for the country
    data = pd.read_csv(".\dataframes\%s.csv" % df_list[df_list_str.index(category)])
    data = data[~data["Country"].str.startswith("OECD")]
    country = st.selectbox("Country", data["Country"].unique())
    # line plot of the evolution of the municipal waste emission for the selected country
    
    data = data[data["Country"] == country]
    fig = px.line(data, x="Year", y="Value", labels={
                  "value": "Municipal waste emission/Year (Thousands of tonnes)"})
    fig.update_layout(height=500)

    st.plotly_chart(fig)


elif page == "GDP":

    # small title 
    st.subheader("GDP per capita")

    # Little paragraph explaining what GDP per capita is
    st.markdown("<span style='color:lightblue'>GDP per capita is a measure of the average income of a country's citizens. It is calculated by dividing the country's GDP by its population. It is used as a way to compare the economic development of different countries and to track trends over time.</span>", unsafe_allow_html=True)
    # what is GDP
    st.markdown("<span style='color:lightblue'>GDP is the total value of goods and services produced by a country in a year. It is used as a way to compare the economic development of different countries and to track trends over time.</span>", unsafe_allow_html=True)
    ds = pd.read_csv("dataframes/GDP_pcapita.csv", index_col=0)

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
    ds = pd.read_csv("dataframes/GDP_pcapita.csv", index_col=0)
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
    
    
    

   
elif page == "HDI":

    # small title 
    st.subheader("Human Development Index")
    # Little paragraph to explain what the HDI is
    st.markdown("<span style='color:lightblue'>The Human Development Index (HDI) is a composite statistic of life expectancy, education, and per capita income indicators, which are used to rank countries into four tiers of human development. A country scores higher HDI when the lifespan is higher, the education level is higher, and the GDP per capita is higher.</span>", unsafe_allow_html=True)

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


elif page == "Population Density":
    
        # Little paragraph to explain what the Population Density is
        st.markdown("<span style='color:lightblue'>Population density is the number of people living in a given area. It is used to compare the population of different countries and to track trends over time.</span>", unsafe_allow_html=True)
    
        ds = pd.read_csv("./dataframes/population-density.csv", index_col=0)
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
        ds = pd.read_csv("./dataframes/population-density.csv", index_col=0)
    
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


elif page == "Extreme temperatures":

    # Small title for the page
    st.subheader("Extreme temperatures")
    # Little paragraph to explain what the Extreme temperatures is
    st.markdown("<span style='color:lightblue'>Extreme temperatures are the highest and lowest temperatures recorded in a given area. It is used to compare the extreme temperatures of different countries and to track trends over time.</span>", unsafe_allow_html=True)


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

    st.markdown("<span style='color:lightblue'>%s</span>" % df_definitions[mesurement], unsafe_allow_html=True)

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

elif page == "Analysis":
    st.subheader("Analysis")
    st.subheader("Is GDP related to the amount of waste produced?")

    data_MW_CAP = pd.read_csv(".\dataframes\MW_CAP.csv" )
    data_GDP = pd.read_csv("dataframes/GDP_pcapita.csv", index_col=0)

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

    st.subheader("Is recycling share and landfill share related to the GDP per capita?")

    data_recycling = pd.read_csv("dataframes/RECYCLING_SHARE.csv", index_col=0)
    data_landfill = pd.read_csv("dataframes/LANDF_SHARE.csv", index_col=0)

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
    data_HDI = pd.read_csv("dataframes/HDI.csv", index_col=0)
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

    # Study of the extreme temperature events in relation to waste production
    st.subheader("Extreme temperature events in relation to waste production")

    # slider for the year

    year5 = st.slider("Year   ", 1990, 2019, 2019)

    # Municipal Waste
    data_MW_CAP_3 = data_MW_CAP[data_MW_CAP["Year"] == year5]
    # remove countries starting with "OECD"
    data_MW_CAP_3 = data_MW_CAP_3[~data_MW_CAP_3["Country"].str.startswith("OECD")]

    # Population exposure to heat stress
    data_heat = pd.read_csv("dataframes/UTCI_POP_IND.csv", index_col=0)
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


    data_icing = pd.read_csv("dataframes/ID_POP_IND.csv", index_col=0)

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

    data_pop_den = pd.read_csv("./dataframes/population-density.csv", index_col=0)
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




    



