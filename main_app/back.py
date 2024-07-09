from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model, encoder, and data
model = joblib.load('model.pkl')
label_encoder = joblib.load('label_encoder.pkl')
monthly_data = joblib.load('monthly_data.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    decoded_predictions = label_encoder.inverse_transform(predictions)
    return jsonify(decoded_predictions.tolist())

@app.route('/data', methods=['GET'])
def get_data():
    return monthly_data.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
