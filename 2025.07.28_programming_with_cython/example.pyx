def calculate(int n):
    cdef int i

    cdef long long result = 0
    # cdef int result = 0  # 这个类型在数值比较大的时候会溢出，结果不正确。
    # result = 0  # 这个不声明类型，使用 Python 的 int，Python 的整数是任意精度的，不会溢出，但性能会比 C 类型低。

    for i in range(n):
        result += i
        
    return result