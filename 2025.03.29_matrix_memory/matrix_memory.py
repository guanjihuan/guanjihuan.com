"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45873
"""

import numpy as np
import sys

n_array = np.concatenate((np.arange(1, 10, 1),
                          np.arange(10, 100, 10),
                          np.arange(100, 1000, 100),
                          np.arange(1000, 10000, 1000),
                          np.arange(10000, 100000, 10000),
                          np.arange(100000, 1000000, 100000)))

for n in n_array:
    matrix = np.zeros((n, n))  # 双精度浮点数 float64 一个数据占用 8B
    # matrix = np.zeros((n, n), dtype=complex) # 双精度复数  complex128  一个数据占用 16B
    # matrix = np.zeros((n, n),  dtype=np.float32) # 单精度浮点数 float32  一个数据占用 4B
    # matrix = np.zeros((n, n), dtype=int) # 整数 int32 一个数据占用 4B
    if n==1:
        print(type(matrix[0, 0]), '\n')
    size0 = matrix.nbytes # 矩阵数据内存占用
    size = sys.getsizeof(matrix) # 矩阵总的内存占用
    print(f'矩阵 N={n}')
    if size<1024:
        print(f'数据内存占用: {size0:.2f} B')
        print(f'总的内存占用: {size:.2f} B')
    elif 1024<size<1024*1024:
        print(f'数据内存占用: {size0/1024:.2f} KB')
        print(f'总的内存占用: {size/1024:.2f} KB')
    elif 1024*1024<size<1024*1024*1024:
        print(f'数据内存占用: {size0/(1024*1024):.2f} MB')
        print(f'总的内存占用: {size/(1024*1024):.2f} MB')
    elif 1024*1024*1024<size<1024*1024*1024*1024:
        print(f'数据内存占用: {size0/(1024*1024*1024):.2f} GB')
        print(f'总的内存占用: {size/(1024*1024*1024):.2f} GB')
    else:
        print(f'数据内存占用: {size0/(1024*1024*1024*1024):.2f} TB')
        print(f'总的内存占用: {size/(1024*1024*1024*1024):.2f} TB')
    print()