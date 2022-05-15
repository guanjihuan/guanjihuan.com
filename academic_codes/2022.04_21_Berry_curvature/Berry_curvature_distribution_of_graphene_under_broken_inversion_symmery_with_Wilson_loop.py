"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/20869
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *  
import cmath


def hamiltonian(k1, k2, t1=2.82, a=1/sqrt(3)):  # 石墨烯哈密顿量（a为原子间距，不赋值的话默认为1/sqrt(3)）
    h = np.zeros((2, 2))*(1+0j)
    h[0, 0] = 0.28/2
    h[1, 1] = -0.28/2
    h[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h[0, 1] = h[1, 0].conj()
    return h


def main():
    n1 = 1000 # small plaquettes精度
    n2 = 10 # Wilson loop精度
    delta = 2*pi/n1
    for band in range(2):
        F_all = []  # 贝里曲率
        for kx in np.linspace(-2*pi, 2*pi, n1):
            for ky in [0]: # 这里只考虑ky=0对称轴上的情况
                vector_array = []
                # line_1
                for i2 in range(n2+1):
                    H_delta = hamiltonian(kx+delta/n2*i2, ky) 
                    eigenvalue, eigenvector = np.linalg.eig(H_delta)
                    vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]
                    vector_array.append(vector_delta)
                # line_2
                for i2 in range(n2):
                    H_delta = hamiltonian(kx+delta, ky+delta/n2*(i2+1))  
                    eigenvalue, eigenvector = np.linalg.eig(H_delta)
                    vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]
                    vector_array.append(vector_delta)
                # line_3
                for i2 in range(n2):
                    H_delta = hamiltonian(kx+delta-delta/n2*(i2+1), ky+delta)  
                    eigenvalue, eigenvector = np.linalg.eig(H_delta)
                    vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]
                    vector_array.append(vector_delta)
                # line_4
                for i2 in range(n2-1):
                    H_delta = hamiltonian(kx, ky+delta-delta/n2*(i2+1))  
                    eigenvalue, eigenvector = np.linalg.eig(H_delta)
                    vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]
                    vector_array.append(vector_delta)
                Wilson_loop = 1
                for i0 in range(len(vector_array)-1):
                    Wilson_loop = Wilson_loop*np.dot(vector_array[i0].transpose().conj(), vector_array[i0+1])
                Wilson_loop = Wilson_loop*np.dot(vector_array[len(vector_array)-1].transpose().conj(), vector_array[0])
                arg = np.log(Wilson_loop)/delta/delta*1j

                F_all = np.append(F_all,[arg], axis=0) 
        plt.plot(np.linspace(-2*pi, 2*pi, n1)/pi, np.real(F_all))
        plt.xlabel('k_x (pi)')
        plt.ylabel('Berry curvature')
        if band==0:
            plt.title('Valence Band')
        else:
            plt.title('Conductance Band')
        plt.show()


if __name__ == '__main__':
    main()