import numpy as np
import functools
from math import *
import cmath
import guan

# Installation: pip install --upgrade guan

def main():
    N = 15
    M = 0
    t1 = 1
    phi= pi/2
    t2= 0.03
    tc = 0.8
    layer_num = 2
    bands_of_bilayer_model(N, M, t1, t2, phi, tc, layer_num)
    conductance_of_bilayer_model_with_disorder_array(N, M, t1, t2, phi, tc, layer_num)

# Haldane model

def hamiltonian_of_Haldane_model(k, N, M, t1, t2, phi, sign):
    h00 = h00_of_Haldane_model(N, M, t1, t2, phi, sign)
    h01 = h01_of_Haldane_model(N, M, t1, t2, phi, sign)
    hamiltonian = h00 + h01*cmath.exp(1j*k) + h01.transpose().conj()*cmath.exp(-1j*k)
    return hamiltonian

def h00_of_Haldane_model(N, M, t1, t2, phi, sign):
    h00 = np.zeros((4*N, 4*N), dtype=complex)
    for i0 in range(N):
        h00[i0*4+0, i0*4+0] = M
        h00[i0*4+1, i0*4+1] = -M
        h00[i0*4+2, i0*4+2] = M
        h00[i0*4+3, i0*4+3] = -M
        h00[i0*4+0, i0*4+1] = t1
        h00[i0*4+1, i0*4+0] = t1
        h00[i0*4+1, i0*4+2] = t1
        h00[i0*4+2, i0*4+1] = t1
        h00[i0*4+2, i0*4+3] = t1
        h00[i0*4+3, i0*4+2] = t1
        h00[i0*4+0, i0*4+2] = t2*cmath.exp(1j*phi*sign)
        h00[i0*4+2, i0*4+0] = h00[i0*4+0, i0*4+2].conj()
        h00[i0*4+1, i0*4+3] = t2*cmath.exp(1j*phi*sign)
        h00[i0*4+3, i0*4+1] = h00[i0*4+1, i0*4+3].conj()
    for i0 in range(N-1):
        h00[i0*4+3, (i0+1)*4+0] = t1
        h00[(i0+1)*4+0, i0*4+3] = t1
        h00[i0*4+2, (i0+1)*4+0] = t2*cmath.exp(-1j*phi*sign)
        h00[(i0+1)*4+0, i0*4+2] = h00[i0*4+2, (i0+1)*4+0].conj()
        h00[i0*4+3, (i0+1)*4+1] = t2*cmath.exp(-1j*phi*sign)
        h00[(i0+1)*4+1, i0*4+3] = h00[i0*4+3, (i0+1)*4+1].conj()
    return h00

def h01_of_Haldane_model(N, M, t1, t2, phi, sign):
    h01 = np.zeros((4*N, 4*N), dtype=complex)
    for i0 in range(N):
        h01[i0*4+1, i0*4+0] = t1
        h01[i0*4+2, i0*4+3] = t1
        h01[i0*4+0, i0*4+0] = t2*cmath.exp(-1j*phi*sign)
        h01[i0*4+1, i0*4+1] = t2*cmath.exp(1j*phi*sign)
        h01[i0*4+2, i0*4+2] = t2*cmath.exp(-1j*phi*sign)
        h01[i0*4+3, i0*4+3] = t2*cmath.exp(1j*phi*sign)
        h01[i0*4+1, i0*4+3] = t2*cmath.exp(-1j*phi*sign)
        h01[i0*4+2, i0*4+0] = t2*cmath.exp(1j*phi*sign)
        if i0 != 0:
            h01[i0*4+1, (i0-1)*4+3] = t2*cmath.exp(-1j*phi*sign)
    for i0 in range(N-1):
        h01[i0*4+2, (i0+1)*4+0] = t2*cmath.exp(1j*phi*sign)
    return h01

# modified_Haldane_model

def hamiltonian_of_modified_Haldane_model(k, N, M, t1, t2, phi, sign):
    h00 = h00_of_modified_Haldane_model(N, M, t1, t2, phi, sign)
    h01 = h01_of_modified_Haldane_model(N, M, t1, t2, phi, sign)
    hamiltonian = h00 + h01*cmath.exp(1j*k) + h01.transpose().conj()*cmath.exp(-1j*k)
    return hamiltonian

