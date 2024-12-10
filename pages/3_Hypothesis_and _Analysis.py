import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import numpy as np
import plotly.graph_objects as go


combined_data = pd.read_csv('pollution_data_2023_all.csv')

# Select columns with pollutant concentrations for PCA
pollutant_columns = [
    'Daily Mean PM2.5 Concentration', 'Daily Max 8-hour Ozone Concentration', 
    'Daily Max 1-hour SO2 Concentration', 'Daily Max 1-hour NO2 Concentration', 
    'Daily Max 8-hour CO Concentration', 'Daily Mean PM10 Concentration'
]

st.title("Hypothesis Testing")

# Chi-Square Test for Categorical Data
# I need to double check these values 
def categorize_aqi(aqi_value):
    if aqi_value <= 50:
        return 'Good'
    elif aqi_value <= 100:
        return 'Moderate'
    elif aqi_value <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif aqi_value <= 200:
        return 'Unhealthy'
    elif aqi_value <= 300:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'

# Feature engineering part: Adding AQI category for Chi-Square
combined_data['AQI_Category'] = combined_data['Daily AQI Value'].apply(categorize_aqi)

# Create a contingency table for 'Local Site Name' and 'AQI_Category'
contingency_table = pd.crosstab(combined_data['Local Site Name'], combined_data['AQI_Category'])
chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)

st.write("""A Chi-Square Test of Independence was preformed to determine whether there is a significant relationship between 
         the location and the AQI category. Below is the hypothesis and the outputs of our testing:

- Null Hypothesis (H0): Location and AQI category are independent.
- Alternative Hypothesis (H1): Location and AQI category are dependent.
""")


st.write(f"""- **Chi-Square Statistic: {chi2_stat:.2f}:** 
    The Chi-square value measures the difference between the observed frequencies and the expected frequencies under 
    the null hypothesis. A higher Chi-Square statistic suggests a larger discrepancy, indicating a stronger 
    association between the variables being tested (in this case, location and AQI category).""")  
st.write(f"""- **P-Value: {p_value:.2e}:**
    The p-value tells us whether the observed difference is statistically significant. In this case, 
         the p-value of {p_value:.2e} indicates that the probability of obtaining the observed data, assuming the 
         null hypothesis is true, is almost zero. Since this is much smaller than the typical significance 
         level of 0.05, we reject the null hypothesis and conclude that there is a significant relationship 
         between location and AQI category.""")
    
st.write(f"""- **Degrees of Freedom: {dof}:**
    Degrees of freedom represent the number of independent comparisons we can make between the groups.
    In this case, it is {dof}, which corresponds to the number of categories in our contingency table.""")

# Cheching hypothesis using p-value
if p_value < 0.05:
    st.write("""Since the p-value is less than 0.05, we reject the null hypothesis, indicating that 
             there is a significant relationship between the location and AQI category.""")
else:
    st.write("""Since the p-value is greater than 0.05, we fail to reject the null hypothesis, suggesting that there is
              no significant relationship between the location and AQI category.""")



# contingency table heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(contingency_table, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Count'})
ax.set_title('Heatmap of AQI Categories by Location')
ax.set_xlabel('AQI Category')
ax.set_ylabel('Location')
st.pyplot(fig)

st.write("""The heatmap above visualizes the distribution of AQI categories across different locations. Each cell in the heatmap 
    represents the count of observations for a specific combination of location and AQI category.
         
- Columns (AQI Category): Columns represent different categories of air quality based on AQI values; 
      'Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', and 'Very Unhealthy'.
- Rows (Location): Rows represent different locations where air quality measurements were taken.
- Cell Values: The numbers in each cell indicate the number of times a specific AQI category was recorded for that 
      location.
- Color Intensity: The color intensity is a representaion of the cells value: darker colors indicate a higher count 
      of observations, while lighter colors represent fewer occurrences.""")

st.subheader('Key Insights')
st.write("""- Locations with darker shades in certain AQI categories indicate more frequent occurrences of those AQI levels at 
      that location.
- By examining the heatmap, you can identify trends, such as whether certain locations tend to have more 'Unhealthy' 
      or 'Good' air quality days.""")

st.header("Multivariate Analysis - Covariance and Correlation")

st.write("""This heatmaps visualize relationships between different pollutants using correlation and covariance. 
    These heatmaps provide insights into how pollutants in the air are related to each other.""")

# Filter the combined_data DataFrame to only include the pollutant columns
pollutant_data = combined_data[pollutant_columns]

# getting the correlation matrix and covariance matrix
corr_matrix = pollutant_data.corr()
cov_matrix = pollutant_data.cov()

st.subheader("Covariance Heatmap")
st.markdown("""The correlatione heatmap shows the covariance between different features of a dataset. Covariance is a measure of how much two 
            variables change together.
    - A positive covariance means that as one variable increases, the other also also increases.
    - A negative covariance means that as one variable increases, the other decreases decreases.""")

plt.figure(figsize=(14, 10))
sns.heatmap(cov_matrix, annot=True, cmap='YlGnBu', fmt='.2f', cbar=True, linewidths=0.5, square=True)
st.pyplot(plt)


st.subheader("Correlation Heatmap")
st.write("""The correlation heatmap shows how different pollutants are linearly related to each other. 
    The values range from -1 to 1:
    - As the value moves closer to one, we have a stronger positive correlation where both variables move in the same direction.
    - As the value moves closer to  negative one, we have a stronger negative correlation where both variables move in 
         the opposite direction.
    - A value close to 0 means that there is no linear correlation.
""")
plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, cmap='YlGnBu', fmt='.2f', cbar=True, linewidths=0.5, square=True)
st.pyplot(plt)



st.subheader("Insights from the Heatmaps")
st.write("""- Correlation Heatmap: The correlation matrix shows covariance of criteria pollutant records over time. Laeger positive 
         values indicate that the two intersecting pollutants, are more likely positively correlated.""")
st.write("""- Correlation Heatmap: Pairs of pollutants with strong correlations (close to 1 or -1), like `PM2.5` and `PM10`, indicates that they often occur together in certain environments. 
      `PM2.5` and `PM10` are likely positively correlated because the two pollutants are brough categories of pollutants that often come from the same source.
      Another promising correlations observed is between `PM10` and carbon monoxide (`CO`).
      ('CO') is one of the most common pollutants that makes up 'PM10' so its reasonable to believe the two pollutants are correlated.
      `PM2.5` and `CO` which is suggested to be positively correlated confirmed by the heatmap although it suggested that they might share a confounder in 'PM10'.\n""")



