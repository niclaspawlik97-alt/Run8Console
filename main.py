import helper.parser_json
import helper.parser_train_symbols
import helper.parser_industry_tags
import pandas as pd   


if __name__ == "__main__":

    df_start = helper.parser_json.sort_origin('Barstow, CA')
    df_end = helper.parser_json.sort_dest('Barstow, CA')

    df_train_symbols = helper.parser_train_symbols.sort_dest('Barstow Yard')

    #df_train_symbols.to_json('barstow_train_symbols.json', orient='records', indent=4)

    df_search_yard = helper.parser_industry_tags.get_yard_by_tag('CAN')

    #print(df_start)
    #print(df_end)

    #print(df_train_symbols)

    print(df_search_yard)
