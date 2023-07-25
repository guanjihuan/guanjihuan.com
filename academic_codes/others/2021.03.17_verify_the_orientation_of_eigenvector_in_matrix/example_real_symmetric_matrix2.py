import numpy as np

A = np.array([[0, 1, 1, -1], [1, 0, -1, 1], [1, -1, 0, 1], [-1, 1, 1, 0]])
eigenvalue, eigenvector = np.linalg.eig(A)
print('矩阵：\n', A)
print('特征值:\n', eigenvalue)
print('特征向量:\n', eigenvector)

print('\n判断是否正交：\n', np.dot(eigenvector.transpose(), eigenvector))
print('判断是否正交：\n', np.dot(eigenvector, eigenvector.transpose()))

print('特征向量矩阵的列向量模方和：')
for i in range(4):
    print(eigenvector[0, i]**2+eigenvector[1, i]**2+eigenvector[2, i]**2+eigenvector[3, i]**2)
print('特征向量矩阵的行向量模方和：')
for i in range(4):
    print(eigenvector[i, 0]**2+eigenvector[i, 1]**2+eigenvector[i, 2]**2+eigenvector[i, 3]**2)

print('\n对角化验证：')
print(np.dot(np.dot(eigenvector.transpose(), A), eigenvector))
print(np.dot(np.dot(eigenvector, A), eigenvector.transpose()))

print('\n特征向量理论值:')
T = np.array([[1/np.sqrt(2), 1/np.sqrt(6), -1/np.sqrt(12), 1/2], [1/np.sqrt(2), -1/np.sqrt(6), 1/np.sqrt(12), -1/2], [0, 2/np.sqrt(6), 1/np.sqrt(12), -1/2], [0, 0, 3/np.sqrt(12), 1/2]])
print(T)

print('\n判断是否正交：\n', np.dot(T.transpose(), T))
print('判断是否正交：\n', np.dot(T, T.transpose()))

print('\n对角化验证：')
print(np.dot(np.dot(T.transpose(), A), T))
print(np.dot(np.dot(T, A), T.transpose()))