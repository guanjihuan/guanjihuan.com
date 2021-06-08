"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6896
"""

import numpy as np
from math import *
import matplotlib.pyplot as plt
import time
import cmath


def hamiltonian(kx,ky,kz):  # Weyl semimetal
    A = 1
    M0 = 1
    M1 = 1
    H = A*(sin(kx)*sigma_x()+sin(ky)*sigma_y())+(M0-M1*(2*(1-cos(kx))+2*(1-cos(ky))+2*(1-cos(kz))))*sigma_z()
    return H


def sigma_x():
    return np.array([[0, 1],[1, 0]])


def sigma_y():
    return np.array([[0, -1j],[1j, 0]])


def sigma_z():
    return np.array([[1, 0],[0, -1]])


def main():
    start_time = time.time()
    n = 50 
    delta = 2*pi/n
    kz_array = np.arange(-pi, pi, 0.1)
    chern_number_array = np.zeros(kz_array.shape[0])
    i0 = 0
    for kz in kz_array:
        print('kz=', kz)
        chern_number = 0  # 陈数初始化
        for kx in  np.arange(-pi, pi, 2*pi/n):
            for ky in  np.arange(-pi, pi, 2*pi/n):
                H = hamiltonian(kx, ky, kz)
                eigenvalue, eigenvector = np.linalg.eig(H)
                vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 价带波函数
            
                H_delta_kx = hamiltonian(kx+delta, ky, kz) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
                vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]   # 略偏离kx的波函数

                H_delta_ky = hamiltonian(kx, ky+delta, kz)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
                vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离ky的波函数
                
                H_delta_kx_ky = hamiltonian(kx+delta, ky+delta, kz)  
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
        print('Chern number = ', chern_number, '\n')
        chern_number_array[i0] = np.real(chern_number)
        i0 += 1
    end_time = time.time()
    print('运行时间(min)=', (end_time-start_time)/60)
    plt.plot(kz_array, chern_number_array, 'o-')
    plt.xlabel('kz')
    plt.ylabel('Chern number') 
    plt.show()


if __name__ == '__main__':
    main()