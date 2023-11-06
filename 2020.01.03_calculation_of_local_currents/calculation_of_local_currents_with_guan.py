"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/3888
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import guan

def matrix_00(width=10):  # 电极元胞内跃迁，width不赋值时默认为10  
    h00 = np.zeros((width, width))
    for width0 in range(width-1):
        h00[width0, width0+1] = 1
        h00[width0+1, width0] = 1
    return h00


def matrix_01(width=10):  # 电极元胞间跃迁，width不赋值时默认为10
    h01 = np.identity(width)
    return h01


def matrix_LC(width=10, length=300):  # 左电极跳到中心区
    h_LC = np.zeros((width, width*length))
    for width0 in range(width):
        h_LC[width0, width0] = 1
    return h_LC


def matrix_CR(width=10, length=300):  # 中心区跳到右电极
    h_CR = np.zeros((width*length, width))
    for width0 in range(width):
        h_CR[width*(length-1)+width0, width0] = 1
    return h_CR


def matrix_center(width=10, length=300):  # 中心区哈密顿量
    hamiltonian = np.zeros((width*length, width*length))
    for length0 in range(length-1):
        for width0 in range(width):
            hamiltonian[width*length0+width0, width*(length0+1)+width0] = 1  # 长度方向跃迁
            hamiltonian[width*(length0+1)+width0, width*length0+width0] = 1 
    for length0 in range(length):
        for width0 in range(width-1):
            hamiltonian[width*length0+width0, width*length0+width0+1] = 1  # 宽度方向跃迁
            hamiltonian[width*length0+width0+1, width*length0+width0] = 1
    # 中间加势垒
    for j0 in range(6):
        for i0 in range(6): 
            hamiltonian[width*(int(length/2)-3+j0)+int(width/2)-3+i0, width*(int(length/2)-3+j0)+int(width/2)-3+i0]= 1e8
    return hamiltonian


def main():
    start_time = time.time()
    fermi_energy = 0
    width = 60
    length = 100
    h00 = matrix_00(width)
    h01 = matrix_01(width)
    h_LC = matrix_LC(width, length)
    h_CR = matrix_CR(width, length)
    hamiltonian = matrix_center(width, length) 
    
    G_n = guan.electron_correlation_function_green_n_for_local_current(fermi_energy, h00, h01, h_LC, h_CR, hamiltonian)

    direction_x = np.zeros((width, length))
    direction_y = np.zeros((width, length))
    for length0 in range(length-1):
        for width0 in range(width):
            direction_x[width0, length0] = G_n[width*length0+width0, width*(length0+1)+width0]
    for length0 in range(length):
        for width0 in range(width-1):
            direction_y[width0, length0] = G_n[width*length0+width0, width*length0+width0+1]

    X, Y = np.meshgrid(range(length), range(width))
    plt.quiver(X, Y, direction_x, direction_y)
    plt.show()
    end_time = time.time()
    print('运行时间=', end_time-start_time)


if __name__ == '__main__':
    main()