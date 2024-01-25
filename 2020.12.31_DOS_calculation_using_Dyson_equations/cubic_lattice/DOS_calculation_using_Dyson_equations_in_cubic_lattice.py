"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/7650
"""

import numpy as np

def matrix_00(width, length):  
    h00 = np.zeros((width*length, width*length))
    for x in range(length):
        for y in range(width-1):
            h00[x*width+y, x*width+y+1] = 1
            h00[x*width+y+1, x*width+y] = 1
    for x in range(length-1):
        for y in range(width):
            h00[x*width+y, (x+1)*width+y] = 1
            h00[(x+1)*width+y, x*width+y] = 1
    return h00

def matrix_01(width, length): 
    h01 = np.identity(width*length)
    return h01

def main():
    height = 2  # z
    width = 3   # y
    length = 4  # x
    eta = 1e-2
    E = 0
    h00 = matrix_00(width, length)
    h01 = matrix_01(width, length)
    G_ii_n_array = G_ii_n_with_Dyson_equation(width, length, height, E, eta, h00, h01)
    for i0 in range(height):
        print('z=', i0+1, ':')
        for j0 in range(width):
            print('      y=', j0+1, ':')
            for k0 in range(length):
                print('             x=', k0+1, ' ', -np.imag(G_ii_n_array[i0, k0*width+j0, k0*width+j0])/np.pi)   # 态密度

def G_ii_n_with_Dyson_equation(width, length, height, E, eta, h00, h01):
    dim = length*width
    G_ii_n_array = np.zeros((height, dim, dim), dtype=complex)
    G_11_1 = np.linalg.inv((E+eta*1j)*np.identity(dim)-h00)
    for i in range(height):  # i为格林函数的右下指标
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
        for j0 in range(height-1-i): # j0为格林函数的右上指标，表示当前体系大小，即G^{(j0)}
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