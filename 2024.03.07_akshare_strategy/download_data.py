import guan
stock_symbols_60, stock_symbols_00, stock_symbols_30, stock_symbols_68, \
stock_symbols_8_4,stock_symbols_others = guan.stock_symbols_classification()

import os
guan.make_directory('./all_to_2024_03_07')

guan.make_directory('./all_to_2024_03_07/stock_data_60')
for stock_symbol in stock_symbols_60:
    try:
        if not os.path.exists('./all_to_2024_03_07/stock_data_60/'+stock_symbol+'.txt'):
            title, stock_data = guan.history_data_of_one_stock(symbol=stock_symbol, \
                                period='daily', start_date="19000101", end_date='21000101')
            guan.dump_data(data=stock_data, filename='./all_to_2024_03_07/stock_data_60/'+stock_symbol, file_format='.txt')
    except:
        pass
print('60下载完成')

guan.make_directory('./all_to_2024_03_07/stock_data_00')
for stock_symbol in stock_symbols_00:
    try:
        if not os.path.exists('./all_to_2024_03_07/stock_data_00/'+stock_symbol+'.txt'):
            title, stock_data = guan.history_data_of_one_stock(symbol=stock_symbol, \
                                period='daily', start_date="19000101", end_date='21000101')
            guan.dump_data(data=stock_data, filename='./all_to_2024_03_07/stock_data_00/'+stock_symbol, file_format='.txt')
    except:
        pass
print('00下载完成')