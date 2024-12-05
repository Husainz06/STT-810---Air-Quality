import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import bootstrap

st.title("Average Pollutants")
combined_data = pd.read_csv('pollution_data_2023_all.csv')
pollutants = [
    'Daily Mean PM2.5 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 1-hour NO2 Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM10 Concentration',
    'Daily Mean Pb Concentration'
]

st.subheader("Calculating Average Pollutants")
st.write("""One of the important measures in our analysis is calculating the average pollutant per 
         location. This gives some insight about the pollution in those locations. Below is the calculated
         averages of the pollutants per location. As mentioned in the 'Data Overview' page, some locations
         do not keep track of all pollutants and that's why some data is not present in this table.""")
average_pollutants = combined_data.groupby('Local Site Name')[pollutants].mean().reset_index()
st.table(average_pollutants)
st.subheader('2023 Pollutant Averages')
st.write("""The following plot shows the average pollutants in 2023 over the reading location in the state of Michgan. This gives us
         a general idea on what locations are polluted the most and what pollutants are present the most in these locations.
         The following plot is interactive, you can expand it to fill the screen by using the full screen mode, show/hide locations by
         clicking them in the legend, and you can double click a legend item to remove all items and keep that item alone.""")
# Set the index to 'Local Site Name' and transpose the DataFrame
average_pollutants.set_index('Local Site Name', inplace=True)
average_pollutants = average_pollutants.transpose()


fig = px.bar(average_pollutants,
             labels={'value': 'Average Concentration', 'variable': 'Pollutants'},
             title='Average Pollutant Concentrations per Location')

fig.update_layout(
    xaxis_title='Pollutants',
    yaxis_title='Average Concentration - 2023',
    legend_title='Locations',
    barmode='group'
)
st.plotly_chart(fig)

st.subheader("Filtering Averages")
st.write("""To better understand pollution, we need to be able to check the averages during different 
         periods of time. Below we can filter by monthe and location to allow getting more detailed 
         information about the averages.""")

# Plot 1
# dictionary for the plot to use the keys in the menu and values for visualization
pollutants_dictionary = {
    'PM2.5': 'Daily Mean PM2.5 Concentration',
    'Ozone': 'Daily Max 8-hour Ozone Concentration',
    'SO2': 'Daily Max 1-hour SO2 Concentration',
    'NO2': 'Daily Max 1-hour NO2 Concentration',
    'CO': 'Daily Max 8-hour CO Concentration',
    'PM10': 'Daily Mean PM10 Concentration',
    'Pb': 'Daily Mean Pb Concentration'
}
# dropdown menu
selected_pollutant = st.selectbox("Select a Pollutant", list(pollutants_dictionary.keys()))
locations = combined_data['Local Site Name'].unique()
selected_location = st.selectbox("Select a Location", locations)

# using the selection to filter data
filtered_data = combined_data[combined_data['Local Site Name'] == selected_location]

fig = px.bar(filtered_data, x='Date', y=pollutants_dictionary[selected_pollutant],
    title=f"{selected_pollutant} Levels at {selected_location}",labels={"x": "Date", "y": selected_pollutant})
st.plotly_chart(fig)


st.write('Average per location over the year')
# Plot 2:  Year average - location based

selected_pollutant2 = st.selectbox("Select a Pollutant (or All)" 
                , ["All Pollutants"] + list(pollutants_dictionary.keys()), key="pollutant_select")

if selected_pollutant2 != "All Pollutants":
    filtered_data = combined_data.groupby('Local Site Name').agg(
        Max_Concentration=pd.NamedAgg(column=pollutants_dictionary[selected_pollutant2], aggfunc='max')
    ).reset_index()
else:
    # If "All Pollutants" is selected, stack the data for plotting
    melted_data = combined_data.melt(
        id_vars='Local Site Name', 
        value_vars=[v for v in pollutants_dictionary.values() if v is not None],
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




# Bootstrapping:
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
st.subheader("Bootstrapping the Mean of a Pollutant")

selected_pollutant3 = st.selectbox("Select a Pollutant (or All)",list(pollutants_dictionary.keys()))
# Filter data
data = combined_data[pollutants_dictionary[selected_pollutant3]].dropna()
confidence_level = st.number_input(
    "Select Confidence Level",
    min_value=0.0,
    max_value=1.0,
    value=0.95, 
    step=0.05,  
    format="%.2f" 
)
n_iterations = st.number_input(
    "Select Confidence Level",
    min_value=100,
    max_value=10000,
    value=500, 
    step=100,  
    #format="%.2f" 
)
#st.write(f"Bootstrapped 95% Confidence Interval for {selected_pollutant3}: ({lower_bound:.2f}, {upper_bound:.2f})")
with st.spinner("Creating plot.... Please wait."):
    data = (data,)
    res = bootstrap(data, np.std, confidence_level=confidence_level, n_resamples=n_iterations)
    fig, ax = plt.subplots()
    ax.hist(res.bootstrap_distribution, bins=50, color='cornflowerblue', edgecolor='black', density=True)
    ax.axvline(res.confidence_interval.low, color='green', linestyle='dashed',  label=f'{confidence_level} CI Lower Bound')
    ax.axvline(res.confidence_interval.high, color='green', linestyle='dashed',  label=f'{confidence_level} CI Upper Bound')
    ax.axvline(np.mean(res.bootstrap_distribution), color='red', linestyle='dashed',  label='Original Mean')
    ax.set_title(f"Bootstrapping the Mean of {selected_pollutant3} with {confidence_level*100}% Confidende Interval")
    ax.set_xlabel('Level')
    ax.set_ylabel('Frequency')
    ax.legend()
    st.pyplot(fig)
    st.write(f"Confidence interval: {res.confidence_interval}")