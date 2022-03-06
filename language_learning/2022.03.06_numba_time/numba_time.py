import numpy as np
from numba import jit
import time

def for_sum(numpy_array):
    sum = 0
    for number in numpy_array:
        sum += number
    return sum

@jit
def numba_for_sum(numpy_array):
    sum = 0
    for number in numpy_array:
        sum += number
    return sum

numpy_array = np.arange(0,1e8,1)

start = time.time()
result = sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('python中sum()函数求和时间：\n', end - start)

start = time.time()
result = np.sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('numpy.sum()函数求和时间：\n', end - start)

start = time.time()
result = for_sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('for循环求和numpy数组的时间：\n', end - start)

start = time.time()
result = numba_for_sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('numba加速for循环求和numpy数组的时间：\n', end - start, '\n')