import numpy as np
from math import *
import guan

def hamiltonian(kx, ky):  # kagome lattice
    k1 = kx
    k2 = kx/2+ky*sqrt(3)/2
    k3 = -kx/2+ky*sqrt(3)/2
    h = np.zeros((3, 3), dtype=complex)
    h[0, 1] = cos(k1)
    h[0, 2] = cos(k2)
    h[1, 2] = cos(k3)
    h = h + h.transpose().conj()
    t = 1
    h = -2*t*h
    return h

kx_array = np.linspace(-pi ,pi, 100)
ky_array = np.linspace(-pi ,pi, 100)
eigenvalue_array = guan.calculate_eigenvalue_with_two_parameters(kx_array, ky_array, hamiltonian)
guan.plot_3d_surface(kx_array, ky_array, eigenvalue_array, xlabel='kx', ylabel='ky', zlabel='E')