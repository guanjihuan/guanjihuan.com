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
    n1 = 10 # small plaquettes精度
    n2 = 800 # Wilson loop精度
    delta = 2*pi/n1
    chern_number = 0
    for kx in np.arange(-pi, pi, delta):
        for ky in np.arange(-pi, pi, delta):
            vector_array = []
            # line_1
            for i2 in range(n2+1):
                H_delta = hamiltonian(kx+delta/n2*i2, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]
                # vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]*cmath.exp(1j*np.random.uniform(0, pi))  # 验证规范不依赖性
                vector_array.append(vector_delta)
            # line_2
            for i2 in range(n2):
                H_delta = hamiltonian(kx+delta, ky+delta/n2*(i2+1))  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]
                vector_array.append(vector_delta)
            # line_3
            for i2 in range(n2):
                H_delta = hamiltonian(kx+delta-delta/n2*(i2+1), ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]
                vector_array.append(vector_delta)
            # line_4
            for i2 in range(n2-1):
                H_delta = hamiltonian(kx, ky+delta-delta/n2*(i2+1))  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]
                vector_array.append(vector_delta)
            Wilson_loop = 1
            for i0 in range(len(vector_array)-1):
                Wilson_loop = Wilson_loop*np.dot(vector_array[i0].transpose().conj(), vector_array[i0+1])
            Wilson_loop = Wilson_loop*np.dot(vector_array[len(vector_array)-1].transpose().conj(), vector_array[0])
            arg = np.log(Wilson_loop)/1j
            chern_number = chern_number + arg
    chern_number = chern_number/(2*pi)
    print('Chern number = ', chern_number)
    end_time = time.time()
    print('运行时间（秒）=', end_time-start_time)


if __name__ == '__main__':
    main()