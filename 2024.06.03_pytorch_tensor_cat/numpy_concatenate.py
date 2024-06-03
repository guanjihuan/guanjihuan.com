"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/41194
"""

import numpy as np

a = np.random.rand(2, 3)
b = np.random.rand(2, 3)

# 第一维度的数据合并（需要其他的维度保持一致）
concatenated_1 = np.concatenate((a, b), axis=0)
print(concatenated_1.shape)

# 第二维度的数据合并（需要其他的维度保持一致）
concatenated_2 = np.concatenate((a, b), axis=1)
print(concatenated_2.shape)