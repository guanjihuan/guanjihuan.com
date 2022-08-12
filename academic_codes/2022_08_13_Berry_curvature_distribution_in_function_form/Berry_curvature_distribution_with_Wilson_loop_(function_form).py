"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/24059
"""

import numpy as np
from math import *  
import cmath
import math
import guan


def hamiltonian(k1, k2, t1=2.82, a=1/sqrt(3)):  # 石墨烯哈密顿量（a为原子间距，不赋值的话默认为1/sqrt(3)）
    h = np.zeros((2, 2))*(1+0j)
    h[0, 0] = 0.28/2
    h[1, 1] = -0.28/2
    h[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h[0, 1] = h[1, 0].conj()
    return h


def main():
    k_array, berry_curvature_array = calculate_berry_curvature_with_wilson_loop(hamiltonian_function=hamiltonian, k_min=-2*math.pi, k_max=2*math.pi, precision_of_plaquettes=500, precision_of_wilson_loop=1)
    # k_array, berry_curvature_array = guan.calculate_berry_curvature_with_wilson_loop(hamiltonian_function=hamiltonian, k_min=-2*math.pi, k_max=2*math.pi, precision_of_plaquettes=500, precision_of_wilson_loop=1)
    guan.plot_3d_surface(k_array, k_array, np.real(berry_curvature_array[:, :, 0]), title='Valence Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    guan.plot_3d_surface(k_array, k_array, np.real(berry_curvature_array[:, :, 1]), title='Conductance Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    dim = berry_curvature_array.shape
    guan.plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :, 0]), title='Valence Band  ky=0', xlabel='kx', ylabel='Berry curvature')  # ky=0
    guan.plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :, 1]), title='Conductance Band  ky=0', xlabel='kx', ylabel='Berry curvature') # ky=0


def calculate_berry_curvature_with_wilson_loop(hamiltonian_function, k_min=-math.pi, k_max=math.pi, precision_of_plaquettes=20, precision_of_wilson_loop=5, print_show=0):
    if np.array(hamiltonian_function(0, 0)).shape==():
        dim = 1
    else:
        dim = np.array(hamiltonian_function(0, 0)).shape[0]   
    delta = (k_max-k_min)/precision_of_plaquettes
    k_array = np.arange(k_min, k_max, delta)
    berry_curvature_array = np.zeros((k_array.shape[0], k_array.shape[0], dim), dtype=complex)
    i00 = 0
    for kx in k_array:
        if print_show == 1:
            print(kx)
        j00 = 0
        for ky in k_array:
            vector_array = []
            # line_1
            for i0 in range(precision_of_wilson_loop):
                H_delta = hamiltonian_function(kx+delta/precision_of_wilson_loop*i0, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)
            # line_2
            for i0 in range(precision_of_wilson_loop):
                H_delta = hamiltonian_function(kx+delta, ky+delta/precision_of_wilson_loop*i0)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)
            # line_3
            for i0 in range(precision_of_wilson_loop):
                H_delta = hamiltonian_function(kx+delta-delta/precision_of_wilson_loop*i0, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)
            # line_4
            for i0 in range(precision_of_wilson_loop):
                H_delta = hamiltonian_function(kx, ky+delta-delta/precision_of_wilson_loop*i0)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta)
                vector_delta = eigenvector[:, np.argsort(np.real(eigenvalue))]
                vector_array.append(vector_delta)
            wilson_loop = 1
            for i0 in range(len(vector_array)-1):
                wilson_loop = wilson_loop*np.dot(vector_array[i0].transpose().conj(), vector_array[i0+1])
            wilson_loop = wilson_loop*np.dot(vector_array[len(vector_array)-1].transpose().conj(), vector_array[0])
            berry_curvature = np.log(np.diagonal(wilson_loop))/delta/delta*1j
            berry_curvature_array[j00, i00, :]=berry_curvature
            j00 += 1
        i00 += 1
    return k_array, berry_curvature_array


if __name__ == '__main__':
    main()