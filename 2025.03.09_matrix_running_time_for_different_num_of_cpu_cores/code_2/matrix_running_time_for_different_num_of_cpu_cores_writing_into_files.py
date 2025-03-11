"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45324
"""

import numpy as np
import time
import pickle

n = 1000

A = np.random.rand(n, n)
B = np.random.rand(n, n)

test_times = 20

# 矩阵乘法
start_time = time.time()
for _ in range(test_times):
    C = np.dot(A, B)
multiply_time = (time.time() - start_time)/test_times
with open(f'multiply_time_n={n}.pkl', 'wb') as f:
    pickle.dump(multiply_time, f)

# 矩阵求逆
start_time = time.time()
for _ in range(test_times):
    inv_A = np.linalg.inv(A)
inv_time = (time.time() - start_time)/test_times
with open(f'inv_time_n={n}.pkl', 'wb') as f:
    pickle.dump(inv_time, f)

# 矩阵的特征值和特征向量
start_time = time.time()
for _ in range(test_times):
    eigenvalues_A, eigenvector_A = np.linalg.eig(A)
eigen_time = (time.time() - start_time)/test_times
with open(f'eigen_time_n={n}.pkl', 'wb') as f:
    pickle.dump(eigen_time, f)