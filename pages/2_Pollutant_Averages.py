# ------------------------------------------------------------------------------
# STT 810 Final Project : Michigan Air Quality Analysis
# Authors: Hussian Aljafer , Jack Ruhala , Bhavya Chawla
# Page Description: This page calculates averages, displays plots and performs bootstrapping
# 
# Date Created: Dec. 2024
# Libraries needed to run the page: streamlit, pandas, plotly, matplotlib, numpy
# Refer to 'README.md' for more information
# GitHub repository link: https://github.com/Husainz06/STT-810---Air-Quality.git
# ------------------------------------------------------------------------------

# Importing the required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


# Page title
st.title("Average Pollutants")

# Reading the combined dataset
combined_data = pd.read_csv('pollution_data_2023_all.csv')

# Defining columns needed for processing
pollutants = [
    'Daily Mean PM2.5 Concentration',
    'Daily Max 8-hour Ozone Concentration',
    'Daily Max 1-hour SO2 Concentration',
    'Daily Max 1-hour NO2 Concentration',
    'Daily Max 8-hour CO Concentration',
    'Daily Mean PM10 Concentration',
    'Daily Mean Pb Concentration'
]


#------------------------------------    Section1: Average pollutants ------------------------------------
st.header("Calculating Average Pollutants")
st.write("""An important measures of analysis is calculating the average of all pollutants per 
         location on any given day. This gives some insight about the pollution vs geographical location. Below is the calculated
         average of the pollutants per location on any given day. As mentioned in the 'Data Overview' page, some locations
         do not keep track of all pollutants and that's why some data is not present in this table.""")

# Calculating the average of each pollutant grouping by the site name
# to get the average of each pololutant in each location
average_pollutants = combined_data.groupby('Local Site Name')[pollutants].mean().reset_index()

# Displaying the results as a table
st.table(average_pollutants)

#------------------------------------    Section2: 2023 Average pollutants ------------------------------------

st.subheader('2023 Pollutant Averages')
st.write("""The following bar plot shows the average pollutant levels per day in 2023 accross the state of Michgan. The bar plot provides a
         general idea on which locations have higher air pollution concentrations and what pollutant, of the once recorded in an area, are most present.
         The bar plot is interactive, you can expand it to fill the screen by using the full screen mode, show/hide locations by
         clicking them in the legend, and you can double click a legend item to remove all other items.""")

# Set the index to 'Local Site Name' as the previous step had no index for the data transpose the DataFrame
average_pollutants.set_index('Local Site Name', inplace=True)
#transposing the DataFrame to have column names representing locations ao allow visualising the data better
average_pollutants = average_pollutants.transpose()

# Creating an interactive bar plot using plotly
fig = px.bar(average_pollutants,
             labels={'value': 'Average Concentration', 'variable': 'Pollutants'},
             title='Average Pollutant Concentrations per Location')

# Setting up the plot's features
fig.update_layout(
    xaxis_title='Pollutants',
    yaxis_title='Average Concentration - 2023',
    legend_title='Locations',
    barmode='group'
)
# SHowing the plot
st.plotly_chart(fig)

#------------------------------------    Subection 2.1: Filtering Average pollutants ------------------------------------
st.subheader('Average Pollutant Level')
st.markdown("""Below, days with highest recorded pollutent level for each site in the year 2023.
            Keep in mind that these pollutants are not tracked in all locations i.e. some pollutants are tracked in more locations
            than others.""")

# Creating a dictionary for the dropdown menu which will aloow showing the pollutant's name instead of the column name.
# The pollutant name will be mapped to the column name using this dictionary
pollutants_dictionary = {
    'PM2.5': 'Daily Mean PM2.5 Concentration',
    'Ozone': 'Daily Max 8-hour Ozone Concentration',
    'SO2': 'Daily Max 1-hour SO2 Concentration',
    'NO2': 'Daily Max 1-hour NO2 Concentration',
    'CO': 'Daily Max 8-hour CO Concentration',
    'PM10': 'Daily Mean PM10 Concentration',
    'Pb': 'Daily Mean Pb Concentration'
}
# Creating a dropdown menu that pulls the pollutant dictionary keys as its options
# The option 'All Pollutants' is added to allow displaying all pollutants
selected_pollutant2 = st.selectbox("Select a Pollutant (or All)" 
                , ["All Pollutants"] + list(pollutants_dictionary.keys()), key="pollutant_select")

# Selecting between displayin all pollutant data vs a single pollutant based on the user's choice
if selected_pollutant2 != "All Pollutants":
    
    # ussing agg() and NamedAgg() to apply the max() function to the selected column to select the daily max concentration 
    filtered_data = combined_data.groupby('Local Site Name').agg(
        Max_Concentration=pd.NamedAgg(column=pollutants_dictionary[selected_pollutant2], aggfunc='max')
    ).reset_index()

