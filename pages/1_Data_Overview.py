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
st.subheader('Raw Data Sample')
st.write("""Below is a sample of the raw data we acquired form the EPA website which shows CO data.""")
st.write(co_data.head(50))

st.write("""As seen from the dataset above, it only contains the data for one pollutant. For our analysis, we need all pollutants to 
         be included in one dataset.""")

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
st.write("""As seen from the dataset above, it only contains the data for one pollutant. For our analysis, we need all pollutants to 
         be included in one dataset. For the purposes of this project, we do not really need all columns of the dataset. 
         For that reason, we selected the columns that we need for our analysis, which are:

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
         heatmaps below.""")

missing_data = combined_data[pollutants].isnull().astype(int)
heatmap = go.Heatmap(
    # Transpose to have pollutants on y-axis for better visualization
    z=missing_data.T.values,  
    x=combined_data['Local Site Name'],
    y=pollutants
)

# Update layout
fig = go.Figure(data=[heatmap])
fig.update_layout(
    title='Missing Data Across Locations',
    xaxis_title='Location',
    yaxis_title='Pollutants',
    height = 800,
    width = 1500
)

st.plotly_chart(fig)


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
    title='Missing Data Across Dates',
    xaxis_title='Date',
    yaxis_title='Pollutants',
    height = 550,
    width = 1500
)

st.plotly_chart(fig)

st.subheader("Interpreting the Missing Data Heatmap")

st.markdown("""
The missing data heatmap provides a visual representation of how much data is missing across different variables in the dataset.
             Missing data is common in real-world datasets, and understanding its distribution is crucial for deciding how to handle 
            it in the analysis. here is what the different parts of it mean:

- **Colors**: The heatmap uses color coding to indicate the presence or absence of data. 
  - The**light or white areas** represent **missing data**, while **darker shades** represent **available data**.
- **Rows**: Each row represents a different variable (i.e., pollutant or feature) in the dataset.
- **Columns**: Each column represents a data point for the corresponding variable. The first heatmap shows which specific location
            has missing values while the second one shows wich dates have missing values.""")

st.subheader("Insights form the Heatmaps")
st.markdown("""
- **Spotting Missing Data Trends**:
   - Large blocks of **light-colored cells** in the heatmap indicate a significant amount of missing data for those particular variables. 
            This suggests that for those pollutants or features, data might not have been recorded for many days or locations.
   - If the missing data is **concentrated around specific periods**, it could indicate an issue with data collection during those times, 
            such as equipment failure or reporting lapses.
  
- **Identifying Patterns**:
   - If the missing data is **random**, it might not significantly impact any  analysis. However, if the missing data follows a 
            **pattern** - like the data we have here -, it could suggest something systematic about how data is being collected 
            or processed.
        - **Patterns in time**: If the data is missing predominantly on certain dates or seasons, it may indicate a seasonal problem 
            with monitoring equipment or data reporting.

- **Insight into the Quality of the Data**:
The heatmap gives us a quick overview of the **completeness** of the dataset. It helps us assess the overall **quality** 
            of the data before moving on to more complex analyses like hypothesis testing, correlations, or predictions.
By interpreting the missing data heatmap, we can gain valuable insights into the data quality and identify any issues 
            with missing values that might affect our analysis. It allows us to decide on the best course of action for 
            dealing with missing data, whether that means imputing values, removing columns, or performing further investigation.
""")

