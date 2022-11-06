"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/27656
"""

import guan
import numpy as np

# one dimensional chain model
unit_cell = 0
hopping = 1
hamiltonian_function = guan.one_dimensional_fourier_transform_with_k(unit_cell, hopping)
k_array = np.linspace(-np.pi, np.pi, 100)
eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, hamiltonian_function)
guan.plot(k_array, eigenvalue_array, xlabel='k', ylabel='E', style='k', title='one dimensional chain model')

# n times band folding
max_n = 10
for n in np.arange(2, max_n+1):
    unit_cell = np.zeros((n, n))
    for i0 in range(int(n)):
        for j0 in range(int(n)):
            if abs(i0-j0)==1:
                unit_cell[i0, j0] = 1
    hopping = np.zeros((n, n))
    hopping[0, n-1] = 1
    hamiltonian_function = guan.one_dimensional_fourier_transform_with_k(unit_cell, hopping)
    k_array = np.linspace(-np.pi, np.pi, 100)
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, hamiltonian_function)
    guan.plot(k_array, eigenvalue_array, xlabel='k', ylabel='E', style='k', title='%i times band folding'%n)