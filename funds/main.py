"""main function for using funds"""
import pandas as pd

def get_levereged_fund_list():
    """return list of levereged fund"""
    FILE_PATH = "./funds/fund_data.csv"
    df = pd.read_csv(FILE_PATH, header=0)
    return df
