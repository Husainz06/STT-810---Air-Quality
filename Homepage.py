import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the dataset
combined_data = pd.read_csv('pollution_data_2023_all.csv')  # Adjust to your dataset path
pollutants_dictionary = {
    'PM2.5': 'Daily Mean PM2.5 Concentration',
    'Ozone': 'Daily Max 8-hour Ozone Concentration',
    'SO2': 'Daily Max 1-hour SO2 Concentration',
    'NO2': 'Daily Max 1-hour NO2 Concentration',
    'CO': 'Daily Max 8-hour CO Concentration',
    'PM10': 'Daily Mean PM10 Concentration',
    'Pb': 'Daily Mean Pb Concentration'
}
# --- Get a list of numeric pollutant columns ---
numeric_columns = combined_data.select_dtypes(include=[np.number]).columns.tolist()

# Remove 'Date' column from numeric columns list
numeric_columns = [col for col in numeric_columns if 'Date' not in col]

# Pollutant column selection
pollutant_column = st.selectbox("Select a Pollutant", list(pollutants_dictionary.keys()))

# Get the data and clean it for simulation
pollutant_data = pd.to_numeric(combined_data[pollutants_dictionary[pollutant_column]], errors='coerce')
pollutant_data = pollutant_data.dropna()  

st.write("### Part 4: Monte Carlo Simulation")

# monte carlo aparmeters
mu = pollutant_data.mean() 
std = pollutant_data.std()
num_simulations = 1000  
days = 365  # in days to simulate one year

# simulating results
simulated_results = np.random.normal(mu, std, size=(num_simulations, days))
# axis = 1 to calculate the mean accross the rows
# https://panjeh.medium.com/how-to-get-average-of-rows-columns-in-a-numpy-array-8f305dd92624
mean_simulations = simulated_results.mean(axis=1)

plt.figure(figsize=(10, 6))
plt.hist(mean_simulations, bins=50, alpha=0.6, color='orange', edgecolor='black')
plt.title(f"Monte Carlo Simulation of {pollutant_column} over {days} Days")
plt.xlabel(f"Simulated {pollutant_column} Mean Value (µg/m³)")
plt.ylabel("Frequency")
st.pyplot(plt)

# Plot the cumulative distribution of simulated mean pollution values
plt.figure(figsize=(10, 6))
plt.hist(mean_simulations, bins=50, cumulative=True, alpha=0.6, color='blue', edgecolor='black')
plt.title(f"Cumulative Distribution of Simulated {pollutant_column} Means")
plt.xlabel(f"Simulated {pollutant_column} Mean Value (µg/m³)")
plt.ylabel("Cumulative Frequency")
st.pyplot(plt)


user_input = st.number_input(f"Enter the pollution threshold for '{pollutant_column}' to calculate probability.", value=0)
expectd_value = np.mean(mean_simulations > user_input)
st.write(f"Probability of exceeding {user_input} µg/m³: {expectd_value*100}%")

# --- Summary Statistics ---
simulated_mean = np.mean(mean_simulations)
simulated_std = np.std(mean_simulations)

st.write(f"### Monte Carlo Simulation Summary")
st.write(f"Mean of Simulated Pollution Levels: {simulated_mean:.2f}")
st.write(f"Standard Deviation of Simulated Pollution Levels: {simulated_std:.2f}")
