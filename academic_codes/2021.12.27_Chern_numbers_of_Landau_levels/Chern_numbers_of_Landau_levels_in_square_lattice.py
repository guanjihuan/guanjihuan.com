"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/18306
"""

import numpy as np
from math import *
import cmath
import functools
import guan

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
    Ny = 21

    k_array = np.linspace(-pi, pi, 100)
    H_k = functools.partial(hamiltonian, ky=0, Ny=Ny, B=1/Ny)
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, H_k)
    guan.plot(k_array, eigenvalue_array, xlabel='kx', ylabel='E', style='k')

    H_k = functools.partial(hamiltonian, Ny=Ny, B=1/Ny)
    chern_number = guan.calculate_chern_number_for_square_lattice(H_k, precision=100)
    print(chern_number)
    print(sum(chern_number))


if __name__ == '__main__':
    main()