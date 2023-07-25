import numpy as np
np.zeros((2, 3)) # 零矩阵
np.identity(3) # 单位矩阵
np.diag([1, 3, 5])  # 对角矩阵
matrix1 = np.array([[3, 5+1j], [2, 7]]) # numpy矩阵
matrix1.shape # 矩阵的维度
matrix1.transpose() # 矩阵转置
matrix1.conj() # 矩阵所有元素共轭
np.conj(matrix1) # 矩阵所有元素共轭（同上）
np.arange(1, 5, 1) # 数列（左闭右开）
np.linspace(-2, 2, 5) # 数列（左闭右闭）
np.random.uniform(-2, 2) # 随机数
np.random.randint(0, 2)  # 随机整数（左闭右开）
np.sort([1, 7, 0, 3])  # 排列
np.argsort([1, 7, 0, 3]) # 排列索引
np.linalg.det(matrix1)  # 行列式
matrix2 = np.linalg.inv(matrix1)  # 求逆
np.matmul(matrix1, matrix2) # 矩阵乘积
np.dot(matrix1, matrix2) # 矩阵乘积（同上）
eigenvalue, eigenvector = np.linalg.eig(matrix1)  # 求本征值，本征向量
matrix3 = np.append(matrix1, matrix2, axis=0) # 增加数组元素或者矩阵的行