import numpy as np
import time

numpy_array = np.arange(0,1e5,1)
times = 1000

from numba import jit
from numba import prange
@jit(nopython=True, parallel=True)
def numba_example(numpy_array):
    sum = 0
    for i in prange(len(numpy_array)):
        sum += numpy_array[i]
    return sum

start = time.time()
for _ in range(times):
    result = numba_example(numpy_array)
end = time.time()
print(f'运行时间：{end - start}')