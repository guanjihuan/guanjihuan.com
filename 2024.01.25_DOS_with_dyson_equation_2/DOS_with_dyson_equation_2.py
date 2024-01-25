"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/38466
"""

import numpy as np

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
    G_ii_n_array = G_ii_n_with_Dyson_equation_2(width, length, E, eta, h00, h01)
    for i0 in range(length):
        # print('G_{'+str(i0+1)+','+str(i0+1)+'}^{('+str(length)+')}:')
        # print(G_ii_n_array[i0, :, :],'\n')
        print('x=', i0+1, ':')
        for j0 in range(width):
            print('     y=', j0+1, ' ', -np.imag(G_ii_n_array[i0, j0, j0])/np.pi)   # 态密度

def G_ii_n_with_Dyson_equation_2(width, length, E, eta, h00, h01):
    G_ii_n_array = np.zeros((length, width, width), complex)
    G_11_1 = np.linalg.inv((E+eta*1j)*np.identity(width)-h00)
    for i in range(length):
        G_nn_n_right_minus = G_11_1
        G_nn_n_left_minus = G_11_1
        if i!=0:
            for _ in range(i-1):
                G_nn_n_right = Green_nn_n(E, eta, h00, h01, G_nn_n_right_minus)
                G_nn_n_right_minus = G_nn_n_right
        if i!=length-1:
            for _ in range(length-i-2):
                G_nn_n_left = Green_nn_n(E, eta, h00, h01, G_nn_n_left_minus)
                G_nn_n_left_minus = G_nn_n_left
        
        if i==0:
            G_ii_n_array[i, :, :] = np.linalg.inv((E+eta*1j)*np.identity(width)-h00-np.dot(np.dot(h01, G_nn_n_left_minus), h01.transpose().conj()))
        elif i!=0 and i!=length-1:
            G_ii_n_array[i, :, :] = np.linalg.inv((E+eta*1j)*np.identity(width)-h00-np.dot(np.dot(h01.transpose().conj(), G_nn_n_right_minus), h01)-np.dot(np.dot(h01, G_nn_n_left_minus), h01.transpose().conj()))
        elif i==length-1: 
            G_ii_n_array[i, :, :] = np.linalg.inv((E+eta*1j)*np.identity(width)-h00-np.dot(np.dot(h01.transpose().conj(), G_nn_n_right_minus), h01))
    return G_ii_n_array

def Green_nn_n(E, eta, H00, V, G_nn_n_minus):
    dim  = H00.shape[0]
    G_nn_n = np.linalg.inv((E+eta*1j)*np.identity(dim)-H00-np.dot(np.dot(V.transpose().conj(), G_nn_n_minus), V))
    return G_nn_n

if __name__ == '__main__': 
    main()