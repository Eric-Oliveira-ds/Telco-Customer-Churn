import pandas as pd
import sys

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

    df.to_parquet(r'C:\Users\erico\OneDrive\Documentos\Projeto-Eric-Churn\Telco-Customer-Churn\data\curated_data.parquet')

    dataframe = pd.read_parquet(r'C:\Users\erico\OneDrive\Documentos\Projeto-Eric-Churn\Telco-Customer-Churn\data\curated_data.parquet')

    return dataframe

    