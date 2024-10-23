import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("Air Quality Analysis")
st.subheader('Data Overview')
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

#select required columns from each dataframe
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

combined_data = pd.merge(pm25_data_columns, ozone_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_ozone'))
combined_data = pd.merge(combined_data, so2_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_so2'))
combined_data = pd.merge(combined_data, no2_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_no2'))
combined_data = pd.merge(combined_data, co_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_co'))
combined_data = pd.merge(combined_data, pm10_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_pm10'))
combined_data = pd.merge(combined_data, pb_data_columns, on=['Date', 'Site ID'], how='left',suffixes=('', '_pb'))
#combined_data.to_csv('pollution_data_2023_all.csv', index=False)
st.subheader("Generated Data Sample")
st.write("Below is some description of what the data looks like.")
st.write(combined_data.head(100))
st.subheader("Basic Statistics")
st.write("Below is some basic statistics of the data.")
st.write(combined_data.describe())
st.subheader("Calculating Averages")
st.write("Below is a table that shows the averages of each of the pollutants per location over the year 2023.")
# These are shown as the name appears in the dataset
pollutants = [
    'Daily Mean PM2.5 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 1-hour NO2 Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM10 Concentration',
    'Daily Mean Pb Concentration'
]

# Group by 'Local Site Name' and calculate the mean for each pollutant
average_pollutants = combined_data.groupby('Local Site Name')[pollutants].mean().reset_index()

# Display the result
st.table(average_pollutants)



st.subheader("Filtering by month")
st.write("While this part needs to be completed to allow selecting a pollutant and a month, we were  able \
         to filter averages per locations per moths.")
co_data = pd.read_csv('2023_CO.csv')

co_data['Date'] = pd.to_datetime(co_data['Date'])

month = co_data[co_data['Date'].dt.month == 2]

month_filtered = month[['Site ID', 'Local Site Name', 'Daily Max 8-hour CO Concentration']]

average = month_filtered.groupby(['Site ID', 'Local Site Name']).mean().reset_index()

st.write(average[['Local Site Name', 'Daily Max 8-hour CO Concentration']])

st.subheader('Missingess')
st.write("As can be seen from the basic statistics above, there's a good amount of missing data due to the \
         following facts: ")

html_content = """
<ul>
    <li>Diiferent reading dates for some pollutants which will have a missing value for any
    pollutant that is not read on that date.</li>
    <li>Diiferent reading intervals for some pollutants</li>
    <li>Diiferent reading locations for some pollutants which will have a missing value for any
    pollutant that is not read on that location.</li>
</ul>
"""
st.markdown(html_content, unsafe_allow_html=True)
st.write("The heatmap below shows a visualization of the missing vsalues.")
missing_data = combined_data[pollutants].isnull().astype(int)  # Convert NaN to 1 and non-NaN to 0
heatmap = go.Heatmap(
    z=missing_data.T.values,  # Transpose to have pollutants on y-axis
    x=combined_data['Date'],
    y=pollutants,
    colorscale='Viridis',
    showscale=True,
    colorbar=dict(title='Missing Data (1 = Missing, 0 = Present)'),
    hoverinfo='x+y+z'
)

# Update layout
fig = go.Figure(data=[heatmap])
fig.update_layout(
    title='Missing Data Across Pollutants',
    xaxis_title='Date',
    yaxis_title='Pollutants',
    yaxis=dict(autorange='reversed')  # Reverse the y-axis for better readability
)

# Show the plot in Streamlit
st.title("Pollutant Missing Data Heatmap")
st.plotly_chart(fig)
