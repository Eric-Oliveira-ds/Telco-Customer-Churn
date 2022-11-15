import pandas as pd

def read_data(data_path:str)-> pd.DataFrame:

    """ Funtion - Read csv file from path 
    and tranform column and save to parquet 

        Receive:
            data_path - path by csv data
        Return: 
            dataframe pandas
    """
    
    df = pd.read_csv(data_path)

    df['TotalCharges'] = df['TotalCharges'].apply(lambda x: float(x.replace(' ', '0')))
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0:'No',1:'Yes'})

    df.to_parquet(r'C:\Users\erico\OneDrive\Documentos\Projeto-Eric-Churn\Telco-Customer-Churn\data\curated_data.parquet')

    dataframe = pd.read_parquet(r'C:\Users\erico\OneDrive\Documentos\Projeto-Eric-Churn\Telco-Customer-Churn\data\curated_data.parquet')

    return dataframe

    