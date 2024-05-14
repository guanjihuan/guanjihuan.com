def addition_time():
    import time
    start_time = time.time()
    result = 0.0
    for _ in range(int(1e9)):
        result += 1e-9
    end_time = time.time()
    return end_time - start_time
execution_time = addition_time()
print("Execution time 0:", execution_time)

def np_dot_time():
    import numpy as np
    import time
    start_time = time.time()
    matrix_size = 10
    for _ in range(int(1e7)):
        matrix1 = np.random.rand(matrix_size, matrix_size)
        matrix2 = np.random.rand(matrix_size, matrix_size)
        result_matrix = np.dot(matrix1, matrix2)
    end_time = time.time()
    return end_time - start_time
execution_time = np_dot_time()
print("Execution time 1:", execution_time)

def np_dot_time_2():
    import numpy as np
    import time
    start_time = time.time()
    matrix_size = 1000
    for _ in range(int(1e3)):
        matrix1 = np.random.rand(matrix_size, matrix_size)
        matrix2 = np.random.rand(matrix_size, matrix_size)
        result_matrix = np.dot(matrix1, matrix2)
    end_time = time.time()
    return end_time - start_time
execution_time = np_dot_time_2()
print("Execution time 2:", execution_time)

def np_dot_time_3():
    import numpy as np
    import time
    start_time = time.time()
    matrix_size = 10000
    for _ in range(1):
        matrix1 = np.random.rand(matrix_size, matrix_size)
        matrix2 = np.random.rand(matrix_size, matrix_size)
        result_matrix = np.dot(matrix1, matrix2)
    end_time = time.time()
    return end_time - start_time
execution_time = np_dot_time_3()
print("Execution time 3:", execution_time)