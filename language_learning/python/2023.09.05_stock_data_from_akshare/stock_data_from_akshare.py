"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/35979
"""

import guan

print(guan.find_stock_name_from_symbol(symbol='000002'), '\n')
title, stock_data = guan.history_data_of_one_stock(symbol='000002', period='daily')
print(title, '\n')
print(stock_data[0])

# 日线
plt, fig, ax = guan.import_plt_and_start_fig_ax()
guan.plot_without_starting_fig(plt, fig, ax, stock_data[:, 0], stock_data[:, 2], style='-')

# 月线
title, stock_data = guan.history_data_of_one_stock(symbol='000002', period='monthly')
guan.plot_without_starting_fig(plt, fig, ax, stock_data[:, 0], stock_data[:, 2], style='or-')

guan.plot_without_starting_fig(plt, fig, ax, [], [], xlabel='Time', ylabel='Stock Price')
import datetime
ax.set_xlim(datetime.date(2017, 1, 1), datetime.date(2023, 9, 5))
plt.show()