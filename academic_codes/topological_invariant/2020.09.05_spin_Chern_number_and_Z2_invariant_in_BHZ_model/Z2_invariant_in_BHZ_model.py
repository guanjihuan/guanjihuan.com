"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5778
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *   # 引入pi, cos等
import cmath
import time


def hamiltonian(kx, ky):  # BHZ模型
    A=0.3645/5
    B=-0.686/25
    C=0
    D=-0.512/25
    M=-0.01
    matrix = np.zeros((4, 4))*(1+0j) 

    varepsilon = C-2*D*(2-cos(kx)-cos(ky))
    d3 = -2*B*(2-(M/2/B)-cos(kx)-cos(ky))
    d1_d2 = A*(sin(kx)+1j*sin(ky))
    matrix[0, 0] = varepsilon+d3
    matrix[1, 1] = varepsilon-d3
    matrix[0, 1] = np.conj(d1_d2)
    matrix[1, 0] = d1_d2 

    varepsilon = C-2*D*(2-cos(-kx)-cos(-ky))
    d3 = -2*B*(2-(M/2/B)-cos(-kx)-cos(-ky))
    d1_d2 = A*(sin(-kx)+1j*sin(-ky))
    matrix[2, 2] = varepsilon+d3
    matrix[3, 3] = varepsilon-d3
    matrix[2, 3] = d1_d2 
    matrix[3, 2] = np.conj(d1_d2)
    return matrix


def main():
    start_clock = time.perf_counter()
    delta = 0.1
    Z2 = 0  # Z2数
    for kx in np.arange(-pi, 0, delta):
        print(kx)
        for ky in np.arange(-pi, pi, delta):
            H = hamiltonian(kx, ky) 
            eigenvalue, eigenvector = np.linalg.eig(H)
            vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 价带波函数1
            vector2 = eigenvector[:, np.argsort(np.real(eigenvalue))[1]]  # 价带波函数2
        
            H_delta_kx = hamiltonian(kx+delta, ky) 
            eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
            vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]   # 略偏离kx的波函数1
            vector_delta_kx2 = eigenvector[:, np.argsort(np.real(eigenvalue))[1]]   # 略偏离kx的波函数2

            H_delta_ky = hamiltonian(kx, ky+delta)  
            eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
            vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离ky的波函数1
            vector_delta_ky2 = eigenvector[:, np.argsort(np.real(eigenvalue))[1]]  # 略偏离ky的波函数2
            
            H_delta_kx_ky = hamiltonian(kx+delta, ky+delta)  
            eigenvalue, eigenvector = np.linalg.eig(H_delta_kx_ky)
            vector_delta_kx_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离kx和ky的波函数1
            vector_delta_kx_ky2 = eigenvector[:, np.argsort(np.real(eigenvalue))[1]]  # 略偏离kx和ky的波函数2
            
            Ux = dot_and_det(vector, vector_delta_kx, vector2, vector_delta_kx2)
            Uy = dot_and_det(vector, vector_delta_ky, vector2, vector_delta_ky2)
            Ux_y = dot_and_det(vector_delta_ky, vector_delta_kx_ky, vector_delta_ky2, vector_delta_kx_ky2)
            Uy_x = dot_and_det(vector_delta_kx, vector_delta_kx_ky, vector_delta_kx2, vector_delta_kx_ky2)

            F = np.imag(cmath.log(Ux*Uy_x*np.conj(Ux_y)*np.conj(Uy)))
            A = np.imag(cmath.log(Ux))+np.imag(cmath.log(Uy_x))+np.imag(cmath.log(np.conj(Ux_y)))+np.imag(cmath.log(np.conj(Uy)))
            Z2 = Z2 + (A-F)/(2*pi)
    print('Z2 = ', Z2)  # Z2数
    end_clock = time.perf_counter()
    print('CPU执行时间(min)=', (end_clock-start_clock)/60)


def dot_and_det(a1, b1, a2, b2): # 内积组成的矩阵对应的行列式
    x1 = np.dot(np.conj(a1), b1)
    x2 = np.dot(np.conj(a2), b2)
    x3 = np.dot(np.conj(a1), b2)
    x4 = np.dot(np.conj(a2), b1)
    return x1*x2-x3*x4


if __name__ == '__main__':
    main()
