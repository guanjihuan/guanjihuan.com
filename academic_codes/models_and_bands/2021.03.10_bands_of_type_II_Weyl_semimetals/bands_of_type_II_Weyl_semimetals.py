"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/10385
"""

import numpy as np
from math import *


def main():
    k1 = np.linspace(-pi, pi, 100)
    k2 = np.linspace(-pi, pi, 100)

    eigenvalue_array = Calculate_Eigenvalue_with_Two_Parameters(k1, k2, hamiltonian)
    Plot_3D_Surface(k1, k2, eigenvalue_array, xlabel='kx', ylabel='ky', zlabel='E', title='', filename='a')


def hamiltonian(kx,ky,kz=0):
    w0x = 2
    w0y = 0
    w0z = 0
    vx = 1
    vy = 1
    vz = 1
    H = (w0x*kx+w0y*ky+w0z*kz)*sigma_0() + vx*kx*sigma_x()+vy*ky*sigma_y()+vz*kz*sigma_z()
    return H


def sigma_0():
    return np.eye(2)

def sigma_x():
    return np.array([[0, 1],[1, 0]])


def sigma_y():
    return np.array([[0, -1j],[1j, 0]])


def sigma_z():
    return np.array([[1, 0],[0, -1]])


def Calculate_Eigenvalue_with_Two_Parameters(x, y, matrix):  
    dim = np.array(matrix(0, 0)).shape[0]
    dim_x = np.array(x).shape[0]
    dim_y = np.array(y).shape[0]
    eigenvalue_array = np.zeros((dim_y, dim_x, dim))
    i0 = 0
    for y0 in y:
        j0 = 0
        for x0 in x:
            matrix0 = matrix(x0, y0)
            eigenvalue, eigenvector = np.linalg.eig(matrix0)
            eigenvalue_array[i0, j0, :] = np.sort(np.real(eigenvalue[:]))
            j0 += 1
        i0 += 1
    return eigenvalue_array


def Plot_3D_Surface(x, y, matrix, xlabel='x', ylabel='y', zlabel='z', title='', filename='a'): 
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    plt.subplots_adjust(bottom=0.1, right=0.8) 
    x, y = np.meshgrid(x, y)
    if len(matrix.shape) == 2:
        surf = ax.plot_surface(x, y, matrix, cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    elif len(matrix.shape) == 3:
        for i0 in range(matrix.shape[2]):
            surf = ax.plot_surface(x, y, matrix[:,:,i0], cmap=cm.coolwarm, linewidth=0, antialiased=False) 
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_zlabel(zlabel, fontsize=20, fontfamily='Times New Roman') 
    # ax.set_zlim(-1, 1)  # 设置z轴的范围
    ax.zaxis.set_major_locator(LinearLocator(5)) # 设置z轴主刻度的个数
    ax.zaxis.set_major_formatter('{x:.2f}')   # 设置z轴主刻度的格式
    ax.tick_params(labelsize=15)  # 设置刻度值字体大小
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels] # 设置刻度值字体
    # plt.savefig(filename+'.jpg', dpi=300) 
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    main()