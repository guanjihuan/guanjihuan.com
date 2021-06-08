import numpy as np
from math import *
# import os
# os.chdir('D:/data')  # 设置路径


def hamiltonian(k1, k2):
    pass


def main():
    k1 = np.arange(-pi, pi, 0.05)
    k2 = np.arange(-pi, pi, 0.05)
    write_bands_two_dimension(k1, k2, hamiltonian)


def write_bands_two_dimension(k1, k2, hamiltonian):
    f1 = open('a1.txt', 'w')
    f2 = open('a2.txt', 'w')
    f1.write('0     ')
    f2.write('0     ')
    for k10 in k1:
        f1.write(str(k10)+'   ')
        f2.write(str(k10)+'   ')
    f1.write('\n')
    f2.write('\n')
    for k20 in k2:
        f1.write(str(k20)+'   ')
        f2.write(str(k20)+'   ')
        for k10 in k1:
            matrix0 = hamiltonian(k10, k20)
            eigenvalue, eigenvector = np.linalg.eig(matrix0)
            eigenvalue = np.sort(np.real(eigenvalue))
            f1.write(str(eigenvalue[0])+'   ')
            f2.write(str(eigenvalue[1])+'   ')
        f1.write('\n')
        f2.write('\n')
    f1.close()
    f2.close()

if __name__ == '__main__':
    main()