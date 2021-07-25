"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/16148
"""

import numpy as np
from math import *
import time


def hamiltonian(kx, ky):  # 量子反常霍尔QAH模型（该参数对应的陈数为2）
    t1 = 1.0
    t2 = 1.0
    t3 = 0.5
    m = -1.0
    matrix = np.zeros((2, 2), dtype=complex)
    matrix[0, 1] = 2*t1*cos(kx)-1j*2*t1*cos(ky)
    matrix[1, 0] = 2*t1*cos(kx)+1j*2*t1*cos(ky)
    matrix[0, 0] = m+2*t3*sin(kx)+2*t3*sin(ky)+2*t2*cos(kx+ky)
    matrix[1, 1] = -(m+2*t3*sin(kx)+2*t3*sin(ky)+2*t2*cos(kx+ky))
    return matrix


def main():
    start_time = time.time()
    n = 200 
    delta = 2*pi/n 
    chern_number = 0 
    for kx in np.arange(-pi, pi, delta):
        for ky in np.arange(-pi, pi,delta):
            H = hamiltonian(kx, ky)
            eigenvalue, eigenvector = np.linalg.eig(H)
            vector_0 = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]
            vector_1 = eigenvector[:, np.argsort(np.real(eigenvalue))[1]]
            eigenvalue = np.sort(np.real(eigenvalue))

            H_delta_kx = hamiltonian(kx+delta, ky)-hamiltonian(kx, ky) 
            H_delta_ky = hamiltonian(kx, ky+delta)-hamiltonian(kx, ky)

            berry_curvature = 1j*(np.dot(np.dot(np.dot(np.dot(np.dot(vector_0.transpose().conj(), H_delta_kx/delta), vector_1), vector_1.transpose().conj()), H_delta_ky/delta), vector_0)- np.dot(np.dot(np.dot(np.dot(np.dot(vector_0.transpose().conj(), H_delta_ky/delta), vector_1), vector_1.transpose().conj()), H_delta_kx/delta), vector_0))/(eigenvalue[0]-eigenvalue[1])**2

            chern_number = chern_number + berry_curvature*(2*pi/n)**2
    chern_number = chern_number/(2*pi)
    print('Chern number = ', chern_number)
    end_time = time.time()
    print('运行时间(min)=', (end_time-start_time)/60)


if __name__ == '__main__':
    main()