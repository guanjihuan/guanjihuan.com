"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/12185
"""

import numpy as np
from math import *  
import cmath  
import functools 
import guan

def hamiltonian(B, k, N, M, t1, a):  # graphene哈密顿量（N是条带的宽度参数）
    # 初始化为零矩阵
    h00 = np.zeros((4*N, 4*N), dtype=complex)
    h01 = np.zeros((4*N, 4*N), dtype=complex)
    # 原胞内的跃迁h00
    for i in range(N):
        h00[i*4+0, i*4+0] = M
        h00[i*4+1, i*4+1] = -M
        h00[i*4+2, i*4+2] = M
        h00[i*4+3, i*4+3] = -M
        # 最近邻
        h00[i*4+0, i*4+1] = t1*cmath.exp(-2*pi*1j*B*(3*a*i+1/4*a)*(np.sqrt(3)/2*a))
        h00[i*4+1, i*4+0] = np.conj(h00[i*4+0, i*4+1])
        h00[i*4+1, i*4+2] = t1
        h00[i*4+2, i*4+1] = np.conj(h00[i*4+1, i*4+2])
        h00[i*4+2, i*4+3] = t1*cmath.exp(2*pi*1j*B*(3*a*i+7/4*a)*(np.sqrt(3)/2)*a)
        h00[i*4+3, i*4+2] = np.conj(h00[i*4+2, i*4+3])
    for i in range(N-1):
        # 最近邻
        h00[i*4+3, (i+1)*4+0] = t1
        h00[(i+1)*4+0, i*4+3] = t1
    # 原胞间的跃迁h01
    for i in range(N):
        # 最近邻
        h01[i*4+1, i*4+0] = t1*cmath.exp(-2*pi*1j*B*(3*a*i+1/4*a)*(np.sqrt(3)/2*a))
        h01[i*4+2, i*4+3] = t1*cmath.exp(-2*pi*1j*B*(3*a*i+7/4*a)*(np.sqrt(3)/2*a))
    matrix = h00 + h01*cmath.exp(1j*k) + h01.transpose().conj()*cmath.exp(-1j*k)
    return matrix

def main():
    N = 30
    a = 1
    hamiltonian_function0 = functools.partial(hamiltonian, k=0, N=N, M=0, t1=1, a=a)
    B_array = np.linspace(0, 1/(3*np.sqrt(3)/2*a*a), 100)
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(B_array, hamiltonian_function0)
    BS_array = B_array*(3*np.sqrt(3)/2*a*a)
    guan.plot(BS_array, eigenvalue_array, xlabel='Flux (BS/phi_0)', ylabel='E', title='Ny=%i'%N, filename='a', show=1, save=0, type='k.', y_min=None, y_max=None, markersize=3)
   
if __name__ == '__main__':
    main()