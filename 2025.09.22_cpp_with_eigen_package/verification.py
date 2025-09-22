import numpy as np
A = np.array([
    [2, 1, 1, 0],
    [1, 3, 1, 1],
    [1, 1, 4, 1],
    [0, 1, 1, 5]
])
A_inv = np.linalg.inv(A)
print("A_inv:\n", A_inv)