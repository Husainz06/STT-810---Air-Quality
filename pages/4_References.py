import streamlit as st

st.title("Data Sources and References")
st.header("Data Source")
st.write("""The datasets used of Michigan's pollution levels of the year 2023 come from the from the EPA 
         Webpage. The datasets can be found [here](https://www.epa.gov/outdoor-air-quality-data/download-daily-data).""")

st.header("References")

st.markdown("""
Below are the references used in creating this project and in writing different pollutant information and 
            information about the statistical and visualization concepts.
- STT 810 Course Material
- CMSE 830 Course Material
- [EPA's Air Quality Index (AQI)](https://www.epa.gov/aqi)
    - [EPA's Particulate Matter (PM) Pollution](https://www.epa.gov/pm-pollution)
    - [EPA's Ozone Pollution](https://www.epa.gov/ozone-pollution)
    - [EPA's Nitrogen Dioxide (NO₂) Pollution](https://www.epa.gov/no2-pollution)
    - [EPA's Sulfur Dioxide (SO₂) Pollution](https://www.epa.gov/so2-pollution)
    - [EPA's Lead Pollution](https://www.epa.gov/lead)
- [Plotly Interactive Plots](https://plotly.com)
- [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
- [Bootstrap Sampling in Python](https://www.digitalocean.com/community/tutorials/bootstrap-sampling-in-python)
- [SciPy Statistical Functions](https://docs.scipy.org/doc/scipy/reference/stats.html)
    - [Chi squared](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html)
- [Bootstrap Method Overview - Wikipedia](https://en.wikipedia.org/wiki/Bootstrapping_(statistics))
- [Understanding Bootstrapping - Towards Data Science](https://towardsdatascience.com/a-gentle-introduction-to-bootstrapping-87714f978f91)
- [Contingency table](https://en.wikipedia.org/wiki/Contingency_table#:~:text=In%20statistics%2C%20a%20contingency%20table,%2C%20engineering%2C%20and%20scientific%20research.)
""")

st.header("Project Materials")
st.markdown("""We have uploaded all the project's code and datasets on 
            [this GitHub Repository](https://github.com/Husainz06/STT-810---Air-Quality.git). You can view or download the code
            and all the used datasets. There's a 'readme, file that has the setup details on local machine and on streamlit.""")
