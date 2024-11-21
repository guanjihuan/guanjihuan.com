"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/43508
"""

import numpy as np
import matplotlib.pyplot as plt

investment_ratio_array = np.arange(0.1, 1.1, 0.1)
investment_times = 1000
test_times = 100

# 几个例子：https://www.guanjihuan.com/archives/43412

# 例子（2）的参数
p = 0.6 # 胜率
b = 1 # 收益
a = 1 # 损失

# # 例子（3）的参数
# p = 0.5
# b = 1
# a = 0.5

win_array = [] # 胜出的仓位
for i0 in range(test_times):
    # print(i0)
    capital_array = []
    for f in investment_ratio_array:
        capital = 1
        for _ in range(investment_times):
            investment = capital*f
            if investment>0:
                random_value = np.random.uniform(0, 1)
                if random_value<p:
                    capital = capital+investment*b
                else:
                    capital = capital-investment*a
        capital_array.append(capital)
    max_capital_index = capital_array.index(max(capital_array))
    win_array.append(investment_ratio_array[max_capital_index])

def kelly_formula(p, b, a):
    f=(p/a)-((1-p)/b)
    return f

print(kelly_formula(p=p, b=b, a=a))
plt.hist(win_array, bins=100, color='skyblue')
plt.show()