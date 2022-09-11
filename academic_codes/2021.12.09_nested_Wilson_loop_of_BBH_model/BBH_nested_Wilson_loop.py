"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/17984
"""

import numpy as np
import cmath
from math import *

def hamiltonian(kx, ky):  # BBH model
    # label of atoms in a unit cell
    # (2) —— (0)
    #  |      |
    # (1) —— (3)   
    gamma_x = 0.5  # hopping inside one unit cell
    lambda_x = 1   # hopping between unit cells
    gamma_y = gamma_x
    lambda_y = lambda_x
    x_symmetry_breaking_1 = 0.000000000000    # default (not breaking): zero
    x_symmetry_breaking_2 = 1.0000000000001   # default (not breaking): unity
    y_symmetry_breaking_1 = 0.000000000000    # default (not breaking): zero
    y_symmetry_breaking_2 = 1.000000000000    # default (not breaking): unity
    h = np.zeros((4, 4), dtype=complex)
    h[0, 0] = x_symmetry_breaking_1
    h[1, 1] = y_symmetry_breaking_1
    h[2, 2] = y_symmetry_breaking_1
    h[3, 3] = x_symmetry_breaking_1
    h[0, 2] = (gamma_x+lambda_x*cmath.exp(1j*kx))*y_symmetry_breaking_2
    h[1, 3] = gamma_x+lambda_x*cmath.exp(-1j*kx)
    h[0, 3] = gamma_y+lambda_y*cmath.exp(1j*ky)
    h[1, 2] = (-gamma_y-lambda_y*cmath.exp(-1j*ky))*x_symmetry_breaking_2
    h[2, 0] = np.conj(h[0, 2])
    h[3, 1] = np.conj(h[1, 3])
    h[3, 0] = np.conj(h[0, 3])
    h[2, 1] = np.conj(h[1, 2]) 
    return h

def main():
    Num_kx = 30  # for wilson loop and nested wilson loop
    Num_ky = 30  # for wilson loop and nested wilson loop
    Num_kx2 = 20  # plot precision
    Num_ky2 = 20  # plot precision
    kx_array = np.linspace(-pi, pi, Num_kx)
    ky_array = np.linspace(-pi, pi, Num_ky)
    kx2_array = np.linspace(-pi, pi, Num_kx2)
    ky2_array = np.linspace(-pi, pi, Num_ky2)

    # Part I: calculate p_y_for_nu_x
    p_y_for_nu_x_array = []
    for kx in kx2_array:
        print('kx=', kx)
        w_vector_for_nu1_array = []
        vector1_array = []
        vector2_array = []
        i0 = -1
        for ky in ky_array:
            eigenvalue, eigenvector = np.linalg.eigh(hamiltonian(kx, ky))
            if ky != pi:
                vector1_array.append(eigenvector[:, 0])
                vector2_array.append(eigenvector[:, 1])
            else:
                vector1_array.append(vector1_array[0])
                vector2_array.append(vector2_array[0])
        i0=0
        for ky in ky_array:
            if ky != pi:
                nu_x_vector_1, nu_x_vector_2 = get_nu_x_vector(kx_array, ky)
                #  the Wannier band subspaces
                w_vector_for_nu1 =  vector1_array[i0]*nu_x_vector_1[0]+vector2_array[i0]*nu_x_vector_1[1]
                w_vector_for_nu1_array.append(w_vector_for_nu1)
            else:
                w_vector_for_nu1_array.append(w_vector_for_nu1_array[0])
            i0 +=1
        W_y_k_for_nu_x = 1
        for i0 in range(Num_ky-1):
            F_for_nu_x = np.dot(w_vector_for_nu1_array[i0+1].transpose().conj(), w_vector_for_nu1_array[i0])
            W_y_k_for_nu_x = F_for_nu_x*W_y_k_for_nu_x
        p_y_for_nu_x = np.log(W_y_k_for_nu_x)/2/pi/1j
        if np.real(p_y_for_nu_x) < 0:
            p_y_for_nu_x += 1
        p_y_for_nu_x_array.append(p_y_for_nu_x.real) 
        print('p_y_for_nu_x=', p_y_for_nu_x)
    plot(kx2_array, p_y_for_nu_x_array, xlabel='kx', ylabel='p_y_for_nu_x', style='-o', y_min=0, y_max=1)
    # import guan
    # guan.plot(kx2_array, p_y_for_nu_x_array, xlabel='kx', ylabel='p_y_for_nu_x', style='-o', y_min=0, y_max=1)

    # Part II: calculate p_x_for_nu_y
    p_x_for_nu_y_array = []
    for ky in  ky2_array:
        w_vector_for_nu1_array = []
        vector1_array = []
        vector2_array = []
        for kx in kx_array:
            eigenvalue, eigenvector = np.linalg.eigh(hamiltonian(kx, ky))
            if kx != pi:
                vector1_array.append(eigenvector[:, 0])
                vector2_array.append(eigenvector[:, 1])
            else:
                vector1_array.append(vector1_array[0])
                vector2_array.append(vector2_array[0])
        i0 = 0
        for kx in kx_array:
            if kx != pi:
                nu_y_vector_1, nu_y_vector_2 = get_nu_y_vector(kx, ky_array)
                #  the Wannier band subspaces
                w_vector_for_nu1 =  vector1_array[i0]*nu_y_vector_1[0]+vector2_array[i0]*nu_y_vector_1[1]
                w_vector_for_nu1_array.append(w_vector_for_nu1)
            else:
                w_vector_for_nu1_array.append(w_vector_for_nu1_array[0])
            i0 += 1
        W_x_k_for_nu_y = 1
        for i0 in range(Num_ky-1):
            F_for_nu_y = np.dot(w_vector_for_nu1_array[i0+1].transpose().conj(), w_vector_for_nu1_array[i0])
            W_x_k_for_nu_y = F_for_nu_y*W_x_k_for_nu_y
        p_x_for_nu_y = np.log(W_x_k_for_nu_y)/2/pi/1j
        if np.real(p_x_for_nu_y) < 0:
            p_x_for_nu_y += 1
        p_x_for_nu_y_array.append(p_x_for_nu_y.real)
        print('p_x_for_nu_y=', p_x_for_nu_y)
    # print(sum(p_x_for_nu_y_array)/len(p_x_for_nu_y_array))
    plot(ky2_array, p_x_for_nu_y_array, xlabel='ky', ylabel='p_x_for_nu_y', style='-o', y_min=0, y_max=1)
    # import guan
    # guan.plot(ky2_array, p_x_for_nu_y_array, xlabel='ky', ylabel='p_x_for_nu_y', style='-o', y_min=0, y_max=1)

def get_nu_x_vector(kx_array, ky):
    Num_kx = len(kx_array)
    vector1_array = []
    vector2_array = []
    for kx in kx_array:
        eigenvalue, eigenvector = np.linalg.eigh(hamiltonian(kx, ky))
        if kx != pi:
            vector1_array.append(eigenvector[:, 0])
            vector2_array.append(eigenvector[:, 1])
        else:
            vector1_array.append(vector1_array[0])
            vector2_array.append(vector2_array[0])
    W_x_k = np.eye(2, dtype=complex)
    for i0 in range(Num_kx-1):
        F = np.zeros((2, 2), dtype=complex)
        F[0, 0] = np.dot(vector1_array[i0+1].transpose().conj(), vector1_array[i0])
        F[1, 1] = np.dot(vector2_array[i0+1].transpose().conj(), vector2_array[i0])
        F[0, 1] = np.dot(vector1_array[i0+1].transpose().conj(), vector2_array[i0])
        F[1, 0] = np.dot(vector2_array[i0+1].transpose().conj(), vector1_array[i0])
        W_x_k = np.dot(F, W_x_k)
    eigenvalue, eigenvector = np.linalg.eig(W_x_k)
    nu_x = np.log(eigenvalue)/2/pi/1j
    nu_x_vector_1 = eigenvector[:, np.argsort(np.real(nu_x))[0]]
    nu_x_vector_2 = eigenvector[:, np.argsort(np.real(nu_x))[1]]
    return nu_x_vector_1, nu_x_vector_2

def get_nu_y_vector(kx, ky_array):
    Num_ky = len(ky_array)
    vector1_array = []
    vector2_array = []
    for ky in ky_array:
        eigenvalue, eigenvector = np.linalg.eigh(hamiltonian(kx, ky))
        if ky != pi:
            vector1_array.append(eigenvector[:, 0])
            vector2_array.append(eigenvector[:, 1])
        else:
            vector1_array.append(vector1_array[0])
            vector2_array.append(vector2_array[0])
    W_y_k = np.eye(2, dtype=complex)
    for i0 in range(Num_ky-1):
        F = np.zeros((2, 2), dtype=complex)
        F[0, 0] = np.dot(vector1_array[i0+1].transpose().conj(), vector1_array[i0])
        F[1, 1] = np.dot(vector2_array[i0+1].transpose().conj(), vector2_array[i0])
        F[0, 1] = np.dot(vector1_array[i0+1].transpose().conj(), vector2_array[i0])
        F[1, 0] = np.dot(vector2_array[i0+1].transpose().conj(), vector1_array[i0])
        W_y_k = np.dot(F, W_y_k)
    eigenvalue, eigenvector = np.linalg.eig(W_y_k)
    nu_y = np.log(eigenvalue)/2/pi/1j
    nu_y_vector_1 = eigenvector[:, np.argsort(np.real(nu_y))[0]]
    nu_y_vector_2 = eigenvector[:, np.argsort(np.real(nu_y))[1]]
    return nu_y_vector_1, nu_y_vector_2

def plot(x_array, y_array, xlabel='x', ylabel='y', title='', fontsize=20, labelsize=20, show=1, save=0, filename='a', file_format='.jpg', dpi=300, style='', y_min=None, y_max=None, linewidth=None, markersize=None, adjust_bottom=0.2, adjust_left=0.2): 
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
        plt.savefig(filename+file_format, dpi=dpi) 
    if show == 1:
        plt.show()
    plt.close('all')

if __name__ == '__main__':
    main()