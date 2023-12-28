"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38193
"""

import akshare as ak
import numpy as np
stocks = ak.stock_zh_a_spot_em()
stock_data = stocks.values
list_index = np.argsort(stock_data[:, 17])
list_index = list_index[::-1]
for i0 in range(30):
    stock_symbol = stock_data[list_index[i0], 1]
    stock_name = stock_data[list_index[i0], 2]
    market_capitalization = stock_data[list_index[i0], 17]/1e8
    print([i0+1, stock_symbol, stock_name, market_capitalization])