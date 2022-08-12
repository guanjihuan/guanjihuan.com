"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/24059
"""

import numpy as np
from math import *  
import cmath
import guan
import math


def hamiltonian(k1, k2, t1=2.82, a=1/sqrt(3)):  # 石墨烯哈密顿量（a为原子间距，不赋值的话默认为1/sqrt(3)）
    h = np.zeros((2, 2))*(1+0j)
    h[0, 0] = 0.28/2
    h[1, 1] = -0.28/2
    h[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h[0, 1] = h[1, 0].conj()
    return h


def main():
    k_array, berry_curvature_array = calculate_berry_curvature_with_efficient_method(hamiltonian_function=hamiltonian, k_min=-2*math.pi, k_max=2*math.pi, precision=500, print_show=0)
    # k_array, berry_curvature_array = guan.calculate_berry_curvature_with_efficient_method(hamiltonian_function=hamiltonian, k_min=-2*math.pi, k_max=2*math.pi, precision=500, print_show=0)
    guan.plot_3d_surface(k_array, k_array, np.real(berry_curvature_array[:, :, 0]), title='Valence Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    guan.plot_3d_surface(k_array, k_array, np.real(berry_curvature_array[:, :, 1]), title='Conductance Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    dim = berry_curvature_array.shape
    guan.plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :, 0]), title='Valence Band  ky=0', xlabel='kx', ylabel='Berry curvature')  # ky=0
    guan.plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :, 1]), title='Conductance Band  ky=0', xlabel='kx', ylabel='Berry curvature') # ky=0


def calculate_berry_curvature_with_efficient_method(hamiltonian_function, k_min=-math.pi, k_max=math.pi, precision=100, print_show=0):
    if np.array(hamiltonian_function(0, 0)).shape==():
        dim = 1
    else:
        dim = np.array(hamiltonian_function(0, 0)).shape[0]   
    delta = (k_max-k_min)/precision
    k_array = np.arange(k_min, k_max, delta)
    berry_curvature_array = np.zeros((k_array.shape[0], k_array.shape[0], dim), dtype=complex)
    i0 = 0
    for kx in k_array:
        if print_show == 1:
            print(kx)
        j0 = 0
        for ky in k_array:
            H = hamiltonian_function(kx, ky)
            vector = guan.calculate_eigenvector(H)
            H_delta_kx = hamiltonian_function(kx+delta, ky) 
            vector_delta_kx = guan.calculate_eigenvector(H_delta_kx)
            H_delta_ky = hamiltonian_function(kx, ky+delta)
            vector_delta_ky = guan.calculate_eigenvector(H_delta_ky)
            H_delta_kx_ky = hamiltonian_function(kx+delta, ky+delta)
            vector_delta_kx_ky = guan.calculate_eigenvector(H_delta_kx_ky)
            for i in range(dim):
                vector_i = vector[:, i]
                vector_delta_kx_i = vector_delta_kx[:, i]
                vector_delta_ky_i = vector_delta_ky[:, i]
                vector_delta_kx_ky_i = vector_delta_kx_ky[:, i]
                Ux = np.dot(np.conj(vector_i), vector_delta_kx_i)/abs(np.dot(np.conj(vector_i), vector_delta_kx_i))
                Uy = np.dot(np.conj(vector_i), vector_delta_ky_i)/abs(np.dot(np.conj(vector_i), vector_delta_ky_i))
                Ux_y = np.dot(np.conj(vector_delta_ky_i), vector_delta_kx_ky_i)/abs(np.dot(np.conj(vector_delta_ky_i), vector_delta_kx_ky_i))
                Uy_x = np.dot(np.conj(vector_delta_kx_i), vector_delta_kx_ky_i)/abs(np.dot(np.conj(vector_delta_kx_i), vector_delta_kx_ky_i))
                berry_curvature = cmath.log(Ux*Uy_x*(1/Ux_y)*(1/Uy))/delta/delta*1j
                berry_curvature_array[j0, i0, i] = berry_curvature
            j0 += 1
        i0 += 1
    return k_array, berry_curvature_array


if __name__ == '__main__':
    main()