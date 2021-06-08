"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5025
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *  
import cmath 


def hamiltonian(k):  # SSH模型
    v=0.6
    w=1
    matrix = np.zeros((2, 2), dtype=complex)
    matrix[0,1] = v+w*cmath.exp(-1j*k)
    matrix[1,0] = v+w*cmath.exp(1j*k)
    return matrix


def main():
    k = np.linspace(-pi, pi, 100)
    plot_bands_one_dimension(k, hamiltonian)


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
