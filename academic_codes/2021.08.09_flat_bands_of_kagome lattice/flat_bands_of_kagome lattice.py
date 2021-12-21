"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/16730
"""

import numpy as np
from math import *
import guan

def hamiltonian(kx, ky):  # kagome lattice
    k1_dot_a1 = kx
    k2_dot_a2 = kx/2+ky*sqrt(3)/2
    k3_dot_a3 = -kx/2+ky*sqrt(3)/2
    h = np.zeros((3, 3), dtype=complex)
    h[0, 1] = 2*cos(k1_dot_a1)
    h[0, 2] = 2*cos(k2_dot_a2)
    h[1, 2] = 2*cos(k3_dot_a3)
    h = h + h.transpose().conj()
    t = 1
    h = -t*h
    return h

kx_array = np.linspace(-pi ,pi, 500)
ky_array = np.linspace(-pi ,pi, 500)
eigenvalue_array = guan.calculate_eigenvalue_with_two_parameters(kx_array, ky_array, hamiltonian)
guan.plot_3d_surface(kx_array, ky_array, eigenvalue_array, xlabel='kx', ylabel='ky', zlabel='E', rcount=200, ccount=200)