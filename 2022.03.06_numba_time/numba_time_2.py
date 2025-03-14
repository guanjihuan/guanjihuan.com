from numba import jit
from numba import prange
import time
import numpy as np

numpy_array = np.arange(0,1e5,1)
times = 1000

def for_sum(numpy_array):
    sum = 0
    for number in numpy_array:
        sum += number
    return sum

@jit
def numba_for_sum_1(numpy_array):
    sum = 0
    for number in numpy_array:
        sum += number
    return sum

@jit(nopython=True)
def numba_for_sum_2(numpy_array):
    sum = 0
    for number in numpy_array:
        sum += number
    return sum

@jit(nopython=True, parallel=True)
def numba_for_sum_3(numpy_array):
    sum = 0
    for i in prange(len(numpy_array)):
        sum += numpy_array[i]
    return sum

start = time.time()
for _ in range(times):
    result = for_sum(numpy_array)
end = time.time()
print('for循环时间：', end - start)

start = time.time()
for _ in range(times):
    result = numba_for_sum_1(numpy_array)
end = time.time()
print('@jit时间：', end - start)

start = time.time()
for _ in range(times):
    result = numba_for_sum_2(numpy_array)
end = time.time()
print('@jit(nopython=True)时间：', end - start)

start = time.time()
for _ in range(times):
    result = numba_for_sum_3(numpy_array)
end = time.time()
print('@jit(nopython=True, parallel=True)时间：', end - start)