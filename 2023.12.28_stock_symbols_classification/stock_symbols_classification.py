"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38180
"""

import akshare as ak
import re

stocks = ak.stock_zh_a_spot_em()
stock_data = stocks.values
stock_symbols = stock_data[:, 1]
num_stocks = len(stock_symbols)
print('所有股票数量：', num_stocks)
# print(stock_symbols)

# 上交所主板
stock_symbols_60 = []
for stock_symbol in stock_symbols:
    find_600 = re.findall(r'^600', stock_symbol)
    find_601 = re.findall(r'^601', stock_symbol)
    find_603 = re.findall(r'^603', stock_symbol)
    find_605 = re.findall(r'^605', stock_symbol)
    if find_600 != [] or find_601 != [] or find_603 != [] or find_605 != []:
        stock_symbols_60.append(stock_symbol)
num_stocks_60 = len(stock_symbols_60)
print('上交所主板股票数量：', num_stocks_60)
# print(stock_symbols_60)

# 深交所主板
stock_symbols_00 = []
for stock_symbol in stock_symbols:
    find_000 = re.findall(r'^000', stock_symbol)
    find_001 = re.findall(r'^001', stock_symbol)
    find_002 = re.findall(r'^002', stock_symbol)
    find_003 = re.findall(r'^003', stock_symbol)
    if find_000 != [] or find_001 != [] or find_002 != [] or find_003 != []:
        stock_symbols_00.append(stock_symbol)
num_stocks_00 = len(stock_symbols_00)
print('深交所主板股票数量：', num_stocks_00)
# print(stock_symbols_00)

# 创业板
stock_symbols_30 = []
for stock_symbol in stock_symbols:
    find_300 = re.findall(r'^300', stock_symbol)
    find_301 = re.findall(r'^301', stock_symbol)
    find_302 = re.findall(r'^302', stock_symbol)
    if find_300 != [] or find_301 != [] or find_302 != []:
        stock_symbols_30.append(stock_symbol)
num_stocks_30 = len(stock_symbols_30)
print('创业板股票数量：', num_stocks_30)
# print(stock_symbols_30)

# 科创板
stock_symbols_68 = []
for stock_symbol in stock_symbols:
    find_688 = re.findall(r'^688', stock_symbol)
    find_689 = re.findall(r'^689', stock_symbol)
    if find_688 != [] or find_689 != []:
        stock_symbols_68.append(stock_symbol)
num_stocks_68= len(stock_symbols_68)
print('科创板股票数量：', num_stocks_68)
# print(stock_symbols_68)

# 北交所和新三板
stock_symbols_8_4_9 = []
for stock_symbol in stock_symbols:
    find_83 = re.findall(r'^83', stock_symbol)
    find_87 = re.findall(r'^87', stock_symbol)
    find_430 = re.findall(r'^430', stock_symbol)
    find_420 = re.findall(r'^420', stock_symbol)
    find_400 = re.findall(r'^400', stock_symbol)
    find_920 = re.findall(r'^920', stock_symbol)
    if find_83 != [] or find_87 != [] or find_430 != [] or find_420 != [] or find_400 != [] or find_920 != []:
        stock_symbols_8_4_9.append(stock_symbol)
num_stocks_8_4_9= len(stock_symbols_8_4_9)
print('北交所和新三板股票数量：', num_stocks_8_4_9)
# print(stock_symbols_8_4)

print('所有股票数量：', num_stocks_60+num_stocks_00+num_stocks_30+num_stocks_68+num_stocks_8_4_9)

# 检查遗漏的股票代码
for stock_symbol in stock_symbols:
    if stock_symbol not in stock_symbols_60 and stock_symbol not in stock_symbols_00 and stock_symbol not in stock_symbols_30 and stock_symbol not in stock_symbols_68 and stock_symbol not in stock_symbols_8_4_9:
        print(stock_symbol)