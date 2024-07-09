import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import joblib
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# Initialize Streamlit app
st.title('DISEASE OUTBREAK ANALYSIS')

# Initialize Flask app
app = Flask(__name__)

# Load data from Flask API
@st.cache_data  # Use st.cache_data instead of st.cache
def load_data():
    response = requests.get('http://127.0.0.1:5000/data')
    data_json = response.json()
    data = pd.DataFrame(data_json)
    data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(day=1))
    return data

# Load model, encoder, and data for Flask routes
def load_model_and_data():
    model = joblib.load('model.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    monthly_data = joblib.load('monthly_data.pkl')
    return model, label_encoder, monthly_data

# Load initial data for Streamlit
data = load_data()

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

# Display current status with larger font size
@st.cache_data  # Use st.cache_data instead of st.cache
def get_latest_status(country_data, label_encoder):
    latest_status = country_data['Status'].iloc[-1]
    status_label = label_encoder.inverse_transform([latest_status])[0]
    return status_label

latest_status = get_latest_status(country_data, label_encoder)

st.header(f'THE LATEST OUTBREAK STATUS FOR {country.upper()} IS:')
st.markdown(
    f"""
    <div style="background-color: rgba(14,17,23,255); padding: 20px; border-radius: 5px; border: 5px solid white; text-align: center;">
        <h1 style="color: white;">{latest_status.upper()}</h1>
    </div>  
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)
st.title("PRECAUTIONS TO BE TAKEN: ")
# Embed YouTube video
st.markdown(
    """
    <iframe width="560" height="315" src="https://www.youtube.com/embed/sO1N6SLmVnA?si=094G16EvKImPHO4n" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
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

# Flask routes for prediction and data retrieval
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame(data)
    model, label_encoder, _ = load_model_and_data()  # Load model and encoder
    predictions = model.predict(df)
    decoded_predictions = label_encoder.inverse_transform(predictions)
    return jsonify(decoded_predictions.tolist())

@app.route('/data', methods=['GET'])
def get_data():
    _, _, monthly_data = load_model_and_data()  # Load monthly data for Streamlit
    return monthly_data.to_json(orient='records')

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
