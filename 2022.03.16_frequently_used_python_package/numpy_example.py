import numpy as np
print(np.zeros((2, 3)), '\n') # 零矩阵
print(np.identity(3), '\n') # 单位矩阵
print(np.diag([1, 3, 5]), '\n')  # 对角矩阵
matrix1 = np.array([[3, 5+1j], [2, 7]]) # numpy矩阵
print(matrix1, '\n')
print(matrix1.shape, '\n') # 矩阵的维度
print(matrix1.transpose(), '\n') # 矩阵转置
print(matrix1.conj(), '\n') # 矩阵所有元素共轭
print(np.conj(matrix1), '\n') # 矩阵所有元素共轭（同上）
print(np.arange(1, 5, 1), '\n') # 数列（左闭右开）
print(np.linspace(-2, 2, 5), '\n') # 数列（左闭右闭）
print(np.random.uniform(-2, 2), '\n') # 随机数
print(np.random.randint(0, 2), '\n')  # 随机整数（左闭右开）
print(np.sort([1, 7, 0, 3]), '\n') # 排列
print(np.argsort([1, 7, 0, 3]), '\n') # 排列索引
print(np.linalg.det(matrix1), '\n')   # 行列式
matrix2 = np.linalg.inv(matrix1)  # 求逆
print(matrix2, '\n')
print(np.matmul(matrix1, matrix2), '\n') # 矩阵乘积
print(np.dot(matrix1, matrix2), '\n') # 矩阵乘积（同上）
eigenvalue, eigenvector = np.linalg.eig(matrix1)  # 求本征值，本征向量
print(eigenvalue, '\n')
print(eigenvector, '\n')
matrix3 = np.append(matrix1, matrix2, axis=0) # 增加数组元素或者矩阵的行
print(matrix3)