else:
    # If "All Pollutants" is selected, stack the data for plotting
    # Using the melt function to combine pollutants into one column
    melted_data = combined_data.melt(
        id_vars='Local Site Name', 
        value_vars=[v for v in pollutants_dictionary.values() if v is not None],
        var_name='Pollutant', 
        value_name='Concentration'
    )
    filtered_data = melted_data.groupby(['Local Site Name', 'Pollutant']).agg(Max_Concentration=('Concentration', 'max')).reset_index()

# Create the bar plot 
if not filtered_data.empty:
    # Checing if we have all pollutants to stack them all
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
    # Plotting a single pollutant  
    else:
        fig = px.bar(
            filtered_data,
            x='Local Site Name',
            y='Max_Concentration',
            # Reading the pollutant name and including it in the title of the plot
            title=f"{selected_pollutant2} Levels by Location",
            labels={"Local Site Name": "Location", "Max_Concentration": "Max Concentration"},
            text='Max_Concentration'
        )
    
    # Show values on top of the bars for easier readability
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(height=800) 
    # Show the plot
    st.plotly_chart(fig)
# When do data is found
else:
    st.write("No data available for the selected pollutant and locations.")

# Elaboration text below the plot 
st.markdown("""While not expicitly shown by the data, We can see a pattern in the plot above where the higher the total polutents in an area, the more polutents are recorded in the area.
               The recording of polutents beyond PM2.5 trends with an increase population and urban development""")



#------------------------------------    Subection 2.2: Filtering Average Pollutants by Date ------------------------------------

st.subheader("Filtering Averages by Date")
st.markdown(""" Understanding pollution over time can help identify temporal trends in the data. 
         The chart below is filter by month and location to allow getting more detailed information about the daily polution averages over time.
         
Use the drop-down menus below to display average pollutant level on some michigan locations. If there's no information on the plot, 
            this means that the pollutant is not being tracked at that location.""")

# Plot 2
#Using the same dictionary above to create a menu
# dropdown menu with a different name to separate the plots and their menus
selected_pollutant = st.selectbox("Select a Pollutant", list(pollutants_dictionary.keys()))

# Getting all locations and avoiding redunduncy by using unique()
locations = combined_data['Local Site Name'].unique()

# Getting the selected location based on the user's choice
selected_location = st.selectbox("Select a Location", locations)

# Using the selections to filter data
filtered_data = combined_data[combined_data['Local Site Name'] == selected_location]

# Creating a plot using plotly
# Using the selected data for labeling
fig = px.bar(filtered_data, x='Date', y=pollutants_dictionary[selected_pollutant],
    title=f"{selected_pollutant} Levels at {selected_location}",labels={"x": "Date", "y": selected_pollutant})
#displaying the plot
st.plotly_chart(fig)

# Elaboration on the spikes in the plots
st.markdown("""
When we look at the month-filtered plot, we can see a clear outlier in some pollutants around mid 2023. 
            if we compare the mid summer outliers events during the year, we find that the polutent outliers was most likely cused by a wildfire. 
            **Canada** in mid 2023, particularly in the **Quebec** and **Ontario** regions experiance some of the worst wildfires ever recorded.
            The smoke from the canaidan wildfires fires spread over vast distances, 
            drifting into the  United States, including Michigan, during the late spring and early summer months.
            Wildfire smoke contains large amounts of fine particulate matter (PM2.5), carbon monoxide (CO), and ground-level ozone. 

During the wildfire event, spikes in PM2.5, ozone, and other pollutants were noticeable in the data for Michigan. These peaks were 
            particularly sharp during the months of **June and July 2023**, when the wildfires were at their peak intensity. 
            The plot we see may reflect these sudden increases in pollutant levels, showing a temporary but significant rise in 
            concentrations that corresponds with the wildfire smoke's reach.
""")


# ------------------------------------    Subection 3: Bootstrapping ------------------------------------

# Function to perform bootstrapping for the mean using numpy
# setting default values for the iterations(samples) and CI
def bootstrap_mean(data, n_iterations=1000, conf_lev= 95):
    # Getting the sample's size
    sample_size = len(data) 
    #list to save the means 
    means = []

    # looping as many times as requested based on the function's input
    for i in range(n_iterations):
        sample = np.random.choice(data, size=sample_size, replace=True)
        means.append(np.mean(sample))
    
    lower_conf = (100 - conf_lev)/2
    upper_conf = 100 - lower_conf

    # calculating the means
    means = np.array(means)

    # calculating lower and upper CI bounds
    lower_bound = np.percentile(means, lower_conf)#2.5) 
    upper_bound = np.percentile(means, upper_conf)
    # returning means, lower bound, and upper bound
    return means, lower_bound, upper_bound

