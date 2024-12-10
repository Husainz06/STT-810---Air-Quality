import streamlit as st

# Set page title
st.title("Michigan Air Quality Analysis")


# Introduction paragraph
st.markdown("""
Air pollution is a growing concern across the globe, with significant implications for human health, the environment, 
and the economy. In Michigan, air quality is a critical issue, with pollutants like ozone, particulate matter, and nitrogen 
dioxide affecting both urban and rural areas. This project aims to bring clarity to these complex issues by providing insights 
into pollution levels across Michigan in 2023 using data from the [Environmental Protection Agency (EPA)](https://www.epa.gov/).
""")

# Section: Understanding Air Pollution and Key Pollutants
st.header("Air Pollution and Key Pollutants we Tracked")


st.markdown("""
The following list pollutants called criteria pollutents and have national laws limiting there expoures to the enviroment:

- **Carbon Monoxide (CO)**: A colorless, odorless gas that can interfere with the body's ability to absorb oxygen, especially 
harmful in enclosed spaces. [Learn more about CO](https://www.epa.gov/co-pollution)

- **Particulate Matter (PM2.5 and PM10)**: Fine particles in the air that can be inhaled into the lungs. PM2.5, which is smaller 
than PM10, is particularly irritating due to its ability to reach deep into the respiratory system. 
[Learn more about PM](https://www.epa.gov/pm-pollution)

- **Ozone (O₃)**: A harmful air pollutant that forms when sunlight reacts with pollutants from vehicles and industrial emissions. 
High levels of ground-level ozone can worsen respiratory conditions. [Learn more about Ozone](https://www.epa.gov/ozone-pollution)

- **Nitrogen Dioxide (NO₂)**: A gas that can irritate the lungs and is a key component in the formation of smog. It’s mainly produced 
by burning fuel, like in vehicles and power plants. [Learn more about NO₂](https://www.epa.gov/no2-pollution)

- **Sulfur Dioxide (SO₂)**: A gas released by burning fossil fuels, particularly in power plants and industrial processes. SO₂ can 
irritate the respiratory system and contribute to acid rain. [Learn more about SO₂](https://www.epa.gov/so2-pollution)

- **Lead (Pb)**: A toxic metal that can cause serious health problems, particularly in children. Lead exposure can come from old 
paints, contaminated water, and air pollution. [Learn more about Lead](https://www.epa.gov/lead)""")

# Section: The Role of the EPA
st.header("The Role of the Environmental Protection Agency (EPA)")

st.markdown("""
The **Environmental Protection Agency (EPA)** is a U.S. government agency that protects the environment. 
The EPA monitors air quality nationwide through a network of air quality monitoring stations. The EPA lobbies for air quality standards 
of criteria pollutants and provides real-time data on pollution levels via the **Air Quality Index (AQI)**. 

For more details about the EPA and their role in air quality, visit [EPA website](https://www.epa.gov/).
""")

# Section: What This Application Does
st.subheader("What This Application Does")

st.markdown("""
This application allows you to explore air quality data across Michigan. Using datasets from the EPA dating in 2023, this 
application visualizes pollution levels for most criteria pollutants. 
            The main features of the app include:

- **Pollution Visualizations**: Interactive graphs and maps showing pollution levels across Michigan.
- **Location Filtering**: Focus on specific regions in Michigan to analyze air quality.
- **Bootstrap Analysis**: Assess the variability of pollutants using bootstrapped means with user-defined confidence intervals.
- **Hypothesis Testing**: Check if there is any correlation between pollution levels and specific locations.
    - Using Feature engineering to add a 'Qaulity Measure' column to allow use for $$Chi^2$$ hypothesis testing.
- **Covariance and Correlation Matrices**: Analyze the relationships between different pollutants.

The goal is to make air quality data more accessible and provide insights into pollution trends, helping to understand its impact 
on public health and the environment.
""")


