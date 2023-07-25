"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/2327
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *   # 引入sqrt(), pi, exp等
import cmath  # 要处理复数情况，用到cmath.exp()
import functools  # 使用偏函数functools.partial()


def get_terms(A, B, C, D, M, a):
    E_s = C+M-4*(D+B)/(a**2)
    E_p = C-M-4*(D-B)/(a**2)
    V_ss = (D+B)/(a**2)
    V_pp = (D-B)/(a**2)
    V_sp = -1j*A/(2*a)
    H0 = np.zeros((4, 4), dtype=complex)  # 在位能 (on-site energy)
    H1 = np.zeros((4, 4), dtype=complex)  # x方向的跃迁 (hopping)
    H2 = np.zeros((4, 4), dtype=complex)  # y方向的跃迁 (hopping)
    H0[0, 0] = E_s
    H0[1, 1] = E_p
    H0[2, 2] = E_s
    H0[3, 3] = E_p

    H1[0, 0] = V_ss
    H1[1, 1] = V_pp
    H1[2, 2] = V_ss
    H1[3, 3] = V_pp
    H1[0, 1] = V_sp
    H1[1, 0] = -np.conj(V_sp)
    H1[2, 3] = np.conj(V_sp)
    H1[3, 2] = -V_sp

    H2[0, 0] = V_ss
    H2[1, 1] = V_pp
    H2[2, 2] = V_ss
    H2[3, 3] = V_pp
    H2[0, 1] = 1j*V_sp
    H2[1, 0] = 1j*np.conj(V_sp)
    H2[2, 3] = -1j*np.conj(V_sp)
    H2[3, 2] = -1j*V_sp
    return H0, H1, H2


def BHZ_model(k, A=0.3645/5, B=-0.686/25, C=0, D=-0.512/25, M=-0.01, a=1, N=100):  # 这边数值是不赋值时的默认参数
    H0, H1, H2 = get_terms(A, B, C, D, M, a)
    H00 = np.zeros((4*N, 4*N), dtype=complex)  # 元胞内，条带宽度为N
    H01 = np.zeros((4*N, 4*N), dtype=complex)  # 条带方向元胞间的跃迁
    for i in range(N):
        H00[i*4+0:i*4+4, i*4+0:i*4+4] = H0  # a:b代表 a <= x < b
        H01[i*4+0:i*4+4, i*4+0:i*4+4] = H1
    for i in range(N-1):
        H00[i*4+0:i*4+4, (i+1)*4+0:(i+1)*4+4] = H2
        H00[(i+1)*4+0:(i+1)*4+4, i*4+0:i*4+4] = np.conj(np.transpose(H2))
    H = H00 + H01 * cmath.exp(-1j * k) + H01.transpose().conj() * cmath.exp(1j * k)
    return H


def main():
    hamiltonian0 = functools.partial(BHZ_model, N=50)  # 使用偏函数，固定一些参数
    k = np.linspace(-pi, pi, 300)  # 300
    plot_bands_one_dimension(k, hamiltonian0)


def plot_bands_one_dimension(k, hamiltonian, filename='bands_1D'):
    dim = hamiltonian(0).shape[0]
    dim_k = k.shape[0]
    eigenvalue_k = np.zeros((dim_k, dim))  # np.zeros()里要用tuple
    i0 = 0
    for k0 in k:
        matrix0 = hamiltonian(k0)
        eigenvalue, eigenvector = np.linalg.eig(matrix0)
        eigenvalue_k[i0, :] = np.sort(np.real(eigenvalue[:]))
        i0 += 1
    for dim0 in range(dim):
        plt.plot(k, eigenvalue_k[:, dim0], '-k')  # -.
    # plt.savefig(filename + '.jpg')  # plt.savefig(filename+'.eps')
    plt.show()


if __name__ == '__main__':
    main()
