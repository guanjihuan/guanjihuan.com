from numba import jit
import numpy as np
import time

numpy_array = np.arange(0,1e5,1)
times = 1000

def for_sum(numpy_array):
    sum = 0
    for number in numpy_array:
        sum += number
    return sum

start = time.time()
for _ in range(times):
    result = for_sum(numpy_array)
end = time.time()
print('for循环求和时间：', end - start)

start = time.time()
for _ in range(times):
    result = sum(numpy_array)
end = time.time()
print('sum()函数求和时间：', end - start)

start = time.time()
for _ in range(times):
    result = np.sum(numpy_array)
end = time.time()
print('numpy.sum()函数求和时间：', end - start)

print()

@jit
def numba_for_sum(numpy_array):
    sum = 0
    for number in numpy_array:
        sum += number
    return sum

@jit
def numba_np_sum(numpy_array):
    result = np.sum(numpy_array)
    return result

@jit(nopython=True)
def numba_nopython_np_sum(numpy_array):
    result = np.sum(numpy_array)
    return result

@jit(nopython=True, parallel=True)
def numba_nopython_parallel_np_sum(numpy_array):
    result = np.sum(numpy_array)
    return result

start = time.time()
for _ in range(times):
    result = numba_for_sum(numpy_array)
end = time.time()
print('numba + for循环求和时间：', end - start)

start = time.time()
for _ in range(times):
    result = numba_np_sum(numpy_array)
end = time.time()
print('numba + numpy.sum()函数求和时间：', end - start)

start = time.time()
for _ in range(times):
    result = numba_nopython_np_sum(numpy_array)
end = time.time()
print('numba(nopython) + numpy.sum()函数求和时间：', end - start)

start = time.time()
for _ in range(times):
    result = numba_nopython_parallel_np_sum(numpy_array)
end = time.time()
print('numba(nopython,parallel) + numpy.sum()函数求和时间：', end - start)