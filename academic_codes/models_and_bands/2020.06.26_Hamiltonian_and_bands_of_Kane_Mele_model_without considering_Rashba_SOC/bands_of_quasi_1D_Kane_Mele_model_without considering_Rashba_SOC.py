"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4829
"""

import numpy as np
import matplotlib.pyplot as plt
from math import * 
import cmath 
import functools


def hamiltonian(k, N, M, t1, t2, phi):  # Kane-Mele model
    # 初始化为零矩阵
    h00 = np.zeros((2*4*N, 2*4*N), dtype=complex) # 因为自旋有上有下，所以整个维度要乘2。这里4是元胞内部重复单位的大小，规定元胞大小以4来倍增。
    h01 = np.zeros((2*4*N, 2*4*N), dtype=complex)

    for spin in range(2):
        # 原胞内的跃迁h00
        for i in range(N):
            # 最近邻
            h00[i*4*2+0*2+spin, i*4*2+1*2+spin] = t1 
            h00[i*4*2+1*2+spin, i*4*2+0*2+spin] = t1

            h00[i*4*2+1*2+spin, i*4*2+2*2+spin] = t1  
            h00[i*4*2+2*2+spin, i*4*2+1*2+spin] = t1

            h00[i*4*2+2*2+spin, i*4*2+3*2+spin] = t1  
            h00[i*4*2+3*2+spin, i*4*2+2*2+spin] = t1

            # 次近邻
            h00[i*4*2+0*2+spin, i*4*2+2*2+spin] = t2*cmath.exp(-1j*phi)*sign_spin(spin)    
            h00[i*4*2+2*2+spin, i*4*2+0*2+spin] = h00[i*4*2+0*2+spin, i*4*2+2*2+spin].conj()
            h00[i*4*2+1*2+spin, i*4*2+3*2+spin] = t2*cmath.exp(-1j*phi)*sign_spin(spin) 
            h00[i*4*2+3*2+spin, i*4*2+1*2+spin] = h00[i*4*2+1*2+spin, i*4*2+3*2+spin].conj()
            
        for i in range(N-1):
            # 最近邻
            h00[i*4*2+3*2+spin, (i+1)*4*2+0*2+spin] = t1  
            h00[(i+1)*4*2+0*2+spin, i*4*2+3*2+spin] = t1

            # 次近邻
            h00[i*4*2+2*2+spin, (i+1)*4*2+0*2+spin] = t2*cmath.exp(1j*phi)*sign_spin(spin) 
            h00[(i+1)*4*2+0*2+spin, i*4*2+2*2+spin] = h00[i*4*2+2*2+spin, (i+1)*4*2+0*2+spin].conj()
            h00[i*4*2+3*2+spin, (i+1)*4*2+1*2+spin] = t2*cmath.exp(1j*phi)*sign_spin(spin) 
            h00[(i+1)*4*2+1*2+spin, i*4*2+3*2+spin] = h00[i*4*2+3*2+spin, (i+1)*4*2+1*2+spin].conj()

        # 原胞间的跃迁h01
        for i in range(N):
            # 最近邻
            h01[i*4*2+1*2+spin, i*4*2+0*2+spin] = t1  
            h01[i*4*2+2*2+spin, i*4*2+3*2+spin] = t1

            # 次近邻
            h01[i*4*2+0*2+spin, i*4*2+0*2+spin] = t2*cmath.exp(1j*phi)*sign_spin(spin)  
            h01[i*4*2+1*2+spin, i*4*2+1*2+spin] = t2*cmath.exp(-1j*phi)*sign_spin(spin) 
            h01[i*4*2+2*2+spin, i*4*2+2*2+spin] = t2*cmath.exp(1j*phi)*sign_spin(spin) 
            h01[i*4*2+3*2+spin, i*4*2+3*2+spin] = t2*cmath.exp(-1j*phi)*sign_spin(spin) 

            h01[i*4*2+1*2+spin, i*4*2+3*2+spin] = t2*cmath.exp(1j*phi)*sign_spin(spin)  
            h01[i*4*2+2*2+spin, i*4*2+0*2+spin] = t2*cmath.exp(-1j*phi)*sign_spin(spin) 

            if i != 0:
                h01[i*4*2+1*2+spin, (i-1)*4*2+3*2+spin] = t2*cmath.exp(1j*phi)*sign_spin(spin)   
                
        for i in range(N-1):
            h01[i*4*2+2*2+spin, (i+1)*4*2+0*2+spin] = t2*cmath.exp(-1j*phi)*sign_spin(spin) 

    matrix = h00 + h01*cmath.exp(1j*k) + h01.transpose().conj()*cmath.exp(-1j*k)
    return matrix


def sign_spin(spin):
    if spin==0:
        sign=1
    else:
        sign=-1
    return sign


def main():
    hamiltonian0 = functools.partial(hamiltonian, N=20, M=0, t1=1, t2=0.03, phi=pi/2)
    k = np.linspace(0, 2*pi, 300)
    plot_bands_one_dimension(k, hamiltonian0)


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
    plt.ylim(-1, 1)
    plt.show()


if __name__ == '__main__': 
    main()
