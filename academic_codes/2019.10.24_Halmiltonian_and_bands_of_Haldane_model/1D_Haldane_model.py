"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/410
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *
import cmath 
import functools


def hamiltonian(k, N, M, t1, t2, phi):  # Haldane哈密顿量（N是条带的宽度参数）
    # 初始化为零矩阵
    h00 = np.zeros((4*N, 4*N), dtype=complex)
    h01 = np.zeros((4*N, 4*N), dtype=complex)

    # 原胞内的跃迁h00
    for i in range(N):
        h00[i*4+0, i*4+0] = M
        h00[i*4+1, i*4+1] = -M
        h00[i*4+2, i*4+2] = M
        h00[i*4+3, i*4+3] = -M

        # 最近邻
        h00[i*4+0, i*4+1] = t1
        h00[i*4+1, i*4+0] = t1
        h00[i*4+1, i*4+2] = t1
        h00[i*4+2, i*4+1] = t1
        h00[i*4+2, i*4+3] = t1
        h00[i*4+3, i*4+2] = t1

        # 次近邻
        h00[i*4+0, i*4+2] = t2*cmath.exp(-1j*phi)  # 逆时针为正，顺时针为负
        h00[i*4+2, i*4+0] = h00[i*4+0, i*4+2].conj()
        h00[i*4+1, i*4+3] = t2*cmath.exp(-1j*phi)
        h00[i*4+3, i*4+1] = h00[i*4+1, i*4+3].conj()
    for i in range(N-1):
        # 最近邻
        h00[i*4+3, (i+1)*4+0] = t1
        h00[(i+1)*4+0, i*4+3] = t1

        # 次近邻
        h00[i*4+2, (i+1)*4+0] = t2*cmath.exp(1j*phi)
        h00[(i+1)*4+0, i*4+2] = h00[i*4+2, (i+1)*4+0].conj()
        h00[i*4+3, (i+1)*4+1] = t2*cmath.exp(1j*phi)
        h00[(i+1)*4+1, i*4+3] = h00[i*4+3, (i+1)*4+1].conj()

    # 原胞间的跃迁h01
    for i in range(N):
        # 最近邻
        h01[i*4+1, i*4+0] = t1
        h01[i*4+2, i*4+3] = t1

        # 次近邻
        h01[i*4+0, i*4+0] = t2*cmath.exp(1j*phi)
        h01[i*4+1, i*4+1] = t2*cmath.exp(-1j*phi)
        h01[i*4+2, i*4+2] = t2*cmath.exp(1j*phi)
        h01[i*4+3, i*4+3] = t2*cmath.exp(-1j*phi)

        h01[i*4+1, i*4+3] = t2*cmath.exp(1j*phi)
        h01[i*4+2, i*4+0] = t2*cmath.exp(-1j*phi)
        if i != 0:
            h01[i*4+1, (i-1)*4+3] = t2*cmath.exp(1j*phi)
    for i in range(N-1):
        h01[i*4+2, (i+1)*4+0] = t2*cmath.exp(-1j*phi)

    matrix = h00 + h01*cmath.exp(1j*k) + h01.transpose().conj()*cmath.exp(-1j*k)
    return matrix


def main():
    hamiltonian0 = functools.partial(hamiltonian, N=40, M=2/3, t1=1, t2=1/3, phi=pi/4)
    k = np.linspace(-pi, pi, 300)
    plot_bands_one_dimension(k, hamiltonian0)


def plot_bands_one_dimension(k, hamiltonian):
    dim = hamiltonian(0).shape[0]
    dim_k = k.shape[0]
    eigenvalue_k = np.zeros((dim_k, dim))
    i0 = 0
    for k0 in k:
        matrix0 = hamiltonian(k0)
        eigenvalue, eigenvector = np.linalg.eig(matrix0)
        eigenvalue_k[i0, :] = np.sort(np.real(eigenvalue[:]))
        i0 += 1
    for dim0 in range(dim):
        plt.plot(k, eigenvalue_k[:, dim0], '-k')
    plt.show()


if __name__ == '__main__':
    main()
