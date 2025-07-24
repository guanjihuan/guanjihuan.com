import numpy as np
import example

A = [[1.0, 2.0, 3.0],
    [0.0, 1.0, 4.0],
    [5.0, 6.0, 0.0]]

Ainv_1 = np.asfortranarray(np.empty_like(A))
example.inverse_matrix(A, Ainv_1) # 调用 Fortran 子程序
print(Ainv_1)

Ainv_2 = np.linalg.inv(A)
print(Ainv_2)

print('---')

# 时间对比

A = np.random.rand(3000, 3000)

import time
start = time.time()
Ainv_1 = np.asfortranarray(np.empty_like(A))
example.inverse_matrix(A, Ainv_1) # 调用 Fortran 子程序
end = time.time()
print('Python + Fortran 求逆时间：', end - start)

start = time.time()
Ainv_2 = np.linalg.inv(A)
end = time.time()
print('Python np.linalg.inv() 求逆时间：', end - start)