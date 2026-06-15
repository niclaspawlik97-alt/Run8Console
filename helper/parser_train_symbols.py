import json
import pandas as pd


train_symbol_json = 'C:\\Users\\nicla\\AppData\\Local\\RailCoder\\YARDS\\YardConfigurations\\SouthernCA_BNSF_Barstow_TrainProfiles.json'

def create_dataframe():
    df = pd.read_json(train_symbol_json)

    return df

def sort_dest(_destination):
    df = create_dataframe()
    destination = df[df['DEST_CITY_STATE'] == _destination]

    return destination