def h00_of_modified_Haldane_model(N, M, t1, t2, phi, sign):
    h00 = np.zeros((4*N, 4*N), dtype=complex)
    for i0 in range(N):
        h00[i0*4+0, i0*4+0] = M
        h00[i0*4+1, i0*4+1] = -M
        h00[i0*4+2, i0*4+2] = M
        h00[i0*4+3, i0*4+3] = -M
        h00[i0*4+0, i0*4+1] = t1
        h00[i0*4+1, i0*4+0] = t1
        h00[i0*4+1, i0*4+2] = t1
        h00[i0*4+2, i0*4+1] = t1
        h00[i0*4+2, i0*4+3] = t1
        h00[i0*4+3, i0*4+2] = t1
        h00[i0*4+0, i0*4+2] = t2*cmath.exp(-1j*phi*sign)
        h00[i0*4+2, i0*4+0] = h00[i0*4+0, i0*4+2].conj()
        h00[i0*4+1, i0*4+3] = t2*cmath.exp(1j*phi*sign)
        h00[i0*4+3, i0*4+1] = h00[i0*4+1, i0*4+3].conj()
    for i0 in range(N-1):
        h00[i0*4+3, (i0+1)*4+0] = t1
        h00[(i0+1)*4+0, i0*4+3] = t1
        h00[i0*4+2, (i0+1)*4+0] = t2*cmath.exp(1j*phi*sign)
        h00[(i0+1)*4+0, i0*4+2] = h00[i0*4+2, (i0+1)*4+0].conj()
        h00[i0*4+3, (i0+1)*4+1] = t2*cmath.exp(-1j*phi*sign)
        h00[(i0+1)*4+1, i0*4+3] = h00[i0*4+3, (i0+1)*4+1].conj()
    return h00

def h01_of_modified_Haldane_model(N, M, t1, t2, phi, sign):
    h01 = np.zeros((4*N, 4*N), dtype=complex)
    for i0 in range(N):
        h01[i0*4+1, i0*4+0] = t1
        h01[i0*4+2, i0*4+3] = t1
        h01[i0*4+0, i0*4+0] = t2*cmath.exp(1j*phi*sign)
        h01[i0*4+1, i0*4+1] = t2*cmath.exp(1j*phi*sign)
        h01[i0*4+2, i0*4+2] = t2*cmath.exp(1j*phi*sign)
        h01[i0*4+3, i0*4+3] = t2*cmath.exp(1j*phi*sign)
        h01[i0*4+1, i0*4+3] = t2*cmath.exp(-1j*phi*sign)
        h01[i0*4+2, i0*4+0] = t2*cmath.exp(-1j*phi*sign)
        if i0 != 0:
            h01[i0*4+1, (i0-1)*4+3] = t2*cmath.exp(-1j*phi*sign)
    for i0 in range(N-1):
        h01[i0*4+2, (i0+1)*4+0] = t2*cmath.exp(-1j*phi*sign)
    return h01

# bilayer model

def hamiltonian_of_bilayer_model(k, N, M, t1, t2, phi, tc, layer_num):
    modified_Haldane_model = hamiltonian_of_modified_Haldane_model(k=k, N=N, M=M, t1=t1, t2=t2, phi=phi, sign=1)
    Haldane_model = hamiltonian_of_Haldane_model(k=k, N=N, M=M, t1=t1, t2=t2, phi=phi, sign=1)
    hamiltonian = np.zeros((4*N*layer_num, 4*N*layer_num), dtype=complex)
    for layer in range(layer_num):
        if np.mod(layer,2) == 0:
            hamiltonian[layer*4*N+0:layer*4*N+4*N, layer*4*N+0:layer*4*N+4*N] = modified_Haldane_model
        if np.mod(layer,2) == 1:
            hamiltonian[layer*4*N+0:layer*4*N+4*N, layer*4*N+0:layer*4*N+4*N] = Haldane_model 
    for layer in range(layer_num-1):
        for i0 in range(N):
            # AB stacking
            hamiltonian[layer*4*N+i0*4+0, (layer+1)*4*N+i0*4+1] = tc
            hamiltonian[(layer+1)*4*N+i0*4+1, layer*4*N+i0*4+0] = tc
            hamiltonian[layer*4*N+i0*4+2, (layer+1)*4*N+i0*4+3] = tc
            hamiltonian[(layer+1)*4*N+i0*4+3, layer*4*N+i0*4+2] = tc
            
            # # # BA stacking
            # hamiltonian[layer*4*N+i0*4+1, (layer+1)*4*N+i0*4+0] = tc
            # hamiltonian[(layer+1)*4*N+i0*4+0, layer*4*N+i0*4+1] = tc
            # hamiltonian[layer*4*N+i0*4+3, (layer+1)*4*N+i0*4+2] = tc
            # hamiltonian[(layer+1)*4*N+i0*4+2, layer*4*N+i0*4+3] = tc

            # # AA stacking
            # hamiltonian[layer*4*N+i0*4+0, (layer+1)*4*N+i0*4+0] = tc
            # hamiltonian[(layer+1)*4*N+i0*4+0, layer*4*N+i0*4+0] = tc
            # hamiltonian[layer*4*N+i0*4+1, (layer+1)*4*N+i0*4+1] = tc
            # hamiltonian[(layer+1)*4*N+i0*4+1, layer*4*N+i0*4+1] = tc
            # hamiltonian[layer*4*N+i0*4+2, (layer+1)*4*N+i0*4+2] = tc
            # hamiltonian[(layer+1)*4*N+i0*4+2, layer*4*N+i0*4+2] = tc
            # hamiltonian[layer*4*N+i0*4+3, (layer+1)*4*N+i0*4+3] = tc
            # hamiltonian[(layer+1)*4*N+i0*4+3, layer*4*N+i0*4+3] = tc
    return hamiltonian

