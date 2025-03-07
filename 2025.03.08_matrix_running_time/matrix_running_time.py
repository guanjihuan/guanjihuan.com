"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45275
"""

import numpy as np
import time
import sys
from numba import jit

n_array = np.concatenate((np.arange(1000, 10000, 1000), np.arange(10000, 40000, 10000)))
print(f'n_array={n_array}\n')

@jit
def numba_test(C, n):
    for i0 in range(n):
        for j0 in range(n):
            C[i0, j0] = np.random.rand()
    return C

for n in n_array:
    print(f'n={n}')

    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.random.rand(n, n)

    # 矩阵占用内存
    size = sys.getsizeof(C)
    print(f'矩阵占用内存: {size/(1024*1024):.2f} MB')

    # 矩阵的迹
    start_time = time.time()
    trace_A = np.trace(A)
    trace_time = time.time() - start_time
    print(f"矩阵的迹时间: {trace_time:.3f} 秒")

    # 矩阵转置
    start_time = time.time()
    A_T = A.T
    transpose_time = time.time() - start_time
    print(f"矩阵转置时间: {transpose_time:.3f} 秒")

    # 矩阵加法
    start_time = time.time()
    C = A + B
    add_time = time.time() - start_time
    print(f"矩阵加法时间: {add_time:.3f} 秒")

    # numba for 循环赋值
    start_time = time.time()
    numba_test(C, n)
    create_time = time.time() - start_time
    print(f"numba for 循环赋值时间: {create_time:.3f} 秒")

    # 矩阵创建
    start_time = time.time()
    C = np.random.rand(n, n)
    create_time = time.time() - start_time
    print(f"矩阵创建时间: {create_time:.3f} 秒")

    # for 循环赋值
    start_time = time.time()
    for i0 in range(n):
        for j0 in range(n):
            C[i0, j0] = np.random.rand()
    create_time = time.time() - start_time
    print(f"for 循环赋值时间: {create_time:.3f} 秒")

    # 矩阵乘法
    start_time = time.time()
    C = np.dot(A, B)
    multiply_time = time.time() - start_time
    print(f"矩阵乘法时间: {multiply_time:.3f} 秒")

    # 矩阵求逆
    start_time = time.time()
    inv_A = np.linalg.inv(A)
    inv_time = time.time() - start_time
    print(f"矩阵求逆时间: {inv_time:.3f} 秒")

    # 矩阵的秩
    start_time = time.time()
    rank_A = np.linalg.matrix_rank(A)
    rank_time = time.time() - start_time
    print(f"矩阵的秩时间: {rank_time:.3f} 秒")

    # 矩阵的特征值
    start_time = time.time()
    eigenvalues_A = np.linalg.eigvals(A)
    eigen_time = time.time() - start_time
    print(f"矩阵特征值时间: {eigen_time:.3f} 秒")

    # 矩阵的特征值和特征向量
    start_time = time.time()
    eigenvalues_A, eigenvector_A = np.linalg.eig(A)
    eigen_time = time.time() - start_time
    print(f"矩阵特征值和特征向量时间: {eigen_time:.3f} 秒")

    print()