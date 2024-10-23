import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


# pulling and prepearing data  
# TODO: create a single csv and pull from it

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

#------------------------------------------------------------------------------------------------
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


## ---------------------  visualizations --------------------------
st.subheader("Average pollutants")
st.write("Showing the average pollutants per locations")
average_pollutants.set_index('Local Site Name', inplace=True)

# Transpose the DataFrame for easier plotting
average_pollutants = average_pollutants.transpose()

# Create a bar plot
plt.figure(figsize=(12, 6))
average_pollutants.plot(kind='bar', figsize=(14, 7))

# Add titles and labels
plt.title('Average Pollutant Concentrations per Location', fontsize=16)
plt.xlabel('Pollutants', fontsize=14)
plt.ylabel('Average Concentration', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='Location', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid()

# Show the plot
plt.tight_layout()
#plt.show()
st.pyplot(plt)
st.write("While the above plot show the average pollutants, it is very cluttered. The following interactive \
         plot shows the same information but it is easier to read.")

##----------------  plot 2 -------------------

pollutants = {
    'PM2.5': 'Daily Mean PM2.5 Concentration',
    'Ozone': 'Daily Max 8-hour Ozone Concentration',
    'SO2': 'Daily Max 1-hour SO2 Concentration',
    'NO2': 'Daily Max 1-hour NO2 Concentration',
    'CO': 'Daily Max 8-hour CO Concentration',
    'PM10': 'Daily Mean PM10 Concentration',
    'Pb': 'Daily Mean Pb Concentration'
}
selected_pollutant = st.selectbox("Select a Pollutant", list(pollutants.keys()))
locations = combined_data['Local Site Name'].unique()
selected_location = st.selectbox("Select a Location", locations)
# Filter the data based on selections
filtered_data = combined_data[combined_data['Local Site Name'] == selected_location]

# Create the bar plot
if not filtered_data.empty:
    fig = px.bar(
        filtered_data,
        x='Date',
        y=pollutants[selected_pollutant],
        title=f"{selected_pollutant} Levels at {selected_location}",
        labels={"x": "Date", "y": selected_pollutant}
    )
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected location and pollutant.")


    #----------------------- Second Plot---------------------------


pollutants = {
    'All Pollutants': None,
    'PM2.5': 'Daily Mean PM2.5 Concentration',
    'Ozone': 'Daily Max 8-hour Ozone Concentration',
    'SO2': 'Daily Max 1-hour SO2 Concentration',
    'NO2': 'Daily Max 1-hour NO2 Concentration',
    'CO': 'Daily Max 8-hour CO Concentration',
    'PM10': 'Daily Mean PM10 Concentration',
    'Pb': 'Daily Mean Pb Concentration'
    
}
selected_pollutant2 = st.selectbox("Select a Pollutant (or All)", list(pollutants.keys()), key="pollutant_select")

# Prepare data for plotting
if selected_pollutant2 != "All Pollutants":
    filtered_data = combined_data.groupby('Local Site Name').agg(
        Max_Concentration=pd.NamedAgg(column=pollutants[selected_pollutant2], aggfunc='max')
    ).reset_index()
else:
    # If "All Pollutants" is selected, stack the data for plotting
    melted_data = combined_data.melt(
        id_vars='Local Site Name', 
        value_vars=[v for v in pollutants.values() if v is not None],
        var_name='Pollutant', 
        value_name='Concentration'
    )
    filtered_data = melted_data.groupby(['Local Site Name', 'Pollutant']).agg(Max_Concentration=('Concentration', 'max')).reset_index()

# Create the bar plot
if not filtered_data.empty:
    if selected_pollutant2 == "All Pollutants":
        fig = px.bar(
            filtered_data,
            x='Local Site Name',
            y='Max_Concentration',
            color='Pollutant',
            title="Air Quality Levels by Location",
            labels={"Local Site Name": "Location", "Max_Concentration": "Max Concentration"},
            text='Max_Concentration'
        )
    else:
        fig = px.bar(
            filtered_data,
            x='Local Site Name',
            y='Max_Concentration',
            title=f"{selected_pollutant2} Levels by Location",
            labels={"Local Site Name": "Location", "Max_Concentration": "Max Concentration"},
            text='Max_Concentration'
        )
    
    # Show values on top of the bars
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(height=800) 
    # Show the plot
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected pollutant and locations.")


# --------------------------- Interactive line plot -----------------------------
st.subheader("Pollution Trends Overtime")
st.write("Select a pollutant and a location to show the trend over the year. If the plot is empty \
         then there's probably no data for that pollutant on the selected location.")
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Assuming your DataFrame is named 'combined_data'
combined_data['Date'] = pd.to_datetime(combined_data['Date'])

# List of pollutants
pollutants = [
    'Daily Mean PM2.5 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 1-hour NO2 Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM10 Concentration',
    'Daily Mean Pb Concentration'
]

# Remove NaN values from locations
locations = combined_data['Local Site Name'].dropna().unique().tolist()

# Create a Plotly figure
fig = make_subplots(rows=1, cols=1)

# Initial plot with the first pollutant and location
initial_pollutant = pollutants[0]
initial_location = locations[0]

# Filter the data for the initial plot
filtered_data = combined_data[(combined_data['Local Site Name'] == initial_location) & 
                               (combined_data[initial_pollutant].notna())]

# Add the initial trace
fig.add_trace(go.Scatter(x=filtered_data['Date'], 
                         y=filtered_data[initial_pollutant], 
                         mode='lines', 
                         name=f"{initial_location} - {initial_pollutant}"))

# Update layout
fig.update_layout(
    #title=f"{initial_pollutant} in {initial_location}",
    xaxis_title='Date',
    yaxis_title='Concentration',
    height = 400,
    width = 1300,
    updatemenus=[
        {
            'buttons': [
                {
                    'label': pollutant,
                    'method': 'update',
                    'args': [
                        {'y': [combined_data[combined_data['Local Site Name'] == initial_location][pollutant]]},
                        {'title': f"{pollutant} in {initial_location}"}
                    ]
                } for pollutant in pollutants
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top',
            'active': 0  # Default to the first pollutant
        },
        {
            'buttons': [
                {
                    'label': location,
                    'method': 'update',
                    'args': [
                        {'y': [combined_data[combined_data['Local Site Name'] == location][initial_pollutant]]},
                        {'title': f"{initial_pollutant} in {location}"}
                    ]
                } for location in locations
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.65,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top',
            'active': 0  # Default to the first location
        }
    ]
)

# Show the plot

st.plotly_chart(fig,use_container_width=True)



# -------------------- Heat map -----------------------------
st.subheader("Correlation Between Pollutants")
st.write("Below is a heatmap that shows the correlation between different pollutants.")
import seaborn as sns
pollutants = [
    'Daily Mean PM2.5 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 1-hour NO2 Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM10 Concentration',
    'Daily Mean Pb Concentration'
]

# Create a new DataFrame with only the pollutants
pollutant_data = combined_data[pollutants]

# Calculate the correlation matrix
correlation_matrix = pollutant_data.corr()

# Set up the matplotlib figure
plt.figure(figsize=(10, 8))

# Create a heatmap using Seaborn
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})

# Simplify labels
simplified_labels = [pollutant.split(' ')[-2] for pollutant in pollutants]  # Take just the last two words

# Set new labels
plt.xticks(ticks=range(len(simplified_labels)), labels=simplified_labels, rotation=45)
plt.yticks(ticks=range(len(simplified_labels)), labels=simplified_labels, rotation=0)

# Add titles and labels
plt.title('Correlation Between Pollutants')

# Adjust layout
plt.tight_layout()

# Show the plot in Streamlit
st.pyplot(plt)  # Corrected to pass plt directly

# Clear the figure to avoid overlap in subsequent runs
plt.clf()


# -------------------------- Plotting Michigan map -----------------------
