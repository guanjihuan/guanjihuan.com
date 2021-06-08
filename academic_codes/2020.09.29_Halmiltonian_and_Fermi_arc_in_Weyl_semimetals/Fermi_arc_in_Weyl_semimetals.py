"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6077
"""

import numpy as np
from math import *
import matplotlib.pyplot as plt


def main():
    n =  0.5
    k1 = np.arange(-n*pi, n*pi, n/50)
    k2 = np.arange(-n*pi, n*pi, n/50)
    plot_bands_two_dimension_direct(k1, k2, hamiltonian)


def hamiltonian(kx,kz,ky=0):  # surface states of Weyl semimetal
    A = 1
    H = A*kx
    return H


def sigma_x():
    return np.array([[0, 1],[1, 0]])


def sigma_y():
    return np.array([[0, -1j],[1j, 0]])


def sigma_z():
    return np.array([[1, 0],[0, -1]])


def plot_bands_two_dimension_direct(k1, k2, hamiltonian):
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    dim1 = k1.shape[0]
    dim2 = k2.shape[0]
    eigenvalue_k = np.zeros((dim2, dim1))
    i0 = 0   
    for k10 in k1:
        j0 = 0
        for k20 in k2:
            if (k10**2+k20**2 <= 1):
                eigenvalue_k[j0, i0] = hamiltonian(k10, k20)
            else:
                eigenvalue_k[j0, i0] = 'nan'
            j0 += 1
        i0 += 1
    k1, k2 = np.meshgrid(k1, k2)
    ax.scatter(k1, k2, eigenvalue_k)
    plt.xlabel('kx')
    plt.ylabel('kz')
    ax.set_zlabel('E')  
    plt.show()


if __name__ == '__main__':
    main()