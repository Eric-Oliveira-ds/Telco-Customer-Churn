import pandas as pd
import sys

def read_csv_data(data_path:str)-> pd.DataFrame:

    """ Funtion - Read csv file from path
        Receive:
            data_path - path by csv data
        Return: 
            dataframe pandas
    """
    df = pd.read_csv(data_path)

    return df

    