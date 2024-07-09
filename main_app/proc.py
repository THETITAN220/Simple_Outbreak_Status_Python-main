import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
# Load data
data = pd.read_csv('data.csv')  # Assuming the data has a header
# Preprocess data
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year
# Drop the 'Date' column before aggregation
data = data.drop(columns=['Date'])
# Aggregate data to get monthly cases and deaths per country
monthly_data = data.groupby(['Country', 'Year', 'Month']).sum().reset_index()
# Define labels based on cases
def label_status(cases):
    if cases == 0:
        return 'neither'
    elif cases < 100:
        return 'emergence'
    elif cases < 1000:
        return 'epidemic'
    else:
        return 'pandemic'
monthly_data['Status'] = monthly_data['Cases'].apply(label_status)
# Encode labels
label_encoder = LabelEncoder()
monthly_data['Status'] = label_encoder.fit_transform(monthly_data['Status'])
# Define features and labels
features = monthly_data[['Cases', 'Deaths', 'Month', 'Year']]
labels = monthly_data['Status']
# Split data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)
# Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
# Save model and encoder
joblib.dump(model, 'model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
joblib.dump(monthly_data, 'monthly_data.pkl')  # Save the processed data for Streamlit