"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6896
"""

import numpy as np
import guan
import functools

def main():
    kz_array = np.arange(-np.pi, np.pi, 0.1)
    chern_number_array = []
    for kz in kz_array:
        print(kz)
        hamiltonian_function = functools.partial(hamiltonian, kz=kz)
        chern_number = guan.calculate_chern_number_for_square_lattice_with_efficient_method(hamiltonian_function)
        chern_number_array.append(chern_number)
    guan.plot(kz_array, chern_number_array, style='-o')


def hamiltonian(kx,ky,kz):  # Weyl semimetal
    A = 1
    M0 = 1
    M1 = 1
    H = A*(np.sin(kx)*guan.sigma_x()+np.sin(ky)*guan.sigma_y())+(M0-M1*(2*(1-np.cos(kx))+2*(1-np.cos(ky))+2*(1-np.cos(kz))))*guan.sigma_z()
    return H


if __name__ == '__main__':
    main()