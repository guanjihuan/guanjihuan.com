"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/1247
"""

import random
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


def function(x):  # 期望样品的分布，target distribution function
    y = (norm.pdf(x, loc=2, scale=1)+norm.pdf(x, loc=-5, scale=1.5))/2   # loc代表了均值,scale代表标准差
    return y


T = 100000  # 取T个样品
pi = [0 for i in range(T)]  # 任意选定一个马尔科夫链初始状态
for t in np.arange(1, T):
    pi_star = np.random.uniform(-10, 10)  # a proposed distribution， 例如是均匀分布的，或者是一个依赖pi[t - 1]的分布
    alpha = min(1, (function(pi_star) / function(pi[t - 1])))  # 接收率
    u = random.uniform(0, 1)
    if u < alpha:
        pi[t] = pi_star    # 以alpha的概率接收转移
    else:
        pi[t] = pi[t - 1]  # 不接收转移

pi = np.array(pi)  # 转成numpy格式
print(pi.shape)  # 查看抽样样品的维度
plt.plot(pi, function(pi), '*')  # 画出抽样样品期望的分布   # 或用plt.scatter(pi, function(pi))
plt.hist(pi, bins=100, density=1, facecolor='red', alpha=0.7)   # 画出抽样样品的分布   # bins是分布柱子的个数，density是归一化，后面两个参数是管颜色的
plt.show()
