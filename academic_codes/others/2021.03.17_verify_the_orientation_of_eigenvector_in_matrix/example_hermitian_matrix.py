import numpy as np

A = np.array([[3, 2+1j, -1], [2-1j, -2, 6], [-1, 6, 1]])
eigenvalue, eigenvector = np.linalg.eig(A)
print('矩阵：\n', A)
print('特征值:\n', eigenvalue)
print('特征向量:\n', eigenvector)

print('\n判断是否正交：\n', np.dot(eigenvector.transpose().conj(), eigenvector))
print('判断是否正交：\n', np.dot(eigenvector, eigenvector.transpose().conj()))

print('特征向量矩阵的列向量模方和：')
for i in range(3):
    print(np.abs(eigenvector[0, i])**2+np.abs(eigenvector[1, i])**2+np.abs(eigenvector[2, i])**2)
print('特征向量矩阵的行向量模方和：')
for i in range(3):
    print(np.abs(eigenvector[i, 0])**2+np.abs(eigenvector[i, 1])**2+np.abs(eigenvector[i, 2])**2)

print('\n对角化验证：')
print(np.dot(np.dot(eigenvector.transpose().conj(), A), eigenvector))
print(np.dot(np.dot(eigenvector, A), eigenvector.transpose().conj()))