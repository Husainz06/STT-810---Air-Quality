import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.utils import resample

st.title('Data Overview')
st.write("Data sets were obtained from epa.gov as seperate files for each of \
         the pollutants. We needed to combine the files to create a single dataset. \
         We faced an issue with inconsistency of the locations and dates. Some datasest \
         have different locations and different datasets. We did a left merge to avoid \
         losing data. Below is an overview of the dataset that we created.")


#Read all csv files
co_data = pd.read_csv('2023_CO.csv')
ozone_data = pd.read_csv('2023_Ozone.csv')
no2_data = pd.read_csv('2023_NO2.csv')
pb_data = pd.read_csv('2023_Pb.csv')
pm10_data = pd.read_csv('2023_PM10.csv')
pm25_data = pd.read_csv('2023_PM25.csv')
so2_data = pd.read_csv('2023_SO2.csv')

# Sample raw data
st.write('Here\'s a sample of the raw data:')
st.write(co_data.head(50))
#selecting columns to merge to the full dataset
#CO
co_data_columns = co_data[['Date', 'Site ID','Local Site Name','Site Latitude','Site Longitude', 
                            'AQS Parameter Description','Daily Max 8-hour CO Concentration','Units','Daily AQI Value']]
#Ozone
ozone_data_columns = ozone_data[['Date', 'Site ID','Local Site Name','AQS Parameter Description',
                                  'Daily Max 8-hour Ozone Concentration','Units','Daily AQI Value']]
#NO2
no2_data_columns = no2_data[['Date', 'Site ID','Local Site Name','AQS Parameter Description','Daily Max 1-hour NO2 Concentration'
                             ,'Units','Daily AQI Value']]
#Pb 
pb_data_columns = pb_data[['Date', 'Site ID','Local Site Name','AQS Parameter Description','Daily Mean Pb Concentration'
                             ,'Units','Daily AQI Value']]
#PM10
pm10_data_columns = pm10_data[['Date', 'Site ID','Local Site Name','AQS Parameter Description','Daily Mean PM10 Concentration'
                             ,'Units','Daily AQI Value']]
#PM2.5
pm25_data_columns = pm25_data[['Date', 'Site ID','Local Site Name','AQS Parameter Description','Daily Mean PM2.5 Concentration'
                             ,'Units','Daily AQI Value']]
#SO2
so2_data_columns = so2_data[['Date', 'Site ID','Local Site Name','AQS Parameter Description','Daily Max 1-hour SO2 Concentration'
                             ,'Units','Daily AQI Value']]

st.title("Preparing the Dataset")
st.write("""
For the purposes of this project, we do not really need all columns of the dataset. For that reason, we selected the columns that we need for our analysis, which are:

- Date
- Site ID
- Local Site Name
- AQS Parameter Description
- Max/Average Concentration (based on the pollutant)
- Units
- Daily AQI Value

Below is a sample of what that looks like.
""")
st.write(co_data_columns.head(50))

combined_data = pd.merge(pm25_data_columns, ozone_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_ozone'))
combined_data = pd.merge(combined_data, so2_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_so2'))
combined_data = pd.merge(combined_data, no2_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_no2'))
combined_data = pd.merge(combined_data, co_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_co'))
combined_data = pd.merge(combined_data, pm10_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_pm10'))
combined_data = pd.merge(combined_data, pb_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_pb'))
# Generating a combined data file

combined_data.to_csv('pollution_data_2023_all.csv', index=False)
st.subheader("Generated Data Sample")
st.write("""To be able to perform our analysis, we need to have all pollutants in one dataset.
         For that reason, we have combined all datasets int one dataset that contains all pollutant
         data after removing the un-needed columns. This resulted in lots of missing values due to the
         nature of the datasets since not all pollutants are tracked in all locations and not all 
         pollutants are tracked within the same periods. The dataset is then saved as a file called 'pollution_data_2023_all.csv'
         which we will use for the rest of our analysis. Below is some description of what the data looks like.""")
st.write(combined_data.head(50))

st.subheader("Basic Statistics")
st.write("""The first step of our analysis is to perform basic statistics analysis on the dataset to 
         see how the data looks like. Below is some basic statistics of the data.""")
st.write(combined_data.describe())

pollutants = [
    'Daily Mean PM2.5 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 1-hour NO2 Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM10 Concentration',
    'Daily Mean Pb Concentration'
]

st.subheader('Missingess')
st.write("As can be seen from the basic statistics above, there's a good amount of missing data due to the \
         following facts: ")

st.write("""
As can be seen from the basic statistics above, there's a good amount of missing data due to the following facts:

- Different reading dates for some pollutants, which will have a missing value for any pollutant that is not read on that date.
- Different reading intervals for some pollutants.
- Different reading locations for some pollutants, which will have a missing value for any pollutant that is not read at that location.
""")
st.write("The heatmap below shows a visualization of the missing vsalues.")


st.subheader("Pollutant Missing Data Heatmap")
st.write("""As we have mentioned, we have lots of missing data in our dataset that we can visualize in the
         heatmap below.""")

missing_data = combined_data[pollutants].isnull().astype(int)
heatmap = go.Heatmap(
    # Transpose to have pollutants on y-axis for better visualization
    z=missing_data.T.values,  
    x=combined_data['Date'],
    y=pollutants
)

# Update layout
fig = go.Figure(data=[heatmap])
fig.update_layout(
    title='Missing Data Across Pollutants',
    xaxis_title='Date',
    yaxis_title='Pollutants',
    height = 600,
    width = 1500
)

st.plotly_chart(fig)
