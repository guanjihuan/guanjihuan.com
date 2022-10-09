"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/25107
"""

import numpy as np
import math
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

    chern_number = calculate_chern_number_for_square_lattice_with_efficient_method_for_degenerate_case(H_k, index_of_bands=range(int(Ny/2)-1))
    print('价带：', chern_number)
    print()

    chern_number = calculate_chern_number_for_square_lattice_with_efficient_method_for_degenerate_case(H_k, index_of_bands=range(int(Ny/2)+2))
    print('价带（包含两个交叉能带）：', chern_number)
    print()

    chern_number = calculate_chern_number_for_square_lattice_with_efficient_method_for_degenerate_case(H_k, index_of_bands=range(Ny))
    print('所有能带：', chern_number)

    # 函数可通过Guan软件包调用。安装方法：pip install --upgrade guan
    # import guan
    # chern_number = guan.calculate_chern_number_for_square_lattice_with_efficient_method_for_degenerate_case(hamiltonian_function, index_of_bands=[0, 1], precision=100, print_show=0)


def calculate_chern_number_for_square_lattice_with_efficient_method_for_degenerate_case(hamiltonian_function, index_of_bands=[0, 1], precision=100, print_show=0): 
    delta = 2*math.pi/precision
    chern_number = 0
    for kx in np.arange(-math.pi, math.pi, delta):
        if print_show == 1:
            print(kx)
        for ky in np.arange(-math.pi, math.pi, delta):
            H = hamiltonian_function(kx, ky)
            eigenvalue, vector = np.linalg.eigh(H) 
            H_delta_kx = hamiltonian_function(kx+delta, ky) 
            eigenvalue, vector_delta_kx = np.linalg.eigh(H_delta_kx) 
            H_delta_ky = hamiltonian_function(kx, ky+delta)
            eigenvalue, vector_delta_ky = np.linalg.eigh(H_delta_ky) 
            H_delta_kx_ky = hamiltonian_function(kx+delta, ky+delta)
            eigenvalue, vector_delta_kx_ky = np.linalg.eigh(H_delta_kx_ky)
            dim = len(index_of_bands)
            det_value = 1
            # first dot product
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[i0, j0] = np.dot(np.conj(vector[:, dim1]), vector_delta_kx[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value = det_value*dot_matrix
            # second dot product
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[i0, j0] = np.dot(np.conj(vector_delta_kx[:, dim1]), vector_delta_kx_ky[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value = det_value*dot_matrix
            # third dot product
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[i0, j0] = np.dot(np.conj(vector_delta_kx_ky[:, dim1]), vector_delta_ky[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value = det_value*dot_matrix
            # four dot product
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[i0, j0] = np.dot(np.conj(vector_delta_ky[:, dim1]), vector[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value= det_value*dot_matrix
            chern_number += cmath.log(det_value)
    chern_number = chern_number/(2*math.pi*1j)
    return chern_number


if __name__ == '__main__':
    main()