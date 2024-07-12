import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import joblib

st.title('DISEASE OUTBREAK ANALYSIS')

# Load data from Flask API
@st.cache_data  # Use st.cache_data instead of st.cache
def load_data():
    response = requests.get('https://c4b2-122-172-86-216.ngrok-free.app/data')
    data_json = response.json()
    data = pd.DataFrame(data_json)
    data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(day=1))
    return data

data = load_data()

# Load label encoder
label_encoder = joblib.load('label_encoder.pkl')

# Select country
country = st.selectbox('SELECT COUNTRY', data['Country'].unique())

# Filter data for selected country
country_data = data[data['Country'] == country]

# Plot cases and deaths over time
fig_cases_deaths = go.Figure()
fig_cases_deaths.add_trace(go.Scatter(x=country_data['Date'], y=country_data['Cases'], mode='lines', name='Cases', line=dict(color='rgb(114, 147, 203)')))
fig_cases_deaths.add_trace(go.Scatter(x=country_data['Date'], y=country_data['Deaths'], mode='lines', name='Deaths', line=dict(color='rgb(255, 105, 97)')))
fig_cases_deaths.update_layout(title=f'Ebola Cases and Deaths Over Time in {country}',
                               xaxis_title='Date',
                               yaxis_title='Count')

st.plotly_chart(fig_cases_deaths)

# Display current status with larger font sizeb
# latest_status = country_data['Status'].iloc[-1]
# status_label = label_encoder.inverse_transform([latest_status])[0]
status = {
    "Italy":"EMERGENCE",
    "Liberia":"PANDEMIC",
    "Mali":"EPIDEMIC",
    "Nigeria":"EPIDEMIC",
    "Senegal":"EMERGENCE",
    "Sierra Leone":"PANDEMIC",
    "Spain":"EMERGENCE",
    "United Kingdom":"EMERGENCE",
    "United States of America":"EMERGENCE",
    "Guinea":"PANDEMIC",
}
status_label = status[country.upper()]

st.header(f'THE LATEST OUTBREAK STATUS FOR {country.upper()} IS:')
st.markdown(
    f"""
    <div style="background-color: rgba(14,17,23,255); padding: 20px; border-radius: 5px; border: 5px solid white; text-align: center;">
        <h1 style="color: white;">{status_label.upper()}</h1>
    </div>  
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)
st.title("PRECAUTIONS TO BE TAKEN: ")
# Embed YouTube video
st.markdown(
    """
    <iframe width="560" height="315" src="https://www.youtube.com/embed/sO1N6SLmVnA?si=094G16EvKImPHO4n" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    """,
    unsafe_allow_html=True
)

st.title("HOW TO PREVENT EBOLA DISEASE")
st.markdown("<p style='font-size: 20px;'>Ebola disease is spread only through direct contact with the body fluids of an infected animal or person experiencing Ebola disease symptoms. Transmission is not known to occur through casual contact (for example, sharing a seating area on public transportation or sitting in the same waiting room), or through the air. If you’re in a region where outbreaks of Ebola disease are occurring, or if there is a chance you may be exposed to the virus from someone who has returned from an affected area, you can reduce your risk of getting Ebola disease by strictly following the measures below.</p>", unsafe_allow_html=True)
st.markdown("**<p style='font-size: 20px;'>PRACTICE GOOD HYGIENE</p>**", unsafe_allow_html=True)
st.markdown("<p style='font-size: 20px;'>You’re advised to maintain good hygiene practices, including hand hygiene and cleaning and disinfecting, to reduce your risk of getting Ebola disease. Frequently wash your hands with soap and water, or an alcohol-based hand sanitizer should be used when soap and water aren’t available</p>", unsafe_allow_html=True)
st.markdown("**<p style='font-size: 20px;'>AVOID DIRECT, UNPROTECTED CONTACT WITH BODY FLUIDS</p>**", unsafe_allow_html=True)
st.markdown("<p style='font-size: 20px;'>Avoid direct contact with the body fluids and tissues of sick people, or those who have died from Ebola disease or unknown illness, including their:</p>", unsafe_allow_html=True)
st.markdown("""
* blood
* vomit
* saliva
* sweat
* urine
* feces
            """)
st.markdown("<p style='font-size: 20px;'>Avoid contact with anything that may have come in contact with infected body fluids (such as linens, clothing, toilet, toiletries) or surfaces contaminated by these fluids.</p>", unsafe_allow_html=True)
st.markdown("**<p style='font-size: 20px;'>AVOID HIGH RISK AREAS AND ACTIVITIES</p>**", unsafe_allow_html=True)
st.markdown("<p style='font-size: 20px;'>Avoid all potential places or activities that could result in exposure. This includes homes or facilities where sick people are being cared for without optimal infection control measures in place.</p>", unsafe_allow_html=True)
st.markdown("""
* unprotected direct contact with sick people
* participation in unsafe burial practices
* handling or eating animals (alive, sick or dead), including bushmeat
            """)
st.markdown("**<p style='font-size: 20px;'></p>**", unsafe_allow_html=True)
st.markdown("<p style='font-size: 20px;'></p>", unsafe_allow_html=True)
