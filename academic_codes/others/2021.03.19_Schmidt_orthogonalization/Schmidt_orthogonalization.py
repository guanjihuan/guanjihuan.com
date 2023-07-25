"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/10890
"""

import numpy as np


def main():
    A = np.array([[0, 1, 1, -1], [1, 0, -1, 1], [1, -1, 0, 1], [-1, 1, 1, 0]])
    eigenvalue, eigenvector = np.linalg.eig(A)
    print('矩阵：\n', A)
    print('特征值:\n', eigenvalue)
    print('特征向量:\n', eigenvector)

    print('\n判断是否正交：\n', np.dot(eigenvector.transpose(), eigenvector))
    print('判断是否正交：\n', np.dot(eigenvector, eigenvector.transpose()))

    print('对角化验证：')
    print(np.dot(np.dot(eigenvector.transpose(), A), eigenvector))

    # 施密斯正交化
    eigenvector = Schmidt_orthogonalization(eigenvector)

    print('\n施密斯正交化后，特征向量：\n', eigenvector)

    print('施密斯正交化后，判断是否正交：\n', np.dot(eigenvector.transpose(), eigenvector))
    print('施密斯正交化后，判断是否正交：\n', np.dot(eigenvector, eigenvector.transpose()))

    print('施密斯正交化后，对角化验证：')
    print(np.dot(np.dot(eigenvector.transpose(), A), eigenvector))


def Schmidt_orthogonalization(eigenvector):
    num = eigenvector.shape[1]
    for i in range(num):
        for i0 in range(i):
            eigenvector[:, i] = eigenvector[:, i] - eigenvector[:, i0]*np.dot(eigenvector[:, i].transpose().conj(), eigenvector[:, i0])/(np.dot(eigenvector[:, i0].transpose().conj(),eigenvector[:, i0]))
        eigenvector[:, i] = eigenvector[:, i]/np.linalg.norm(eigenvector[:, i])
    return eigenvector


if __name__ == '__main__':
    main()