"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/20869
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *  
import cmath


def hamiltonian(k1, k2, t1=2.82, a=1/sqrt(3)):  # 石墨烯哈密顿量（a为原子间距，不赋值的话默认为1/sqrt(3)）
    h = np.zeros((2, 2), dtype=complex)
    h[0, 0] = 0.28/2
    h[1, 1] = -0.28/2
    h[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h[0, 1] = h[1, 0].conj()
    return h


def main():
    n = 2000  # 取点密度
    delta = 1e-9  # 求导的偏离量
    for band in range(2):
        F_all = []  # 贝里曲率
        for kx in np.linspace(-2*pi, 2*pi, n):
            for ky in [0]: # 这里只考虑ky=0对称轴上的情况
                H = hamiltonian(kx, ky)
                eigenvalue, eigenvector = np.linalg.eig(H)
                if band==0:
                    vector_0 = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]
                    vector_1 = eigenvector[:, np.argsort(np.real(eigenvalue))[1]]
                elif band==1:
                    vector_0 = eigenvector[:, np.argsort(np.real(eigenvalue))[1]]
                    vector_1 = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]
                eigenvalue = np.sort(np.real(eigenvalue))

                H_delta_kx = hamiltonian(kx+delta, ky)-hamiltonian(kx, ky) 
                H_delta_ky = hamiltonian(kx, ky+delta)-hamiltonian(kx, ky)

                berry_curvature = 1j*(np.dot(np.dot(np.dot(np.dot(np.dot(vector_0.transpose().conj(), H_delta_kx/delta), vector_1), vector_1.transpose().conj()), H_delta_ky/delta), vector_0)- np.dot(np.dot(np.dot(np.dot(np.dot(vector_0.transpose().conj(), H_delta_ky/delta), vector_1), vector_1.transpose().conj()), H_delta_kx/delta), vector_0))/(eigenvalue[0]-eigenvalue[1])**2

                F_all = np.append(F_all,[berry_curvature], axis=0) 
        plt.plot(np.linspace(-2*pi, 2*pi, n)/pi, np.real(F_all))
        plt.xlabel('k_x (pi)')
        plt.ylabel('Berry curvature')
        if band==0:
            plt.title('Valence Band')
        else:
            plt.title('Conductance Band')
        plt.show()


if __name__ == '__main__':
    main()