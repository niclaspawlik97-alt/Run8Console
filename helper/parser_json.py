import json
import gspread
import pandas as pd


def create_dataframe():
    # 1. Verbindung über die JSON-Datei herstellen
    gc = gspread.service_account(filename='credentials.json')

    # 2. Google-Tabelle öffnen (Nutzen Sie den exakten Namen Ihrer Datei)
    sh = gc.open("RUN8")
    # Das erste Tabellenblatt auswählen
    worksheet = sh.sheet1

    data = worksheet.get_all_records()

    df = pd.DataFrame(data)

    return df

def sort_origin(_origin):
    df = create_dataframe()
    origin = df[df['Origin'] == _origin]

    return origin

def sort_dest(_destination):
    df = create_dataframe()
    destination = df[df['Destination'] == _destination]

    return destination