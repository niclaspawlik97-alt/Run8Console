import helper.parser_json
import helper.parser_train_symbols
import helper.parser_industry_tags
import gspread
import pandas as pd
import sys


if __name__ == "__main__":

    search_classes = sys.argv[1:]

    df_trains = helper.parser_train_symbols.find_by_classes(search_classes)

    results = []
    not_found = []  # (symbol, cls) Tupel

    for _, row in df_trains.iterrows():
        symbol = row['BASE_TRAIN_SYMBOL']
        for cls in row['CLASS_BLOCKS_LIST']:
            if cls in search_classes:
                yard = helper.parser_industry_tags.get_yard_by_tag(cls)
                if yard is None:
                    if cls not in [x[1] for x in not_found]:
                        not_found.append((symbol, cls))
                else:
                    print(f"Symbol: {symbol} | Class: {cls} | Yard: {yard}")
                    results.append({
                        'SYMBOL': symbol,
                        'CLASS': cls,
                        'YARD': yard
                    })

    # Classes ohne Train-Match
    for cls in search_classes:
        if cls not in [r['CLASS'] for r in results] and cls not in [x[1] for x in not_found]:
            not_found.append(('', cls))

    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("RUN8")

    # Results Sheet
    if results:
        df_export = pd.DataFrame(results)
        worksheet_results = sh.worksheet("ClassToYard")
        worksheet_results.clear()
        worksheet_results.update([df_export.columns.tolist()] + df_export.values.tolist())
        print("Erfolgreich in Google Sheet geschrieben.")

    # Nicht gefundene Classes in "Industry Tag Vervollständigen"
    if not_found:
        worksheet_missing = sh.worksheet("Industry Tag Vervollständigen")
        existing = worksheet_missing.get_all_records()
        existing_classes = [row['Class'] for row in existing]

        new_rows = [
            [symbol, cls, "Kein Industry Tag gefunden"]
            for symbol, cls in not_found
            if cls not in existing_classes
        ]

        if new_rows:
            worksheet_missing.append_rows(new_rows)
            print(f"{len(new_rows)} neue Einträge in 'Industry Tag Vervollständigen' geschrieben.")
        else:
            print("Keine neuen Einträge — alle bereits vorhanden.")

        print(f"\nNicht gefunden: {', '.join([cls for _, cls in not_found])}")