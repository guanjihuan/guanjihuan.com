"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/10890
"""

import numpy as np

a = [[ 0 , 0  ,  1.5 ,  0.32635182-0.98480775j],
 [0  ,   0  , -0.32635182-0.98480775j, 1.5  ],
 [ 1.5 ,    -0.32635182+0.98480775j ,0, 0 ],
 [ 0.32635182+0.98480775j , 1.5 ,  0, 0 ]]

def Schmidt_orthogonalization(eigenvector):
    num = eigenvector.shape[1]
    for i in range(num):
        for i0 in range(i):
            eigenvector[:, i] = eigenvector[:, i] - eigenvector[:, i0]*np.dot(eigenvector[:, i].transpose().conj(), eigenvector[:, i0])/(np.dot(eigenvector[:, i0].transpose().conj(),eigenvector[:, i0]))
        eigenvector[:, i] = eigenvector[:, i]/np.linalg.norm(eigenvector[:, i])
    return eigenvector

def verify_orthogonality(vectors):
    identity = np.eye(vectors.shape[1])
    product = np.dot(vectors.T.conj(), vectors)
    return np.allclose(product, identity)

# 对 np.linalg.eigh() 的特征向量正交化

E, v = np.linalg.eigh(a)
print(verify_orthogonality(v))

v1 = Schmidt_orthogonalization(v)
print(verify_orthogonality(v1))

from scipy.linalg import orth
v2 = orth(v)
print(verify_orthogonality(v2))

v3, S, Vt = np.linalg.svd(v)
print(verify_orthogonality(v3))

v4, R = np.linalg.qr(v)
print(verify_orthogonality(v4))

print()


# 对 np.linalg.eig() 的特征向量正交化

E, v = np.linalg.eig(a)
print(verify_orthogonality(v))

v1 = Schmidt_orthogonalization(v)
print(verify_orthogonality(v1))

from scipy.linalg import orth
v2 = orth(v)
print(verify_orthogonality(v2))

v3, S, Vt = np.linalg.svd(v)
print(verify_orthogonality(v3))

v4, R = np.linalg.qr(v)
print(verify_orthogonality(v4))