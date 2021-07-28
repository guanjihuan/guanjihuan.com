import numpy as np
from math import *
import cmath
import guan

v=0.6
w=1
k = np.linspace(-pi ,pi, 100)

def hamiltonian_1(k):
    matrix = np.zeros((2, 2), dtype=complex)
    matrix[0,1] = v+w*cmath.exp(-1j*k)
    matrix[1,0] = v+w*cmath.exp(1j*k)
    return matrix

def hamiltonian_2(k):
    matrix = np.zeros((2, 2), dtype=complex)
    matrix[0,1] = v*cmath.exp(1j*k/2)+w*cmath.exp(-1j*k/2)
    matrix[1,0] = v*cmath.exp(-1j*k/2)+w*cmath.exp(1j*k/2)
    return matrix

E_1 = guan.calculate_eigenvalue_with_one_parameter(k, hamiltonian_1)
guan.plot(k, E_1, xlabel='k', ylabel='E_1')

E_2 = guan.calculate_eigenvalue_with_one_parameter(k, hamiltonian_2)
guan.plot(k, E_2, xlabel='k', ylabel='E_2')