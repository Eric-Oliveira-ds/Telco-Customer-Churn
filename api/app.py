# Inicializar API REST FLASK
from flask import Flask, request
import joblib
import json
import pandas as pd
import numpy as np

# Load model
model = joblib.load(open(r'C:\Users\erico\Documents\projeto-churn\Telco-Customer-Churn\models\model.pkl','rb'))

app = Flask(__name__)

@app.route('/predict', methods=['POST'])

def churn_predict():
    request_data = request.get_json(force=True)
    if request_data:
        if isinstance(request_data, dict):
            test_raw = pd.DataFrame(request_data, index=[0])
        else:
            test_raw = pd.DataFrame(request_data, columns=request_data[0].keys())

        pred_proba = model.predict_proba(test_raw)[:, 1]

        test_raw["Prediction"] = pred_proba
        test_raw["Prescription"] = np.where(pred_proba >= 0.50, "Potential Churn - Red alert", "No Potential Churn")

        response = test_raw.to_dict(orient="records")

    return json.dumps(response)
   
if __name__ == "__main__":
    app.run(host='0.0.0.0')