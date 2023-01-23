# Data Analysis Application

This application is designed to scrape, clean, and analyze data related to waste emissions, GDP, HDI, population density, and extreme temperatures. The data is collected from various sources and stored in the `dataframes` directory as CSV files.

## How to Use

1.  The `scrap.ipynb` notebook was used to scrape and clean the data. The cleaned data is stored in various csv files in the `dataframes` directory.
    
2.  To run the web app you have to go in the terminal at the root of the projet and run the command `Streamlit run .\Home.py`
    

## File Structure

-   `Home.py`: the main menu of the application.
-   `scrap.ipynb`: script to scrape and clean the data.
-   `dataframes`: directory containing the cleaned data as CSV files.
-   `pages`: directory containing scripts to analyze the data.

## Note

Make sure that you have all the necessary packages installed before running the application.

You will need the following libraries :
- `pandas`
- `streamlit`
- `plotly`

Install with the folowing commands:
```sh
pip install pandas
pip install streamlit
pip install plotly
```
