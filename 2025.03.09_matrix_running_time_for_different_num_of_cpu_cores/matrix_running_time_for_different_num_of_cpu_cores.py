"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45324
"""

import numpy as np
import time

n = 5000
A = np.random.rand(n, n)
B = np.random.rand(n, n)

test_times = 20

# 矩阵行列式
start_time = time.time()
for _ in range(test_times):
    det_A = np.linalg.det(A)
det_time = (time.time() - start_time)/test_times
print(f"矩阵行列式时间: {det_time:.3f} 秒")

# 矩阵乘法
start_time = time.time()
for _ in range(test_times):
    C = np.dot(A, B)
multiply_time = (time.time() - start_time)/test_times
print(f"矩阵乘法时间: {multiply_time:.3f} 秒")

# 矩阵求逆
start_time = time.time()
for _ in range(test_times):
    inv_A = np.linalg.inv(A)
inv_time = (time.time() - start_time)/test_times
print(f"矩阵求逆时间: {inv_time:.3f} 秒")

# 矩阵的秩
start_time = time.time()
for _ in range(test_times):
    rank_A = np.linalg.matrix_rank(A)
rank_time = (time.time() - start_time)/test_times
print(f"矩阵的秩时间: {rank_time:.3f} 秒")

# 矩阵的特征值
start_time = time.time()
for _ in range(test_times):
    eigenvalues_A = np.linalg.eigvals(A)
eigen_time = (time.time() - start_time)/test_times
print(f"矩阵特征值时间: {eigen_time:.3f} 秒")

# 矩阵的特征值和特征向量
start_time = time.time()
for _ in range(test_times):
    eigenvalues_A, eigenvector_A = np.linalg.eig(A)
eigen_time = (time.time() - start_time)/test_times
print(f"矩阵特征值和特征向量时间: {eigen_time:.3f} 秒")