import example
import time

def py_calculate(n):
    result = 0
    for i in range(n):
        result += i
    return result

n = 10**8

start = time.time()
py_result = py_calculate(n)
print(py_result)
py_time = time.time() - start

start = time.time()
cy_result = example.calculate(n)
print(cy_result)
cy_time = time.time() - start

print(f"Python 版本: {py_time:.6f} 秒")
print(f"Cython 版本: {cy_time:.6f} 秒")