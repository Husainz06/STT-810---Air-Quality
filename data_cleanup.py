import pandas as pd

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

# Merge datasets 
merged_data = pd.merge(co_data_columns, ozone_data_columns,  on=['Date', 'Site ID','Local Site Name'],suffixes=('', '_ozone'))
merged_data = pd.merge(merged_data, no2_data_columns,  on=['Date', 'Site ID','Local Site Name'],suffixes=('', '_no2'))
#merged_data = pd.merge(merged_data, pb_data_columns,  on=['Date', 'Site ID','Local Site Name'],suffixes=('', '_pb'))
#merged_data = pd.merge(merged_data, pm10_data_columns,  on=['Date', 'Site ID','Local Site Name'], suffixes=('', '_pm10'))
merged_data = pd.merge(merged_data, pm25_data_columns,  on=['Date', 'Site ID','Local Site Name'], suffixes=('', '_pm2.5'))
#merged_data = pd.merge(merged_data, so2_data_columns,  on=['Date', 'Site ID','Local Site Name'], suffixes=('', '_so2'))

# Check generated dataset
print('data:',merged_data.info())

# Export as csv
merged_data.to_csv('pollution_data_2023.csv', index=False)

# Display data.head()
print(merged_data.head())
