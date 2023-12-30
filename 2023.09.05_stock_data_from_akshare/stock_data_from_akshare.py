"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/35979
"""

import guan

title, stock_data = guan.history_data_of_one_stock(symbol='000002', period='daily')
print(title)
print(stock_data[0])
num = 30
date_array = stock_data[0:num, 0]
opening_array = stock_data[0:num, 1]
closing_array = stock_data[0:num, 2]
high_array = stock_data[0:num, 3]
low_array = stock_data[0:num, 4]
guan.plot(date_array, closing_array, style='o-', xlabel='date', ylabel='price')
guan.plot_stock_line(date_array, opening_array, closing_array, high_array, low_array)