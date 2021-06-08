"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/8557
"""

import numpy as np
from math import *


def hamiltonian(Nx, Ny): 
    delta = 1e-3
    gamma = 1e-3
    lambda0 = 1
    h = np.zeros((4*Nx*Ny, 4*Nx*Ny))
    # 元胞内部跃迁
    for x in range(Nx):
        for y in range(Ny):
            h[x*Ny*4+y*4+0, x*Ny*4+y*4+0] = delta
            h[x*Ny*4+y*4+1, x*Ny*4+y*4+1] = delta
            h[x*Ny*4+y*4+2, x*Ny*4+y*4+2] = -delta
            h[x*Ny*4+y*4+3, x*Ny*4+y*4+3] = -delta

            h[x*Ny*4+y*4+0, x*Ny*4+y*4+2] = gamma
            h[x*Ny*4+y*4+0, x*Ny*4+y*4+3] = gamma
            h[x*Ny*4+y*4+1, x*Ny*4+y*4+2] = -gamma
            h[x*Ny*4+y*4+1, x*Ny*4+y*4+3] = gamma
            h[x*Ny*4+y*4+2, x*Ny*4+y*4+0] = gamma
            h[x*Ny*4+y*4+2, x*Ny*4+y*4+1] = -gamma
            h[x*Ny*4+y*4+3, x*Ny*4+y*4+0] = gamma
            h[x*Ny*4+y*4+3, x*Ny*4+y*4+1] = gamma

    # y方向上的元胞间跃迁
    for x in range(Nx):
        for y in range(Ny-1):
            h[x*Ny*4+y*4+0, x*Ny*4+(y+1)*4+3] = lambda0
            h[x*Ny*4+(y+1)*4+1, x*Ny*4+y*4+2] = -lambda0
            h[x*Ny*4+y*4+2, x*Ny*4+(y+1)*4+1] = -lambda0
            h[x*Ny*4+(y+1)*4+3, x*Ny*4+y*4+0] = lambda0

    # x方向上的元胞间跃迁
    for x in range(Nx-1):
        for y in range(Ny):
            h[x*Ny*4+y*4+0, (x+1)*Ny*4+y*4+2] = lambda0
            h[(x+1)*Ny*4+y*4+1, x*Ny*4+y*4+3] = lambda0
            h[(x+1)*Ny*4+y*4+2, x*Ny*4+y*4+0] = lambda0
            h[x*Ny*4+y*4+3, (x+1)*Ny*4+y*4+1] = lambda0
    return h
    

def main():
    Nx = 10
    Ny = 10
    fermi_energy = 0
    h = hamiltonian(Nx, Ny)
    green = np.linalg.inv((fermi_energy+1e-6j)*np.eye(h.shape[0])-h)
    DOS = np.zeros((Ny*2, Nx*2))
    for x in range(Nx):
        for y in range(Ny):
            DOS[y*2+1, x*2+1] = -np.imag(green[x*Ny*4+y*4+0, x*Ny*4+y*4+0])/pi
            DOS[y*2+0, x*2+0] = -np.imag(green[x*Ny*4+y*4+1, x*Ny*4+y*4+1])/pi
            DOS[y*2+1, x*2+0] = -np.imag(green[x*Ny*4+y*4+2, x*Ny*4+y*4+2])/pi
            DOS[y*2+0, x*2+1] = -np.imag(green[x*Ny*4+y*4+3, x*Ny*4+y*4+3])/pi
    DOS = DOS/np.sum(DOS)
    Plot_3D_Surface(np.arange(1, 2*Nx+0.001), np.arange(1, 2*Ny+0.001), DOS, xlabel='x', ylabel='y', zlabel='DOS', title='BBH Model', filename='BBH Model')


def Plot_3D_Surface(x, y, matrix, xlabel='x', ylabel='y', zlabel='z', title='title', filename='a'): 
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    plt.subplots_adjust(bottom=0.1, right=0.65) 
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
    ax.zaxis.set_major_locator(LinearLocator(2)) # 设置z轴主刻度的个数
    ax.zaxis.set_major_formatter('{x:.2f}')   # 设置z轴主刻度的格式
    ax.tick_params(labelsize=15)  # 设置刻度值字体大小
    labels = ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()
    [label.set_fontname('Times New Roman') for label in labels] # 设置刻度值字体
    cax = plt.axes([0.80, 0.15, 0.05, 0.75]) # color bar的位置 [左，下，宽度， 高度]
    cbar = fig.colorbar(surf, cax=cax)  # color bar
    cbar.ax.tick_params(labelsize=15) # 设置color bar刻度的字体大小
    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
    # plt.savefig(filename+'.jpg', dpi=300) 
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    main()