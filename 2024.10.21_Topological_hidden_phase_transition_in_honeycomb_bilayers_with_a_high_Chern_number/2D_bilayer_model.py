import numpy as np
from math import *
import cmath
import functools
import guan 

# Installation: pip install --upgrade guan

def main():
    M = 0
    t1 = 1
    phi= pi/2
    t2 = 0.03
    tc = 0.31
    bilayer_bands(M, t1, t2, phi, tc)
    chern_number(M, t1, t2, phi)

def hamiltonian_of_Haldane(k1, k2, M, t1, t2, phi, a=1/sqrt(3)): 
    h0 = np.zeros((2, 2), dtype=complex)
    h1 = np.zeros((2, 2), dtype=complex)
    h2 = np.zeros((2, 2), dtype=complex)

    h1[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h1[0, 1] = h1[0, 1].conj()

    h2[0, 0] = t2*cmath.exp(1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))
    h2[1, 1] = t2*cmath.exp(-1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))
    matrix = h0 + h1 + h2 + h2.transpose().conj()
    return matrix

def hamiltonian_of_modified_Haldane(k1, k2, M, t1, t2, phi, a=1/sqrt(3)): 
    h0 = np.zeros((2, 2), dtype=complex)
    h1 = np.zeros((2, 2), dtype=complex)
    h2 = np.zeros((2, 2), dtype=complex)

    k1 = -k1  # kx  # Note that to get the unit cell the bilayer honeycomb lattice containing all possible layer hoppings, here one layer (HM layer or mHM layer） needs to be applied with its counterpart of mirror symmetry along x direction.

    h1[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h1[0, 1] = h1[1, 0].conj()

    h2[0, 0] = t2*cmath.exp(1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))
    h2[1, 1] = t2*cmath.exp(1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))

    matrix = h0 + h1 + h2 + h2.transpose().conj()
    return matrix

def hamiltonian_of_bilayer(k1, k2, M, t1, t2, phi, tc):
    hamiltonian1 = hamiltonian_of_Haldane(k1, k2, M, t1, t2, phi, a=1/sqrt(3))
    hamiltonian2 = hamiltonian_of_modified_Haldane(k1, k2, M, t1, t2, phi, a=1/sqrt(3))
    hamiltonian = np.zeros((4, 4), dtype=complex)
    hamiltonian[0:2, 0:2] = hamiltonian1
    hamiltonian[2:4, 2:4] = hamiltonian2

    # AB stacking
    hamiltonian[1, 2] = tc   # B on HM， A on mHM
    hamiltonian[2, 1] = tc

    # BA stacking
    # hamiltonian[0, 3] = tc  # A on HM， B on mHM
    # hamiltonian[3, 0] = tc

    # AA stacking
    # hamiltonian[0, 2] = tc
    # hamiltonian[2, 0] = tc
    # hamiltonian[1, 3] = tc
    # hamiltonian[3, 1] = tc
    return hamiltonian

def bilayer_bands(M, t1, t2, phi, tc):
    k1_array = np.linspace(0, 4*pi, 3000)
    k2 = 0
    hamiltonian = functools.partial(hamiltonian_of_bilayer, k2=k2, M=M, t1=t1, t2=t2, phi=phi, tc=tc)
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k1_array, hamiltonian)
    plt, fig, ax = guan.import_plt_and_start_fig_ax(labelsize=25)
    guan.plot_without_starting_fig_ax(plt, fig, ax, k1_array, eigenvalue_array[:, 0],  linewidth=2)
    guan.plot_without_starting_fig_ax(plt, fig, ax, k1_array, eigenvalue_array[:, 1],  linewidth=2)
    guan.plot_without_starting_fig_ax(plt, fig, ax, k1_array, eigenvalue_array[:, 2],  linewidth=2, color='k')
    guan.plot_without_starting_fig_ax(plt, fig, ax, k1_array, eigenvalue_array[:, 3],  linewidth=2, color='k')
    guan.plot_without_starting_fig_ax(plt, fig, ax, [], [], fontsize=30, y_max=1.5, y_min=-1.5, xlabel='$\mathrm{k_x}$', ylabel='$\mathrm{E}$')
    plt.show()

def chern_number(M, t1, t2, phi):
    tc_array = np.arange(0.05, 0.8, 0.05)
    chern_number_array = []
    for tc in tc_array:
        print(tc)
        hamiltonian = functools.partial(hamiltonian_of_bilayer, M=M, t1=t1, t2=t2, phi=phi, tc=tc)
        chern_number = guan.calculate_chern_number_for_honeycomb_lattice(hamiltonian, a=1/sqrt(3), precision=500, print_show=0)
        print(chern_number, '\n')
        chern_number_array.append(chern_number[0:2])
    guan.plot(tc_array, np.real(chern_number_array), xlabel='$\mathrm{t_c}$', ylabel='$\mathrm{C}$', style='o-')

if __name__ == '__main__':
    main()