import streamlit as st

st.markdown("# Welcome to our App")
st.markdown("This web app contains graphs and analysis about various data about waste emmision, treatment, climate, and other demographic information for different countries.")

st.subheader("Choose from the side menu between the following pages:")
st.markdown("- **Waste Emissions**: Explore data on waste emissions per country.")
st.markdown("- **Gross Domestic Product (GDP)**: Explore data on GDP per country.")
st.markdown("- **Human Development Index (HDI)**: Explore data on HDI per country.")
st.markdown("- **Extreme Temperatures**: Explore data on extreme temperature events.")
st.markdown("- **Population Density**: Explore data on population density per country.")
st.markdown("- **Analysis**: View analysis and insights about the data.")
st.markdown("<p style='text-align: right'>App created by:</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right'>- Pierrick LE FLOCH</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right'>- Kévin LIM</p>", unsafe_allow_html=True)