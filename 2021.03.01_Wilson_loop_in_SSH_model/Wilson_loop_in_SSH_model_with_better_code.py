"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/10064
"""

import numpy as np
import cmath
from math import *


def hamiltonian(k):
    gamma = 0.5
    lambda0 = 1
    delta = 0
    h = np.zeros((2, 2), dtype=complex)
    h[0,0] = delta
    h[1,1] = -delta
    h[0,1] = gamma+lambda0*cmath.exp(-1j*k)
    h[1,0] = gamma+lambda0*cmath.exp(1j*k)
    return h


def main():
    Num_k = 100
    k_array = np.linspace(-pi, pi, Num_k)
    vector_array = []
    for k in k_array:
        vector  = get_occupied_bands_vectors(k, hamiltonian)   
        if k != pi:
            vector_array.append(vector)
        else:
            vector_array.append(vector_array[0])

    # 计算Wilson loop
    W_k = 1
    for i0 in range(Num_k-1):
        F = np.dot(vector_array[i0+1].transpose().conj(), vector_array[i0])
        W_k = np.dot(F, W_k)
    nu = np.log(W_k)/2/pi/1j
    # if np.real(nu) < 0:
    #     nu += 1
    print('p=', nu, '\n')
    

def get_occupied_bands_vectors(x, matrix):  
    matrix0 = matrix(x)
    eigenvalue, eigenvector = np.linalg.eig(matrix0) 
    vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]] 
    return vector


if __name__ == '__main__':
    main()
