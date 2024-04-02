"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38912
"""

import guan

stock_symbols_60, stock_symbols_00, stock_symbols_30, stock_symbols_68, \
stock_symbols_8_4,stock_symbols_others = guan.stock_symbols_classification()
print(len(stock_symbols_60))
print(len(stock_symbols_00))
print()

file_list_60 = guan.get_all_filenames_in_directory(directory='./all_to_2024_03_07/stock_data_60', \
                                        file_format=None, show_root_path=0, sort=1, include_subdirectory=1)
print(len(file_list_60))
file_list_00 = guan.get_all_filenames_in_directory(directory='./all_to_2024_03_07/stock_data_00', \
                                        file_format=None, show_root_path=0, sort=1, include_subdirectory=1)
print(len(file_list_00))