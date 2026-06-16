import json
import gspread
import pandas as pd

def create_dataframe():
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("RUN8")
    worksheet = sh.worksheet('Industry Tags')

    data = worksheet.get_all_records()

    df = pd.DataFrame(data)

    return df

def get_yard_by_tag(tag_name):
    df = create_dataframe()

    result = df[df['Tag'] == tag_name]
    
    if not result.empty:
        return result['Served By Yard'].values[0]
    else:
        return None


