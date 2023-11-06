import numpy as np

A = np.array([[3, 2, -1], [-2, -2, 2], [3, 6, -1]])
eigenvalue, eigenvector = np.linalg.eig(A)
print('矩阵：\n', A)
print('特征值:\n', eigenvalue)
print('特征向量:\n', eigenvector)
print('特征值为-4对应的特征向量理论值:\n', np.array([1/3, -2/3, 1])/np.sqrt((1/3)**2+(-2/3)**2+1**2))

print('\n判断是否正交：\n', np.dot(eigenvector.transpose(), eigenvector))
print('判断是否正交：\n', np.dot(eigenvector, eigenvector.transpose()))

print('特征向量矩阵的列向量模方和：')
for i in range(3):
    print(eigenvector[0, i]**2+eigenvector[1, i]**2+eigenvector[2, i]**2)
print('特征向量矩阵的行向量模方和：')
for i in range(3):
    print(eigenvector[i, 0]**2+eigenvector[i, 1]**2+eigenvector[i, 2]**2)