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
    Num_kx = 100
    Num_ky = 100
    kx_array = np.linspace(-pi, pi, Num_kx)
    ky_array = np.linspace(-pi, pi, Num_ky)
    nu_x_array = []
    for ky in ky_array:
        vector1_array = []
        vector2_array = []
        for kx in kx_array:
            eigenvalue, eigenvector = np.linalg.eigh(hamiltonian(kx, ky))
            if kx != pi:
                vector1_array.append(eigenvector[:, 0])
                vector2_array.append(eigenvector[:, 1])
            else:
                # 这里是为了-pi和pi有相同的波函数，使得Wilson loop的值与波函数规范无关。
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
        for i0 in range(2):
            if np.real(nu_x[i0]) < 0:
                nu_x[i0] += 1
        nu_x = np.sort(nu_x)
        nu_x_array.append(nu_x.real)
    plot(ky_array, nu_x_array, xlabel='ky', ylabel='nu_x', style='-', y_min=0, y_max=1)
    # import guan
    # guan.plot(ky_array, nu_x_array, xlabel='ky', ylabel='nu_x', style='-', y_min=0, y_max=1)

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