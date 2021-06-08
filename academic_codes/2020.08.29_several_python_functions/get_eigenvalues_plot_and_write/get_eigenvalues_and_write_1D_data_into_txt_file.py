import numpy as np
from math import *
# import os
# os.chdir('D:/data')  # 设置路径


def hamiltonian(k):
    pass


def main():
    k = np.arange(-pi, pi, 0.05)
    write_bands_one_dimension(k, hamiltonian)


def write_bands_one_dimension(k, hamiltonian):
    dim = hamiltonian(0).shape[0]
    f = open('a.txt','w')
    for k0 in k:
        f.write(str(k0)+'   ')
        matrix0 = hamiltonian(k0)
        eigenvalue, eigenvector = np.linalg.eig(matrix0)
        eigenvalue = np.sort(np.real(eigenvalue))
        for dim0 in range(dim):
            f.write(str(eigenvalue[dim0])+'   ')
        f.write('\n')
    f.close()


if __name__ == '__main__':
    main()