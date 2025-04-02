"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45966
"""

import numpy as np
import time

n_array = np.concatenate((np.arange(100, 1000, 100),
                          np.arange(1000, 10000, 1000),
                          np.arange(10000, 60000, 10000)))

for n in n_array:
    A = np.random.rand(n, n)
    start_time = time.time()
    inv_A = np.linalg.inv(A)
    inv_time = time.time() - start_time
    print(f"n = {n} 的计算时间: {inv_time:.6f} 秒")