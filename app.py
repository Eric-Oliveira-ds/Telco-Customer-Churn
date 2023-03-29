# Inicializar API REST FLASK
from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import ClassificationPreset


# Load model
model = joblib.load(open('models/model.pkl','rb'))

app = Flask(__name__)

# HOME
@app.route('/')
def predict():
    return render_template('predict.html')

# Predict single case
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

# predict from database and praticie MLOps-monitoring results from model test
@app.route('/predict_csv', methods=['GET', 'POST'])
def batch_monitoring():

    if request.method == 'POST':
        # get file
        csv_file = request.files['file']
        # read current
        current = pd.read_csv(csv_file)
        # Transform raw data current
        current['SeniorCitizen'] = current['SeniorCitizen'].map({0:'No',1:'Yes'})
        current = current.set_index(['customerID']).copy()
        current.drop(['gender','PhoneService'], inplace=True, axis=1)
        # get predictions (current)
        current['No'] = np.around(model.predict_proba(current)[:,0], decimals=2)
        current['Yes'] = np.around(model.predict_proba(current)[:,1], decimals=2)
        current['Prediction'] = model.predict(current)
        current['Prediction'] = current['Prediction'].map({1:'Churn', 0:'No Churn'})
        current["Prescription"] = np.where(current['Yes'] >= 0.70, "High Potential Churn - Red alert",
                                  np.where(current['Yes'] >= 0.50, "Moderate Potential Churn - Yellow alert", "No Potential Churn"))
        # reset index ID column                      
        current.reset_index(drop=True)

        # read reference
        reference = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
        reference = reference.sample(20)
        # Transform raw data refernce
        reference['SeniorCitizen'] = reference['SeniorCitizen'].map({0:'No',1:'Yes'})
        reference = reference.set_index(['customerID']).copy()
        reference.drop(['gender','PhoneService'], inplace=True, axis=1)
        # get predictions (reference)
        reference['No'] = np.around(model.predict_proba(reference)[:,0], decimals=2)
        reference['Yes'] = np.around(model.predict_proba(reference)[:,1], decimals=2)
        reference['Prediction'] = model.predict(reference)
        reference['Prediction'] = reference['Prediction'].map({1:'Churn', 0:'No Churn'})
        reference["Prescription"] = np.where(reference['Yes'] >= 0.70, "High Potential Churn - Red alert",
                                    np.where(reference['Yes'] >= 0.50, "Moderate Potential Churn - Yellow alert", "No Potential Churn"))

        # generate classification performance dashboard
        column_mapping = ColumnMapping()
        column_mapping.target = 'Churn'
        column_mapping.prediction = ['No', 'Yes']
        column_mapping.pos_label = 'Yes'
        # get dashboard
        classification_performance_report = Report(metrics=[ClassificationPreset(),])
        classification_performance_report.run(reference_data=reference, current_data=current, column_mapping = column_mapping)
        classification_performance_report.save_html('templates/production_monitoring_report.html')

        # drop target
        current.drop(['Churn'], inplace=True, axis=1)
        reference.drop(['Churn'], inplace=True, axis=1)
        

        return current.to_html()

    return '''
            <form action="" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
        '''

@app.route('/production_monitoring')
def production_monitoring():

    return render_template('production_monitoring_report.html')

    
if __name__=='__main__':
    app.run(debug=True)