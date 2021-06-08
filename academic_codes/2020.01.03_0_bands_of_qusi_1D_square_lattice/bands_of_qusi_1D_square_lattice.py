"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/3895
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *
import cmath
import functools


def hamiltonian(k, N, t):  # 准一维方格子哈密顿量
    # 初始化为零矩阵
    h00 = np.zeros((N, N), dtype=complex)
    h01 = np.zeros((N, N), dtype=complex)
    for i in range(N-1):   # 原胞内的跃迁h00
        h00[i, i+1] = t
        h00[i+1, i] = t
    for i in range(N):   # 原胞间的跃迁h01
        h01[i, i] = t
    matrix = h00 + h01*cmath.exp(1j*k) + h01.transpose().conj()*cmath.exp(-1j*k)
    return matrix


def main():
    H_k = functools.partial(hamiltonian, N=10, t=1)
    k = np.linspace(-pi, pi, 300)
    plot_bands_one_dimension(k, H_k)


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
