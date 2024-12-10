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

st.write("""The dataset above only contains the data for one pollutant, but all pollutants should be included in the data moving forward.""")

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
st.write("""Initial data sets provided only contain information for one pollutant per data frame. For analysis, all pollutants need to 
         be included in one dataset. For the purposes of this project, all columns of the dataset are not nessearly needed; 
         The columns that are need for our analysis are:

- Date
- Site ID
- Local Site Name
- AQS Parameter Description
- Max/Average Concentration (based on the pollutant)
- Units
- Daily AQI Value

Below is a sample of what the full data table looks like after combining all criteria pollutant data.
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
st.write("""The merging of datasets resulted in lots of missing values since not all pollutants are equaly tracked in all geological locations.
         The dataset merged dataset was saved as a file called 'pollution_data_2023_all.csv' on the apps Github page.
         The merged dataset will use for the rest of this pages analysis. 
         Below is a sample of what the combine data set looks like.""")
st.write(combined_data.head(50))

st.subheader("Basic Statistics")
st.write("""The first step of analysis is to calculate basic statistics on the dataset to 
         get an idea for how our data is distributed. Below is a statistical summery of the data.""")
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

st.write("""
The statistical summery above shows diffent variable lengths of data collected accross diffrent polutents. Diffent lengths in variable data are most likely due to:

- Inconsistent recording dates and times for some pollutants, which will have a missing value for any pollutant that is not read on that date.
- Recording for some pollutants is dependent on location, which will have a missing value for any pollutant that is not read at that location.
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
    title='Missing Data Across Location',
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
    title='Missing Data Across Time',
    xaxis_title='Date',
    yaxis_title='Pollutants',
    height = 550,
    width = 1500
)

st.plotly_chart(fig)

st.subheader("Interpreting the Missing Data Heatmap")

st.markdown("""
            Missing data heatmaps provides a visual representation of how much data is missing across different variables in the dataset.
            Understanding the distribution of missing data is crucial for deciding how to handle missingness
            in the analysis. Here is how to interpret the missing data heatmap:

- **Colors**: Color coding is used to indicate the presence or absence of data. 
  - The**light or white areas represented by a 0** represent **missing data**, while **darker colors represented by a 1**, represent **available data**.
- **Rows**: Each row represents a different variable (i.e., pollutant or feature) in the dataset.
- **Columns**: Each column represents a data point for the corresponding variable. """)

st.subheader("Insights form the Heatmaps")
st.markdown("""
- **Spotting Missing Data Trends**:
   - Large blocks of missing data suggest a potential pause in data collection. 
            The reason for a pause in data collection could be related or unrelated to important environmental factors so carful considration of imputation to large blocks of missing data is required.
  
- **Identifying Patterns**:
   - If the missing data seems **random**, it might not significantly impact any  analysis. However, if the missing data follows a 
            **pattern** - like the current data -, it could suggest something systematic about how data is being collected 
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

