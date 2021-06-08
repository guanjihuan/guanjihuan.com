"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5778
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *   # 引入pi, cos等
import cmath
import time


def hamiltonian1(kx, ky):  # Half BHZ for spin up
    A=0.3645/5
    B=-0.686/25
    C=0
    D=-0.512/25
    M=-0.01
    matrix = np.zeros((2, 2))*(1+0j) 
    varepsilon = C-2*D*(2-cos(kx)-cos(ky))
    d3 = -2*B*(2-(M/2/B)-cos(kx)-cos(ky))
    d1_d2 = A*(sin(kx)+1j*sin(ky))

    matrix[0, 0] = varepsilon+d3
    matrix[1, 1] = varepsilon-d3
    matrix[0, 1] = np.conj(d1_d2)
    matrix[1, 0] = d1_d2 
    return matrix

def hamiltonian2(kx, ky):  # Half BHZ for spin down
    A=0.3645/5
    B=-0.686/25
    C=0
    D=-0.512/25
    M=-0.01
    matrix = np.zeros((2, 2))*(1+0j) 
    varepsilon = C-2*D*(2-cos(-kx)-cos(-ky))
    d3 = -2*B*(2-(M/2/B)-cos(-kx)-cos(-ky))
    d1_d2 = A*(sin(-kx)+1j*sin(-ky))

    matrix[0, 0] = varepsilon+d3
    matrix[1, 1] = varepsilon-d3
    matrix[0, 1] = d1_d2 
    matrix[1, 0] = np.conj(d1_d2)
    return matrix


def main():
    start_clock = time.perf_counter()
    delta = 0.1 
    for i0 in range(2):
        if i0 == 0:
            hamiltonian = hamiltonian1
        else:
            hamiltonian = hamiltonian2
        chern_number = 0  # 陈数初始化
        for kx in np.arange(-pi, pi, delta):
            print(kx)
            for ky in np.arange(-pi, pi, delta):
                H = hamiltonian(kx, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H)
                vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 价带波函数
            
                H_delta_kx = hamiltonian(kx+delta, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
                vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]   # 略偏离kx的波函数

                H_delta_ky = hamiltonian(kx, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
                vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离ky的波函数
                
                H_delta_kx_ky = hamiltonian(kx+delta, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx_ky)
                vector_delta_kx_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离kx和ky的波函数
                
                Ux = np.dot(np.conj(vector), vector_delta_kx)/abs(np.dot(np.conj(vector), vector_delta_kx))
                Uy = np.dot(np.conj(vector), vector_delta_ky)/abs(np.dot(np.conj(vector), vector_delta_ky))
                Ux_y = np.dot(np.conj(vector_delta_ky), vector_delta_kx_ky)/abs(np.dot(np.conj(vector_delta_ky), vector_delta_kx_ky))
                Uy_x = np.dot(np.conj(vector_delta_kx), vector_delta_kx_ky)/abs(np.dot(np.conj(vector_delta_kx), vector_delta_kx_ky))

                F = cmath.log(Ux*Uy_x*(1/Ux_y)*(1/Uy))
                # 陈数(chern number)
                chern_number = chern_number + F
        chern_number = chern_number/(2*pi*1j)
        if i0 == 0:
            chern_number_up = chern_number
        else:
            chern_number_down = chern_number
    spin_chern_number = (chern_number_up-chern_number_down)/2
    print('Chern number for spin up = ', chern_number_up)
    print('Chern number for spin down = ', chern_number_down)
    print('Spin chern number = ', spin_chern_number)
    end_clock = time.perf_counter()
    print('CPU执行时间(min)=', (end_clock-start_clock)/60)


if __name__ == '__main__':
    main()