def h00_of_bilayer_model(N, M, t1, t2, phi, tc, layer_num):
    h00_modified = h00_of_modified_Haldane_model(N, M, t1, t2, phi, sign=1)
    h00_Haldane = h00_of_Haldane_model(N, M, t1, t2, phi, sign=1)
    h00  = np.zeros((4*N*layer_num, 4*N*layer_num), dtype=complex) 
    for layer in range(layer_num):
        if np.mod(layer,2) == 0:
            h00[layer*4*N+0:layer*4*N+4*N, layer*4*N+0:layer*4*N+4*N] = h00_modified
        if np.mod(layer,2) == 1:
            h00[layer*4*N+0:layer*4*N+4*N, layer*4*N+0:layer*4*N+4*N] = h00_Haldane
    for layer in range(layer_num-1):
        for i0 in range(N):
            # AB stacking
            h00[layer*4*N+i0*4+0, (layer+1)*4*N+i0*4+1] = tc
            h00[(layer+1)*4*N+i0*4+1, layer*4*N+i0*4+0] = tc
            h00[layer*4*N+i0*4+2, (layer+1)*4*N+i0*4+3] = tc
            h00[(layer+1)*4*N+i0*4+3, layer*4*N+i0*4+2] = tc

            # # BA stacking
            # h00[layer*4*N+i0*4+1, (layer+1)*4*N+i0*4+0] = tc
            # h00[(layer+1)*4*N+i0*4+0, layer*4*N+i0*4+1] = tc
            # h00[layer*4*N+i0*4+3, (layer+1)*4*N+i0*4+2] = tc
            # h00[(layer+1)*4*N+i0*4+2, layer*4*N+i0*4+3] = tc

            # # AA stacking
            # h00[layer*4*N+i0*4+0, (layer+1)*4*N+i0*4+0] = tc
            # h00[(layer+1)*4*N+i0*4+0, layer*4*N+i0*4+0] = tc
            # h00[layer*4*N+i0*4+1, (layer+1)*4*N+i0*4+1] = tc
            # h00[(layer+1)*4*N+i0*4+1, layer*4*N+i0*4+1] = tc
            # h00[layer*4*N+i0*4+2, (layer+1)*4*N+i0*4+2] = tc
            # h00[(layer+1)*4*N+i0*4+2, layer*4*N+i0*4+2] = tc
            # h00[layer*4*N+i0*4+3, (layer+1)*4*N+i0*4+3] = tc
            # h00[(layer+1)*4*N+i0*4+3, layer*4*N+i0*4+3] = tc
    return h00

def h01_of_bilayer_model(N, M, t1, t2, phi, tc, layer_num):
    h01_modified = h01_of_modified_Haldane_model(N, M, t1, t2, phi, sign=1)
    h01_Haldane = h01_of_Haldane_model(N, M, t1, t2, phi, sign=1)
    h01  = np.zeros((4*N*layer_num, 4*N*layer_num), dtype=complex)
    for layer in range(layer_num):
        if np.mod(layer,2) == 0:
            h01[layer*4*N+0:layer*4*N+4*N, layer*4*N+0:layer*4*N+4*N] = h01_modified
        if np.mod(layer,2) == 1:
            h01[layer*4*N+0:layer*4*N+4*N, layer*4*N+0:layer*4*N+4*N] = h01_Haldane
    return h01

def bands_of_bilayer_model(N, M, t1, t2, phi, tc, layer_num):
    k_array = np.linspace(0, 2*pi, 300)
    hamiltonian = functools.partial(hamiltonian_of_bilayer_model, N=N, M=M, t1=t1, t2=t2, phi=phi, tc=tc, layer_num=layer_num)
    eigenvalue_array = guan.calculate_eigenvalue_with_one_parameter(k_array, hamiltonian, print_show=1)
    plt, fig, ax = guan.import_plt_and_start_fig_ax(labelsize=25)
    guan.plot_without_starting_fig_ax(plt, fig, ax, k_array, eigenvalue_array, xlabel='$\mathrm{k_x}$', ylabel='$\mathrm{E}$', style='k', fontsize=30,  y_max=0.2, y_min=-0.2,linewidth=None, markersize=None, color=None, fontfamily='Times New Roman')
    plt.show()

def conductance_of_bilayer_model_with_disorder_array(N, M, t1, t2, phi, tc, layer_num):
    h00 = h00_of_bilayer_model(N, M, t1, t2, phi, tc, layer_num)
    h01 = h01_of_bilayer_model(N, M, t1, t2, phi, tc, layer_num)
    fermi_energy = 0
    disorder_intensity_array = np.arange(0, 2.5, .05)
    conductance_array = guan.calculate_conductance_with_disorder_intensity_array(fermi_energy, h00, h01, disorder_intensity_array, length=100, calculation_times=3, print_show=1) # length=2000, calculation_times=20
    guan.plot(disorder_intensity_array, conductance_array, xlabel='$\mathrm{W_d}$', ylabel='$\mathrm{G(e^2/h)}$', style='o-')

if __name__ == '__main__':
    main()