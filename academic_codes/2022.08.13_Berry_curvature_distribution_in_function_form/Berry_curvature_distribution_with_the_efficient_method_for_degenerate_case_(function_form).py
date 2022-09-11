"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/24059
"""

import numpy as np
from math import *  
import cmath
import math


def hamiltonian(k1, k2, t1=2.82, a=1/sqrt(3)):  # 石墨烯哈密顿量（a为原子间距，不赋值的话默认为1/sqrt(3)）
    h = np.zeros((2, 2))*(1+0j)
    h[0, 0] = 0.28/2
    h[1, 1] = -0.28/2
    h[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h[0, 1] = h[1, 0].conj()
    return h


def main():
    k_array, berry_curvature_array = calculate_berry_curvature_with_efficient_method_for_degenerate_case(hamiltonian_function=hamiltonian, index_of_bands=[0], k_min=-2*math.pi, k_max=2*math.pi, precision=500)
    dim = berry_curvature_array.shape
    plot_3d_surface(k_array, k_array, np.real(berry_curvature_array), title='Valence Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :]), title='Valence Band  ky=0', xlabel='kx', ylabel='Berry curvature')  # ky=0

    k_array, berry_curvature_array = calculate_berry_curvature_with_efficient_method_for_degenerate_case(hamiltonian_function=hamiltonian, index_of_bands=[0, 1], k_min=-2*math.pi, k_max=2*math.pi, precision=500)
    dim = berry_curvature_array.shape
    plot_3d_surface(k_array, k_array, np.real(berry_curvature_array), title='All Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :]), title='All Band  ky=0', xlabel='kx', ylabel='Berry curvature') # ky=0


    # import guan
    # k_array, berry_curvature_array = guan.calculate_berry_curvature_with_efficient_method_for_degenerate_case(hamiltonian_function=hamiltonian, index_of_bands=[0], k_min=-2*math.pi, k_max=2*math.pi, precision=500)
    # dim = berry_curvature_array.shape
    # guan.plot_3d_surface(k_array, k_array, np.real(berry_curvature_array), title='Valence Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    # guan.plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :]), title='Valence Band  ky=0', xlabel='kx', ylabel='Berry curvature')  # ky=0

    # k_array, berry_curvature_array = guan.calculate_berry_curvature_with_efficient_method_for_degenerate_case(hamiltonian_function=hamiltonian, index_of_bands=[0, 1], k_min=-2*math.pi, k_max=2*math.pi, precision=500)
    # dim = berry_curvature_array.shape
    # guan.plot_3d_surface(k_array, k_array, np.real(berry_curvature_array), title='All Band', xlabel='kx', ylabel='ky', zlabel='Berry curvature')
    # guan.plot(k_array, np.real(berry_curvature_array[int(dim[0]/2), :]), title='All Band  ky=0', xlabel='kx', ylabel='Berry curvature') # ky=0



def calculate_berry_curvature_with_efficient_method_for_degenerate_case(hamiltonian_function, index_of_bands=[0, 1], k_min=-math.pi, k_max=math.pi, precision=100, print_show=0):
    delta = (k_max-k_min)/precision
    k_array = np.arange(k_min, k_max, delta)
    berry_curvature_array = np.zeros((k_array.shape[0], k_array.shape[0]), dtype=complex)
    i00 = 0
    for kx in np.arange(k_min, k_max, delta):
        if print_show == 1:
            print(kx)
        j00 = 0
        for ky in np.arange(k_min, k_max, delta):
            H = hamiltonian_function(kx, ky)
            eigenvalue, vector = np.linalg.eigh(H) 
            H_delta_kx = hamiltonian_function(kx+delta, ky) 
            eigenvalue, vector_delta_kx = np.linalg.eigh(H_delta_kx) 
            H_delta_ky = hamiltonian_function(kx, ky+delta)
            eigenvalue, vector_delta_ky = np.linalg.eigh(H_delta_ky) 
            H_delta_kx_ky = hamiltonian_function(kx+delta, ky+delta)
            eigenvalue, vector_delta_kx_ky = np.linalg.eigh(H_delta_kx_ky)
            dim = len(index_of_bands)
            det_value = 1
            # first dot
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[dim1, dim2] = np.dot(np.conj(vector[:, dim1]), vector_delta_kx[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value = det_value*dot_matrix
            # second dot
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[dim1, dim2] = np.dot(np.conj(vector_delta_kx[:, dim1]), vector_delta_kx_ky[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value = det_value*dot_matrix
            # third dot
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[dim1, dim2] = np.dot(np.conj(vector_delta_kx_ky[:, dim1]), vector_delta_ky[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value = det_value*dot_matrix
            # four dot
            dot_matrix = np.zeros((dim , dim), dtype=complex)
            i0 = 0
            for dim1 in index_of_bands:
                j0 = 0
                for dim2 in index_of_bands:
                    dot_matrix[dim1, dim2] = np.dot(np.conj(vector_delta_ky[:, dim1]), vector[:, dim2])
                    j0 += 1
                i0 += 1
            dot_matrix = np.linalg.det(dot_matrix)/abs(np.linalg.det(dot_matrix))
            det_value= det_value*dot_matrix
            berry_curvature = cmath.log(det_value)/delta/delta*1j
            berry_curvature_array[j00, i00] = berry_curvature
            j00 += 1
        i00 += 1
    return k_array, berry_curvature_array


def plot_3d_surface(x_array, y_array, matrix, xlabel='x', ylabel='y', zlabel='z', title='', fontsize=20, labelsize=15, show=1, save=0, filename='a', file_format='.jpg', dpi=300, z_min=None, z_max=None, rcount=100, ccount=100): 
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    matrix = np.array(matrix)
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    plt.subplots_adjust(bottom=0.1, right=0.65) 
    x_array, y_array = np.meshgrid(x_array, y_array)
    if len(matrix.shape) == 2:
        surf = ax.plot_surface(x_array, y_array, matrix, rcount=rcount, ccount=ccount, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    elif len(matrix.shape) == 3:
        for i0 in range(matrix.shape[2]):
            surf = ax.plot_surface(x_array, y_array, matrix[:,:,i0], rcount=rcount, ccount=ccount, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    ax.set_title(title, fontsize=fontsize, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.set_zlabel(zlabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.zaxis.set_major_locator(LinearLocator(5)) 
    ax.zaxis.set_major_formatter('{x:.2f}')  
    if z_min!=None or z_max!=None:
        if z_min==None:
            z_min=matrix.min()
        if z_max==None:
            z_max=matrix.max()
        ax.set_zlim(z_min, z_max)
    ax.tick_params(labelsize=labelsize) 
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels] 
    cax = plt.axes([0.8, 0.1, 0.05, 0.8]) 
    cbar = fig.colorbar(surf, cax=cax)  
    cbar.ax.tick_params(labelsize=labelsize)
    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
    if save == 1:
        plt.savefig(filename+file_format, dpi=dpi) 
    if show == 1:
        plt.show()
    plt.close('all')


def plot(x_array, y_array, xlabel='x', ylabel='y', title='', fontsize=20, labelsize=20, show=1, save=0, filename='a', file_format='.jpg', dpi=300, style='', y_min=None, y_max=None, linewidth=None, markersize=None, adjust_bottom=0.2, adjust_left=0.2): 
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=adjust_bottom, left=adjust_left)
    ax.grid()
    ax.tick_params(labelsize=labelsize) 
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    ax.plot(x_array, y_array, style, linewidth=linewidth, markersize=markersize)
    ax.set_title(title, fontsize=fontsize, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=fontsize, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=fontsize, fontfamily='Times New Roman') 
    if y_min!=None or y_max!=None:
        if y_min==None:
            y_min=min(y_array)
        if y_max==None:
            y_max=max(y_array)
        ax.set_ylim(y_min, y_max)
    if save == 1:
        plt.savefig(filename+file_format, dpi=dpi) 
    if show == 1:
        plt.show()
    plt.close('all')


if __name__ == '__main__':
    main()