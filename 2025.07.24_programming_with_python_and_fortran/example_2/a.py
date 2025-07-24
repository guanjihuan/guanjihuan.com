import example

matrix = [[1, 2], [3, 4]]
print(example.sum_matrix(matrix))

print('---')

# 时间对比

import numpy as np
import time

matrix = np.random.rand(5000, 5000)

start = time.time()
print(example.sum_matrix(matrix))
end = time.time()
print('Python + Fortran 循环求和时间：', end - start)

start = time.time()
sum_result = 0
for i0 in range(matrix.shape[0]):
    for j0 in range(matrix.shape[1]):
        sum_result += matrix[i0, j0]
print(sum_result)
end = time.time()
print('Python 循环求和时间：', end - start)

from numba import jit
@jit
def numba_for_sum_matrix(matrix):
    sum_result = 0
    for i0 in range(matrix.shape[0]):
        for j0 in range(matrix.shape[1]):
            sum_result += matrix[i0, j0]
    return sum_result

start = time.time()
print(numba_for_sum_matrix(matrix))
end = time.time()
print('Python numba 循环求和时间：', end - start)

start = time.time()
print(np.sum(matrix))
end = time.time()
print('Python numpy.sum() 求和时间：', end - start)