# Section title and text
st.header("Bootstrapping the Mean of a Pollutant")
st.markdown("""Bootstrapping is a statistical technique used to estimate the uncertainty of a statistic (like the mean) by repeatedly 
            resampling from the data we already have. It works by creating multiple “bootstrap samples” - random samples taken with 
            replacement from the original dataset - and then calculating the statistic (in this case, the mean) for each sample.

This method is especially useful when we don't know the underlying distribution of the data or when we want to estimate the precision 
            of a statistic without relying on complex parametric models. By generating a large number of bootstrap samples, we can 
            build a distribution of the statistic and estimate how much it would vary in different samples from the population.

In this analysis, we are using bootstrapping to estimate the variability of the **mean pollutant concentration**. By generating 
            multiple samples, we can calculate the mean for each sample and create a distribution of those means. From this, we 
            can derive confidence intervals to understand the range within which the true population mean likely falls.

### Why Use Bootstrapping in This Project?

Air quality data, like pollutant concentrations, often don't follow simple, well-known distributions. Traditional statistical 
            methods, like t-tests, assume certain characteristics about the data, such as normality. Bootstrapping doesn't make 
            these assumptions, which makes it a flexible and powerful tool for analyzing real-world environmental data, where 
            normality cannot always be guaranteed.

This approach gives us a clearer picture of the variability in pollutant concentrations, helping us make more robust conclusions 
            about air quality. To begin, please select the pollutant we want to analyze, the confidence intervals and the
         number of samples for the analysis.
        
""")

# Dropdown menu form the same distionary above
selected_pollutant3 = st.selectbox("Select a Pollutant (or All)",list(pollutants_dictionary.keys()))

# Numberical input for the CIs
confidence_level = st.number_input("Select Confidence Level", min_value = 0, max_value = 100, value = 95, step = 5)

# Numerical input for the number of samples
n_samples = st.number_input("Select Number of Samples", min_value = 100, max_value = 100000, value = 500, step = 100)

# Selecting non-null data for the computation
data = combined_data[pollutants_dictionary[selected_pollutant3]].dropna()

# Perform bootstrapping
# Adding st.spinner to show a spinning circle while the plot is loading.
# Wde added this since sometimes the plot may take a while to load

with st.spinner("Generating confidence intervals....Please wait."):

    #calling the bootstrap function
    means, lower_bound, upper_bound = bootstrap_mean(data, n_iterations= n_samples, conf_lev=confidence_level)

    # Plotting the histogram
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(means, bins=50, alpha=0.7, color='blue', edgecolor='black')
    
    # Plotting the lines for mean, lower bound, and upper bound
    ax.axvline(np.mean(data), color='red', linestyle='dashed', linewidth=2, label='Original Mean')
    ax.axvline(lower_bound, color='orange', linestyle='dashed', linewidth=2, label=f'{confidence_level}% CI Lower Bound')
    ax.axvline(upper_bound, color='green', linestyle='dashed', linewidth=2, label=f'{confidence_level}% CI Upper Bound')

    # Setting the title based on the selected pollutant
    ax.set_title(f"Bootstrapping the Mean of {selected_pollutant3}")

    # Showing the legend
    ax.legend()

    # Showing the plot
    st.pyplot(fig)

    # Display confidence intervals as text below the plot
    st.write(f"Bootstrapped {confidence_level}% Confidence Interval for {selected_pollutant3}: ({lower_bound:.2f}, {upper_bound:.2f})")

# ------------------------------------------------  Subsection 3.1: Interpretting the plot
st.header("Interpreting the Bootstrap Histogram")

st.markdown("""Below is how we can interpret the bootstrap plot above:

- **The X-axis**: This shows the different mean concentrations of the pollutant. 
  
- **The Y-axis**: This shows the frequency (or count) of how often each range of mean values appeared in the bootstrap samples.

- **Bootstrap Mean**: The vertical line represents the **original mean** of the data (the mean of the observed pollutant 
            concentrations). This gives us a reference point to see where the observed data’s mean lies within the distribution 
            of means from the bootstrap samples.

- **Confidence Intervals**: are the ranges where the true population mean is likely to fall, based on the bootstrapped data. 
            For example, if we're looking at a 95\% confidence interval, it means that, if we were to take many samples from 
            the population, 95 of them would likely fall within this range. 

### What Does This Tell Us?

- A **wide distribution** of bootstrap means indicates that there is a lot of variability in the pollutant concentration, 
            suggesting the observed mean might not be stable or that the data is quite spread out.
- A **narrow distribution** of means suggests more consistency in the data, meaning the true mean is likely more stable and 
            we can have more confidence in its precision.
These insights help us understand the level of uncertainty around our estimates of air pollution. Bootstrapping allows us to 
            visualize this uncertainty in a clear, accessible way, so we can make better-informed decisions when analyzing air 
            quality data.
""")
