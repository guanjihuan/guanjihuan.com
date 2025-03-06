# 能带图计算
import guan
import numpy as np
k_array = np.linspace(-np.pi, np.pi, 100)
 # one dimensional chain
hamiltonian_function = guan.one_dimensional_fourier_transform_with_k(unit_cell=0, hopping=1)
eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, hamiltonian_function)
guan.plot(k_array, eigenvalue_array, xlabel='k', ylabel='E', style='-k', fontfamily=None)
# square lattice ribbon
eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, guan.hamiltonian_of_square_lattice_in_quasi_one_dimension)
guan.plot(k_array, eigenvalue_array, xlabel='k', ylabel='E', style='-k', fontfamily=None)
# graphene ribbon
eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, guan.hamiltonian_of_graphene_with_zigzag_in_quasi_one_dimension)
guan.plot(k_array, eigenvalue_array, xlabel='k', ylabel='E', style='-k', fontfamily=None)