import numpy as np
from math import *
# import os
# os.chdir('D:/data')  # 设置路径


def hamiltonian(k1, k2):
    pass


def main():
    k1 = np.arange(-pi, pi, 0.05)
    k2 = np.arange(-pi, pi, 0.05)
    plot_bands_two_dimension(k1, k2, hamiltonian)


def plot_bands_two_dimension(k1, k2, hamiltonian):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    dim = hamiltonian(0, 0).shape[0]
    dim1 = k1.shape[0]
    dim2 = k2.shape[0]
    eigenvalue_k = np.zeros((dim2, dim1, dim))
    i0 = 0
    for k20 in k2:
        j0 = 0
        for k10 in k1:
            matrix0 = hamiltonian(k10, k20)
            eigenvalue, eigenvector = np.linalg.eig(matrix0)
            eigenvalue_k[i0, j0, :] = np.sort(np.real(eigenvalue[:]))
            j0 += 1
        i0 += 1
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    k1, k2 = np.meshgrid(k1, k2)
    for dim0 in range(dim):
        ax.plot_surface(k1, k2, eigenvalue_k[:, :, dim0], cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    plt.xlabel('k1')
    plt.ylabel('k2') 
    ax.set_zlabel('E')  
    plt.show()


if __name__ == '__main__':
    main()