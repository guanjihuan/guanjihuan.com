from numba import jit
import numpy as np
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

numpy_array = np.arange(0,2e8,1)

start = time.time()
result = sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('python中sum()函数求和时间：', end - start)

start = time.time()
result = np.sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('numpy.sum()函数求和时间：', end - start)

start = time.time()
result = for_sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('for循环求和numpy数组的时间：', end - start)

start = time.time()
result = numba_for_sum(numpy_array)
end = time.time()
print('\nresult:', result)
print('numba加速for循环求和numpy数组的时间：', end - start, '\n')