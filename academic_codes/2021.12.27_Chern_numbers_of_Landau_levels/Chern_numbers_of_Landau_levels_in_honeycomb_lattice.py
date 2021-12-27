"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/18306
"""

import numpy as np
from math import *
import cmath
import functools
import guan


def hamiltonian(kx, ky, Ny, a, B):
    h00 = np.zeros((4*Ny, 4*Ny), dtype=complex)
    h01 = np.zeros((4*Ny, 4*Ny), dtype=complex)
    t1= 1
    M = 0
    for i in range(Ny):
        h00[i*4+0, i*4+0] = M
        h00[i*4+1, i*4+1] = -M
        h00[i*4+2, i*4+2] = M
        h00[i*4+3, i*4+3] = -M
        h00[i*4+0, i*4+1] = t1*cmath.exp(-2*pi*1j*B*(3*a*i+1/4*a)*(np.sqrt(3)/2*a))
        h00[i*4+1, i*4+0] = np.conj(h00[i*4+0, i*4+1])
        h00[i*4+1, i*4+2] = t1
        h00[i*4+2, i*4+1] = np.conj(h00[i*4+1, i*4+2])
        h00[i*4+2, i*4+3] = t1*cmath.exp(2*pi*1j*B*(3*a*i+7/4*a)*(np.sqrt(3)/2)*a)
        h00[i*4+3, i*4+2] = np.conj(h00[i*4+2, i*4+3])
    for i in range(Ny-1):
        h00[i*4+3, (i+1)*4+0] = t1
        h00[(i+1)*4+0, i*4+3] = t1
    h00[(Ny-1)*4+3, 0+0] = t1*cmath.exp(1j*ky)
    h00[0+0, (Ny-1)*4+3] = t1*cmath.exp(-1j*ky)
    for i in range(Ny):
        h01[i*4+1, i*4+0] = t1*cmath.exp(-2*pi*1j*B*(3*a*i+1/4*a)*(np.sqrt(3)/2*a))
        h01[i*4+2, i*4+3] = t1*cmath.exp(-2*pi*1j*B*(3*a*i+7/4*a)*(np.sqrt(3)/2*a))
    matrix = h00 + h01*cmath.exp(1j*kx) + h01.transpose().conj()*cmath.exp(-1j*kx)
    return matrix


def main():
    Ny = 10
    a = 1

    k_array = np.linspace(-pi, pi, 100)
    H_k = functools.partial(hamiltonian, ky=0, Ny=Ny, a=a, B=1/(3*a*Ny))
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, H_k)
    guan.plot(k_array, eigenvalue_array, xlabel='kx', ylabel='E', type='k')

    H_k = functools.partial(hamiltonian, Ny=Ny, a=a, B=1/(3*a*Ny))
    chern_number = guan.calculate_chern_number_for_square_lattice(H_k, precision=100)
    print(chern_number)
    print(sum(chern_number))


if __name__ == '__main__':
    main()