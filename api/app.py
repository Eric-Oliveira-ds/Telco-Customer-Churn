# Inicializar API REST FLASK
from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
import json

# Load model
model = joblib.load(open(r'C:\Users\erico\Documents\projeto-churn\Telco-Customer-Churn\models\model.pkl','rb'))

app = Flask(__name__)

def predict():
    return render_template('predict.html')

pred_proba = " "

@app.route('/predict',methods=['GET','POST'])
def home():

    global pred_proba

    if request.method =='POST':

        SeniorCitizen = str(request.form['SeniorCitizen'])
        Partner = str(request.form['Partner'])
        Dependents = str(request.form['Dependents'])
        tenure = int(request.form['tenure'])
        MultipleLines = str(request.form['MultipleLines'])
        InternetService = str(request.form['InternetService'])
        OnlineSecurity = str(request.form['OnlineSecurity'])
        OnlineBackup = str(request.form['OnlineBackup'])
        DeviceProtection = str(request.form['DeviceProtection'])
        TechSupport = str(request.form['TechSupport'])
        StreamingTV = str(request.form['StreamingTV'])
        StreamingMovies = str(request.form['StreamingMovies'])
        Contract = str(request.form['Contract'])
        PaperlessBilling = str(request.form['PaperlessBilling'])
        PaymentMethod = str(request.form['PaymentMethod'])
        MonthlyCharges = float(request.form['MonthlyCharges'])
        TotalCharges = float(request.form['TotalCharges'])

        data = {
            'SeniorCitizen': [SeniorCitizen],
            'Partner': [Partner],
            'Dependents': [Dependents],
            'tenure': [tenure],
            'MultipleLines': [MultipleLines],
            'InternetService': [InternetService],
            'OnlineSecurity': [OnlineSecurity],
            'OnlineBackup': [OnlineBackup],
            'DeviceProtection': [DeviceProtection],
            'TechSupport': [TechSupport],
            'StreamingTV': [StreamingTV],
            'StreamingMovies': [StreamingMovies],
            'Contract': [Contract],
            'PaperlessBilling': [PaperlessBilling],
            'PaymentMethod': [PaymentMethod],
            'MonthlyCharges': [MonthlyCharges],
            'TotalCharges': [TotalCharges]
        }

        df = pd.DataFrame(data)

        pred_proba = model.predict_proba(df)[:, 1]

    return render_template('predict.html', prediction = pred_proba)

@app.route('/predict_csv', methods=['GET', 'POST'])
def predict_csv():

    if request.method == 'POST':

        csv_file = request.files['file']
        df = pd.read_csv(csv_file)
        df['TotalCharges'] = df['TotalCharges'].apply(lambda x: float(x.replace(' ', '0')))
        df['SeniorCitizen'] = df['SeniorCitizen'].map({0:'No',1:'Yes'})
        df1 = df.set_index(['customerID']).copy()
        df1.drop(['gender','PhoneService','Churn'], inplace=True, axis=1)

        pred_proba = model.predict_proba(df1)[:, 1]

        df1["Prediction"] = pred_proba
        df1["Prescription"] = np.where(pred_proba >= 0.50, "Potential Churn - Red alert", "No Potential Churn")
        df1 = df1.reset_index()

        response = df1.to_dict(orient="records")

        return df1.to_html() #json.dumps(response)
    return '''
        <form action="" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''

if __name__=='__main__':
    app.run(host='0.0.0.0')