import numpy as np
from math import *
# import os
# os.chdir('D:/data')  # 设置路径


def hamiltonian(k):
    pass


def main():
    k = np.arange(-pi, pi, 0.05)
    plot_bands_one_dimension(k, hamiltonian)


def plot_bands_one_dimension(k, hamiltonian):
    import matplotlib.pyplot as plt
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
    plt.xlabel('k')
    plt.ylabel('E') 
    plt.show()


if __name__ == '__main__':
    main()