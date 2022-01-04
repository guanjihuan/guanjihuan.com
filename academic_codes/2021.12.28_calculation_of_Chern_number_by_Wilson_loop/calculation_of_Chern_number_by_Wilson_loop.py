"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/18319
"""

import numpy as np
from math import * 
import time
import cmath


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
    n = 100  # 积分密度
    delta = 2*pi/n
    chern_number = 0
    for kx in np.arange(-pi, pi, delta):
        for ky in np.arange(-pi, pi, delta):
            H = hamiltonian(kx, ky)
            eigenvalue, eigenvector = np.linalg.eig(H)
            vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 价带波函数
            # vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]*cmath.exp(1j*np.random.uniform(0, pi))  # 验证规范不依赖性
           
            H_delta_kx = hamiltonian(kx+delta, ky) 
            eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
            vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]   # 略偏离kx的波函数

            H_delta_ky = hamiltonian(kx, ky+delta)  
            eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
            vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离ky的波函数

            H_delta_kx_ky = hamiltonian(kx+delta, ky+delta)  
            eigenvalue, eigenvector = np.linalg.eig(H_delta_kx_ky)
            vector_delta_kx_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离kx和ky的波函数

            line_1 = np.dot(vector.transpose().conj(), vector_delta_kx)
            line_2 = np.dot(vector_delta_kx.transpose().conj(), vector_delta_kx_ky)
            line_3 = np.dot(vector_delta_kx_ky.transpose().conj(), vector_delta_ky)
            line_4 = np.dot(vector_delta_ky.transpose().conj(), vector)

            arg = np.log(np.dot(np.dot(np.dot(line_1, line_2), line_3), line_4))/1j
            chern_number = chern_number + arg
    chern_number = chern_number/(2*pi)
    print('Chern number = ', chern_number)
    end_time = time.time()
    print('运行时间(min)=', (end_time-start_time)/60)


if __name__ == '__main__':
    main()