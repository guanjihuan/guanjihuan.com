"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/16199
"""

import numpy as np
from math import *
import cmath

def hamiltonian_1(k, v=0.6, w=1):
    matrix = np.zeros((2, 2), dtype=complex)
    matrix[0,1] = v+w*cmath.exp(-1j*k)
    matrix[1,0] = v+w*cmath.exp(1j*k)
    return matrix

def hamiltonian_2(k, v=0.6, w=1):
    matrix = np.zeros((2, 2), dtype=complex)
    matrix[0,1] = v*cmath.exp(1j*k/2)+w*cmath.exp(-1j*k/2)
    matrix[1,0] = v*cmath.exp(-1j*k/2)+w*cmath.exp(1j*k/2)
    return matrix

def main():
    k_array = np.linspace(-pi ,pi, 100)
    E_1_array = calculate_eigenvalue_with_one_parameter(k_array, hamiltonian_1)
    plot(k_array, E_1_array, xlabel='k', ylabel='E_1')
    E_2_array = calculate_eigenvalue_with_one_parameter(k_array, hamiltonian_2)
    plot(k_array, E_2_array, xlabel='k', ylabel='E_2')

    # import guan
    # E_1_array = guan.calculate_eigenvalue_with_one_parameter(k_array, hamiltonian_1)
    # guan.plot(k_array, E_1_array, xlabel='k', ylabel='E_1')
    # E_2_array = guan.calculate_eigenvalue_with_one_parameter(k_array, hamiltonian_2)
    # guan.plot(k_array, E_2_array, xlabel='k', ylabel='E_2')

def calculate_eigenvalue_with_one_parameter(x_array, hamiltonian_function, print_show=0):
    dim_x = np.array(x_array).shape[0]
    i0 = 0
    if np.array(hamiltonian_function(0)).shape==():
        eigenvalue_array = np.zeros((dim_x, 1))
        for x0 in x_array:
            hamiltonian = hamiltonian_function(x0)
            eigenvalue_array[i0, 0] = np.real(hamiltonian)
            i0 += 1
    else:
        dim = np.array(hamiltonian_function(0)).shape[0]
        eigenvalue_array = np.zeros((dim_x, dim))
        for x0 in x_array:
            if print_show==1:
                print(x0)
            hamiltonian = hamiltonian_function(x0)
            eigenvalue, eigenvector = np.linalg.eigh(hamiltonian)
            eigenvalue_array[i0, :] = eigenvalue
            i0 += 1
    return eigenvalue_array

def plot(x_array, y_array, xlabel='x', ylabel='y', title='', fontsize=20, labelsize=20, show=1, save=0, filename='a', format='jpg', dpi=300, style='', y_min=None, y_max=None, linewidth=None, markersize=None, adjust_bottom=0.2, adjust_left=0.2): 
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=adjust_bottom, left=adjust_left) 
    ax.plot(x_array, y_array, style, linewidth=linewidth, markersize=markersize)
    ax.grid()
    ax.set_title(title, fontsize=fontsize, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=fontsize, fontfamily='Times New Roman') 
    if y_min!=None or y_max!=None:
        if y_min==None:
            y_min=min(y_array)
        if y_max==None:
            y_max=max(y_array)
        ax.set_ylim(y_min, y_max)
    ax.tick_params(labelsize=labelsize) 
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    if save == 1:
        plt.savefig(filename+'.'+format, dpi=dpi) 
    if show == 1:
        plt.show()
    plt.close('all')

if __name__ == '__main__':
    main()