import helper.parser_json
import helper.parser_train_symbols
import helper.parser_industry_tags
import gspread
import pandas as pd   


if __name__ == "__main__":

    search_classes = ["VUL", "OMY", "MCC", "SPM"]

    df_trains = helper.parser_train_symbols.find_by_classes(search_classes)

    results = []
    for _, row in df_trains.iterrows():
        symbol = row['BASE_TRAIN_SYMBOL']
        for cls in row['CLASS_BLOCKS_LIST']:
            if cls in search_classes:
                yard = helper.parser_industry_tags.get_yard_by_tag(cls)
                print(f"Symbol: {symbol} | Class: {cls} | Yard: {yard}")
                results.append({
                    'SYMBOL': symbol,
                    'CLASS': cls,
                    'YARD': yard
                })

    df_export = pd.DataFrame(results)

    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("RUN8")
    worksheet = sh.worksheet("ClassToYard")

    worksheet.clear()
    worksheet.update([df_export.columns.tolist()] + df_export.values.tolist())

    print("Erfolgreich in Google Sheet geschrieben.")