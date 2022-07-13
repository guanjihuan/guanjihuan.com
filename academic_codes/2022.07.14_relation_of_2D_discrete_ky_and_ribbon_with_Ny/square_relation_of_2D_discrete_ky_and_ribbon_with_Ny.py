"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/22691
"""


import guan
import numpy as np
import functools


# 2D square lattice
k1_array = np.linspace(-np.pi, np.pi, 100)
k2_array = np.linspace(-np.pi, np.pi, 100)
eigenvalue_array = guan.calculate_eigenvalue_with_two_parameters(k1_array, k2_array, guan.hamiltonian_of_square_lattice)
guan.plot_3d_surface(k1_array, k2_array, eigenvalue_array, xlabel='kx', ylabel='ky', zlabel='E')


# 2D square lattice for discrete ky array
Ny = 10
ky_array = np.linspace(-np.pi, np.pi, Ny) # important
print(ky_array)

kx_array = np.linspace(-np.pi, np.pi, 100)
i0 = 0
for ky in ky_array:
    hamiltonian_function = functools.partial(guan.hamiltonian_of_square_lattice, k2=ky)
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(kx_array, hamiltonian_function)
    if i0 == 0:
        eigenvalue_array_for_discrete_ky = eigenvalue_array
    else:
        eigenvalue_array_for_discrete_ky = np.append(eigenvalue_array_for_discrete_ky, eigenvalue_array, axis=1)
    i0 += 1


# 1D square ribbon
hamiltonian_function = functools.partial(guan.hamiltonian_of_square_lattice_in_quasi_one_dimension, N=Ny)
eigenvalue_array_2 = guan.calculate_eigenvalue_with_one_parameter(kx_array, hamiltonian_function)


# 1D square ribbon with periodic boundary condition in y direction
hamiltonian_function = functools.partial(guan.hamiltonian_of_square_lattice_in_quasi_one_dimension, N=Ny, period=1)
eigenvalue_array_3 = guan.calculate_eigenvalue_with_one_parameter(kx_array, hamiltonian_function)


# Plot figures
guan.plot_three_array(kx_array, eigenvalue_array_for_discrete_ky, eigenvalue_array_2, eigenvalue_array_3, xlabel='kx', ylabel='E', style_1='-k', style_2='--r', style_3='.y', linewidth_1=3, markersize_2=1, markersize_3=1)