"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/10064
"""

import numpy as np
import cmath
from math import *


def hamiltonian(k):  # SSH模型哈密顿量
    gamma = 0.5
    lambda0 = 1
    h = np.zeros((2, 2))*(1+0j)
    h[0,0] = 0
    h[1,1] = 0
    h[0,1] = gamma+lambda0*cmath.exp(-1j*k)
    h[1,0] = gamma+lambda0*cmath.exp(1j*k)
    return h


def main():
    Num_k = 100
    k_array = np.linspace(-pi, pi, Num_k)
    vector_array = []
    for k in k_array:
        vector  = get_occupied_bands_vectors(k, hamiltonian)   
        vector_array.append(vector)
        # vector_array.append(vector*cmath.exp(1j*np.random.uniform(0, pi)))

    # 波函数固定一个规范
    vector_sum = 0
    for i0 in range(Num_k):
        vector_sum += np.abs(vector_array[i0])
    index = np.argmax(np.abs(vector_sum))
    for i0 in range(Num_k):
        vector_array[i0] = find_vector_with_fixed_gauge_by_making_one_component_real(vector_array[i0], index=index)

    # # 波函数固定一个规范
    # import guan
    # vector_sum = 0
    # for i0 in range(Num_k):
    #     vector_sum += np.abs(vector_array[i0])
    # index = np.argmax(np.abs(vector_sum))
    # for i0 in range(Num_k):
    #     vector_array[i0] = guan.find_vector_with_fixed_gauge_by_making_one_component_real(vector_array[i0], index=index)

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


def find_vector_with_fixed_gauge_by_making_one_component_real(vector, precision=0.005, index=None):
    if index == None:
        index = np.argmax(np.abs(vector))
    sign_pre = np.sign(np.imag(vector[index]))
    for phase in np.arange(0, 2*np.pi, precision):
        sign =  np.sign(np.imag(vector[index]*cmath.exp(1j*phase)))
        if np.abs(np.imag(vector[index]*cmath.exp(1j*phase))) < 1e-9 or sign == -sign_pre:
            break
        sign_pre = sign
    vector = vector*cmath.exp(1j*phase)
    if np.real(vector[index]) < 0:
        vector = -vector
    return vector


if __name__ == '__main__':
    main()
