# Inicializar API REST FLASK
from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load(open(r'C:\Users\erico\Documents\projeto-churn\Telco-Customer-Churn\models\model.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def predict():
    return render_template('predict.html')

@app.route('/predict',methods=['GET','POST'])
def home():

    pred_proba = 0.0
    df = pd.DataFrame()

    if request.method =='POST':

        try:
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
            pred_proba = np.around(pred_proba, decimals=2)
            
        except ValueError:
            print('Enter a valid values please!')


    return render_template('predict.html', prediction = pred_proba)

@app.route('/predict_csv', methods=['GET', 'POST'])
def predict_csv():

    if request.method == 'POST':

        csv_file = request.files['file']
        df1 = pd.read_csv(csv_file)

        pred_proba = model.predict_proba(df1)[:, 1]

        df1["Prediction"] = np.around(pred_proba, decimals=2)
        df1["Prescription"] = np.where(pred_proba >= 0.70, "High Potential Churn - Red alert",
                              np.where(pred_proba >= 0.50, "Moderate Potential Churn - Yellow alert", "No Potential Churn"))
        df1 = df1.reset_index(drop=True)

        return df1.to_html()

    return '''
        <form action="" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''

    
if __name__=='__main__':
    app.run(host='0.0.0.0')