"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4622
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False   #用来正常显示负号


def hamiltonian(width=8, length=8):   # 石墨烯格子的哈密顿量。这里width要求为4的倍数
    h = np.zeros((width*length, width*length))
    # y方向的跃迁
    for x in range(length):   
        for y in range(width-1):
            h[x*width+y, x*width+y+1] = 1
            h[x*width+y+1, x*width+y] = 1

    # x方向的跃迁
    for x in range(length-1):  
        for y in range(width):
            if np.mod(y, 4)==0:
                h[x*width+y+1, (x+1)*width+y] = 1
                h[(x+1)*width+y, x*width+y+1] = 1

                h[x*width+y+2, (x+1)*width+y+3] = 1
                h[(x+1)*width+y+3, x*width+y+2] = 1

    return h
    

def main():
    plot_precision = 0.01  # 画图的精度
    Fermi_energy_array = np.arange(-5, 5, plot_precision)  # 计算中取的费米能Fermi_energy组成的数组
    dim_energy = Fermi_energy_array.shape[0]   # 需要计算的费米能的个数
    total_DOS_array = np.zeros((dim_energy))   # 计算结果（总态密度total_DOS）放入该数组中
    h = hamiltonian()  # 体系的哈密顿量
    dim = h.shape[0]   # 哈密顿量的维度
    i0 = 0
    for Fermi_energy in Fermi_energy_array:
        print(Fermi_energy)  # 查看计算的进展情况
        green = np.linalg.inv((Fermi_energy+0.1j)*np.eye(dim)-h)   # 体系的格林函数
        total_DOS = -np.trace(np.imag(green))/pi    # 通过格林函数求得总态密度
        total_DOS_array[i0] = total_DOS   # 记录每个Fermi_energy对应的总态密度
        i0 += 1
    sum_up = np.sum(total_DOS_array)*plot_precision    # 用于图像归一化
    plt.plot(Fermi_energy_array, total_DOS_array/sum_up, '-')   # 画DOS(E)图像
    plt.xlabel('费米能')
    plt.ylabel('总态密度')
    plt.show()


if __name__ == '__main__':
    main()
