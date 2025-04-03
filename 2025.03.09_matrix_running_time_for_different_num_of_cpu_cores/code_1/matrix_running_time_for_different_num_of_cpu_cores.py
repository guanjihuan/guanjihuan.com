"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45324
"""

import numpy as np
import time

n = 1000
test_times = 20

# 矩阵乘法
start_time = time.time()
for _ in range(test_times):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.dot(A, B)
multiply_time = (time.time() - start_time)/test_times
print(f"矩阵乘法时间: {multiply_time:.3f} 秒")

# 矩阵求逆
start_time = time.time()
for _ in range(test_times):
    A = np.random.rand(n, n)
    inv_A = np.linalg.inv(A)
inv_time = (time.time() - start_time)/test_times
print(f"矩阵求逆时间: {inv_time:.3f} 秒")

# 矩阵的特征值和特征向量
start_time = time.time()
for _ in range(test_times):
    A = np.random.rand(n, n)
    eigenvalues_A, eigenvector_A = np.linalg.eig(A)
eigen_time = (time.time() - start_time)/test_times
print(f"矩阵特征值和特征向量时间: {eigen_time:.3f} 秒")