"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/7650
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *


def matrix_00(width):  
    h00 = np.zeros((width, width))
    for width0 in range(width-1):
        h00[width0, width0+1] = 1
        h00[width0+1, width0] = 1
    return h00


def matrix_01(width): 
    h01 = np.identity(width)
    return h01
    

def main():
    width = 2
    length = 3
    eta = 1e-2
    E = 0
    h00 = matrix_00(width)
    h01 = matrix_01(width)
    G_ii_n_array = G_ii_n_with_Dyson_equation(width, length, E, eta, h00, h01)
    for i0 in range(length):
        # print('G_{'+str(i0+1)+','+str(i0+1)+'}^{('+str(length)+')}:')
        # print(G_ii_n_array[i0, :, :],'\n')
        print('x=', i0+1, ':')
        for j0 in range(width):
            print('     y=', j0+1, ' ', -np.imag(G_ii_n_array[i0, j0, j0])/pi)   # 态密度


def G_ii_n_with_Dyson_equation(width, length, E, eta, h00, h01):
    G_ii_n_array = np.zeros((length, width, width), complex)
    G_11_1 = np.linalg.inv((E+eta*1j)*np.identity(width)-h00)
    for i in range(length):  # i为格林函数的右下指标
        # 初始化开始
        G_nn_n_minus = G_11_1
        G_in_n_minus = G_11_1
        G_ni_n_minus = G_11_1
        G_ii_n_minus = G_11_1
        for i0 in range(i):
            G_nn_n = Green_nn_n(E, eta, h00, h01, G_nn_n_minus)
            G_nn_n_minus = G_nn_n
        if i!=0:
            G_in_n_minus = G_nn_n
            G_ni_n_minus = G_nn_n
            G_ii_n_minus = G_nn_n
        # 初始化结束
        for j0 in range(length-1-i): # j0为格林函数的右上指标，表示当前体系大小，即G^{(j0)}
            G_nn_n = Green_nn_n(E, eta, h00, h01, G_nn_n_minus)
            G_nn_n_minus = G_nn_n

            G_ii_n = Green_ii_n(G_ii_n_minus, G_in_n_minus, h01, G_nn_n, G_ni_n_minus)  # 需要求的对角分块矩阵
            G_ii_n_minus = G_ii_n

            G_in_n = Green_in_n(G_in_n_minus, h01, G_nn_n)
            G_in_n_minus = G_in_n

            G_ni_n = Green_ni_n(G_nn_n, h01, G_ni_n_minus)
            G_ni_n_minus = G_ni_n
        G_ii_n_array[i, :, :] = G_ii_n_minus
    return G_ii_n_array


def Green_nn_n(E, eta, H00, V, G_nn_n_minus): # n>=2
    dim  = H00.shape[0]
    G_nn_n = np.linalg.inv((E+eta*1j)*np.identity(dim)-H00-np.dot(np.dot(V.transpose().conj(), G_nn_n_minus), V))
    return G_nn_n


def Green_in_n(G_in_n_minus, V, G_nn_n):  # n>=2
    G_in_n = np.dot(np.dot(G_in_n_minus, V), G_nn_n)
    return G_in_n


def Green_ni_n(G_nn_n, V, G_ni_n_minus): # n>=2
    G_ni_n = np.dot(np.dot(G_nn_n, V.transpose().conj()), G_ni_n_minus)
    return G_ni_n


def Green_ii_n(G_ii_n_minus, G_in_n_minus, V, G_nn_n, G_ni_n_minus):  # n>=i
    G_ii_n = G_ii_n_minus+np.dot(np.dot(np.dot(np.dot(G_in_n_minus, V), G_nn_n), V.transpose().conj()),G_ni_n_minus)
    return G_ii_n


if __name__ == '__main__': 
    main()
