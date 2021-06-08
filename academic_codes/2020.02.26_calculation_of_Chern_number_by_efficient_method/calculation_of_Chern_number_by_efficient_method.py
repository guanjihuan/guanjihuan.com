"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4179
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *   # 引入pi, cos等
import cmath
import time


def hamiltonian(kx, ky):  # 量子反常霍尔QAH模型（该参数对应的陈数为2）
    t1 = 1.0
    t2 = 1.0
    t3 = 0.5
    m = -1.0
    matrix = np.zeros((2, 2))*(1+0j)
    matrix[0, 1] = 2*t1*cos(kx)-1j*2*t1*cos(ky)
    matrix[1, 0] = 2*t1*cos(kx)+1j*2*t1*cos(ky)
    matrix[0, 0] = m+2*t3*sin(kx)+2*t3*sin(ky)+2*t2*cos(kx+ky)
    matrix[1, 1] = -(m+2*t3*sin(kx)+2*t3*sin(ky)+2*t2*cos(kx+ky))
    return matrix


def main():
    start_time = time.time()
    n = 100 
    delta = 2*pi/n
    chern_number = 0  # 陈数初始化
    for kx in np.arange(-pi, pi, 2*pi/n):
        for ky in np.arange(-pi, pi, 2*pi/n):
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
    print('Chern number = ', chern_number)
    end_time = time.time()
    print('运行时间(min)=', (end_time-start_time)/60)


if __name__ == '__main__':
    main()
