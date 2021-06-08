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
    
    x_array = []
    y_array = []
    DOS = []
    for x in range(Nx):
        for y in range(Ny):
            x_array.append(x*2+2)
            y_array.append(y*2+2)
            DOS.append(-np.imag(green[x*Ny*4+y*4+0, x*Ny*4+y*4+0])/pi)

            x_array.append(x*2+1)
            y_array.append(y*2+1)
            DOS.append(-np.imag(green[x*Ny*4+y*4+1, x*Ny*4+y*4+1])/pi)

            x_array.append(x*2+1)
            y_array.append(y*2+2)
            DOS.append(-np.imag(green[x*Ny*4+y*4+2, x*Ny*4+y*4+2])/pi)

            x_array.append(x*2+2)
            y_array.append(y*2+1)
            DOS.append(-np.imag(green[x*Ny*4+y*4+3, x*Ny*4+y*4+3])/pi)
    DOS = DOS/np.sum(DOS)
    Plot_2D_Scatter(x_array, y_array, DOS, xlabel='x', ylabel='y', title='BBH Model', filename='BBH Model')


def Plot_2D_Scatter(x, y, value, xlabel='x', ylabel='y', title='title', filename='a'):
    from matplotlib.axes._axes import _log as matplotlib_axes_logger
    matplotlib_axes_logger.setLevel('ERROR')  # 只显示error级别的通知   
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LinearLocator
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.subplots_adjust(bottom=0.2, right=0.8, left=0.2) 
    for i in range(np.array(x).shape[0]):
        ax.scatter(x[i], y[i], marker='o', s=1000*value[i], c=(1,0,0))
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.tick_params(labelsize=15)  # 设置刻度值字体大小
    labels = ax.get_xticklabels() + ax.get_yticklabels() 
    [label.set_fontname('Times New Roman') for label in labels] # 设置刻度值字体
    # plt.savefig(filename+'.jpg', dpi=300) 
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    main()