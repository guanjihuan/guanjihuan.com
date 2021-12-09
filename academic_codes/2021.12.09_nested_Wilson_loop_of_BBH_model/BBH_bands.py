"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/17984
"""

import numpy as np
import cmath
from math import *
import functools
import guan

def hamiltonian(kx, ky):  # BBH model
    # label of atoms in a unit cell
    # (2) —— (0)
    #  |      |
    # (1) —— (3)   
    gamma_x = 0.5  # hopping inside one unit cell
    lambda_x = 1   # hopping between unit cells
    gamma_y = gamma_x
    lambda_y = lambda_x
    h = np.zeros((4, 4), dtype=complex)
    h[0, 2] = gamma_x+lambda_x*cmath.exp(1j*kx)
    h[1, 3] = gamma_x+lambda_x*cmath.exp(-1j*kx)
    h[0, 3] = gamma_y+lambda_y*cmath.exp(1j*ky)
    h[1, 2] = -gamma_y-lambda_y*cmath.exp(-1j*ky)
    h[2, 0] = np.conj(h[0, 2])
    h[3, 1] = np.conj(h[1, 3])
    h[3, 0] = np.conj(h[0, 3])
    h[2, 1] = np.conj(h[1, 2]) 
    return h

def main():
    kx = np.arange(-pi, pi, 0.05)
    ky = np.arange(-pi, pi, 0.05)

    eigenvalue_array = guan.calculate_eigenvalue_with_two_parameters(kx, ky, hamiltonian)
    guan.plot_3d_surface(kx, ky, eigenvalue_array, xlabel='kx', ylabel='ky', zlabel='E', title='BBH bands')

    hamiltonian0 = functools.partial(hamiltonian, ky=0) 
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(kx, hamiltonian0)
    guan.plot(kx, eigenvalue_array, xlabel='kx', ylabel='E', title='BBH bands ky=0')

if __name__ == '__main__':
    main()