"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/23989
"""

import numpy as np
from math import *
import cmath
import functools

def hamiltonian(kx, ky, Ny, B):
    h00 = np.zeros((Ny, Ny), dtype=complex)
    h01 = np.zeros((Ny, Ny), dtype=complex)
    t = 1
    for iy in range(Ny-1):
        h00[iy, iy+1] = t
        h00[iy+1, iy] = t
    h00[Ny-1, 0] = t*cmath.exp(1j*ky)
    h00[0, Ny-1] = t*cmath.exp(-1j*ky)
    for iy in range(Ny):
        h01[iy, iy] = t*cmath.exp(-2*np.pi*1j*B*iy)
    matrix = h00 + h01*cmath.exp(1j*kx) + h01.transpose().conj()*cmath.exp(-1j*kx)
    return matrix


def main():
    Ny = 20

    H_k = functools.partial(hamiltonian, Ny=Ny, B=1/Ny)
    chern_number = calculate_chern_number_for_square_lattice_with_Wilson_loop_for_degenerate_case(H_k, index_of_bands=range(int(Ny/2)-1), precision_of_Wilson_loop=5)
    print('价带：', chern_number)
    print()

    chern_number = calculate_chern_number_for_square_lattice_with_Wilson_loop_for_degenerate_case(H_k, index_of_bands=range(int(Ny/2)+2), precision_of_Wilson_loop=5)
    print('价带（包含两个交叉能带）：', chern_number)
    print()

    chern_number = calculate_chern_number_for_square_lattice_with_Wilson_loop_for_degenerate_case(H_k, index_of_bands=range(Ny), precision_of_Wilson_loop=5)
    print('所有能带：', chern_number)

    # # 函数可通过Guan软件包调用。安装方法：pip install --upgrade guan
    # import guan
    # chern_number = guan.calculate_chern_number_for_square_lattice_with_Wilson_loop_for_degenerate_case(hamiltonian_function, index_of_bands=[0, 1], precision_of_plaquettes=20, precision_of_Wilson_loop=5, print_show=0)


def calculate_chern_number_for_square_lattice_with_Wilson_loop_for_degenerate_case(hamiltonian_function, index_of_bands=[0, 1], precision_of_plaquettes=20, precision_of_Wilson_loop=5, print_show=0):
    import math
    delta = 2*math.pi/precision_of_plaquettes
    chern_number = 0
    for kx in np.arange(-math.pi, math.pi, delta):
        if print_show == 1:
            print(kx)
        for ky in np.arange(-math.pi, math.pi, delta):
            vector_array = []
            # line_1
            for i0 in range(precision_of_Wilson_loop):
                H_delta = hamiltonian_function(kx+delta/precision_of_Wilson_loop*i0, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)
            # line_2
            for i0 in range(precision_of_Wilson_loop):
                H_delta = hamiltonian_function(kx+delta, ky+delta/precision_of_Wilson_loop*i0)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)
            # line_3
            for i0 in range(precision_of_Wilson_loop):
                H_delta = hamiltonian_function(kx+delta-delta/precision_of_Wilson_loop*i0, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)
            # line_4
            for i0 in range(precision_of_Wilson_loop):
                H_delta = hamiltonian_function(kx, ky+delta-delta/precision_of_Wilson_loop*i0)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)           
            Wilson_loop = 1
            dim = len(index_of_bands)
            for i0 in range(len(vector_array)-1):
                dot_matrix = np.zeros((dim , dim), dtype=complex)
                i01 = 0
                for dim1 in index_of_bands:
                    i02 = 0
                    for dim2 in index_of_bands:
                        dot_matrix[i01, i02] = np.dot(vector_array[i0][:, dim1].transpose().conj(), vector_array[i0+1][:, dim2])
                        i02 += 1
                    i01 += 1
                det_value = np.linalg.det(dot_matrix)
                Wilson_loop = Wilson_loop*det_value
            dot_matrix_plus = np.zeros((dim , dim), dtype=complex)
            i01 = 0
            for dim1 in index_of_bands:
                i02 = 0
                for dim2 in index_of_bands:
                    dot_matrix_plus[i01, i02] = np.dot(vector_array[len(vector_array)-1][:, dim1].transpose().conj(), vector_array[0][:, dim2])
                    i02 += 1
                i01 += 1
            det_value = np.linalg.det(dot_matrix_plus)
            Wilson_loop = Wilson_loop*det_value
            arg = np.log(Wilson_loop)/1j
            chern_number = chern_number + arg
    chern_number = chern_number/(2*math.pi)
    return chern_number


if __name__ == '__main__':
    main()