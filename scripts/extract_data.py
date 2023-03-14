import pandas as pd

def read_data(data_path:str)-> pd.DataFrame:

    """ Funtion - Read csv file from path 
    and tranform column and save to parquet 

    Args:
        data_path (str) - path by csv data
    Returns: 
       pandas dataframe 
    """
    
    df = pd.read_csv(data_path)

    df['TotalCharges'] = df['TotalCharges'].apply(lambda x: float(x.replace(' ', '0')))
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0:'No',1:'Yes'})

    df.to_parquet(r'C:\Users\erico\Documents\projeto classificacao\Telco-Customer-Churn\data\curated_data.parquet')

    dataframe = pd.read_parquet(r'C:\Users\erico\Documents\projeto classificacao\Telco-Customer-Churn\data\curated_data.parquet')

    return dataframe

    