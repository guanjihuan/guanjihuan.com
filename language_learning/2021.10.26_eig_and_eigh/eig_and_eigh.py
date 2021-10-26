"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/17789
"""

import numpy as np

def hamiltonian(width=2, length=2):
    h00 = np.zeros((width*length, width*length))
    for i0 in range(length):
        for j0 in range(width-1):
            h00[i0*width+j0, i0*width+j0+1] = 1
            h00[i0*width+j0+1, i0*width+j0] = 1
    for i0 in range(length-1):
        for j0 in range(width):
            h00[i0*width+j0, (i0+1)*width+j0] = 1
            h00[(i0+1)*width+j0, i0*width+j0] = 1
    return h00

print('矩阵：\n', hamiltonian(), '\n')

eigenvalue, eigenvector = np.linalg.eig(hamiltonian())
print('eig求解特征值：', eigenvalue)
print('eig求解特征向量：\n',eigenvector)
print('判断特征向量是否正交：\n', np.dot(eigenvector.transpose(), eigenvector))

print()

eigenvalue, eigenvector = np.linalg.eigh(hamiltonian())
print('eigh求解特征值：', eigenvalue)
print('eigh求解特征向量：\n',eigenvector)
print('判断特征向量是否正交：\n', np.dot(eigenvector.transpose(), eigenvector))