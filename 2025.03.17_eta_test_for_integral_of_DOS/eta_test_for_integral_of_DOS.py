"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45681
"""

import numpy as np

def hamiltonian(width=2, length=2):   # 方格子哈密顿量
    h = np.zeros((width*length, width*length))
    # y方向的跃迁
    for x in range(length):
        for y in range(width-1):
            h[x*width+y, x*width+y+1] = 1
            h[x*width+y+1, x*width+y] = 1
    # x方向的跃迁
    for x in range(length-1):
        for y in range(width):
            h[x*width+y, (x+1)*width+y] = 1
            h[(x+1)*width+y, x*width+y] = 1
    return h

# from numba import jit
# @jit(nopython=True)
def total_DOS_for_Fermi_energy_array(Fermi_energy_array, h, broadening):
    dim_energy = Fermi_energy_array.shape[0]
    dim = h.shape[0]
    total_DOS_array = np.zeros((dim_energy))
    i0 = 0
    for Fermi_energy in Fermi_energy_array:
        green = np.linalg.inv((Fermi_energy+broadening*1j)*np.eye(dim)-h)
        total_DOS = -np.trace(np.imag(green))/np.pi # 通过格林函数求得总态密度
        total_DOS_array[i0] = total_DOS
        i0 += 1
    return total_DOS_array

def main():
    plot_precision = 0.01 # 画图的精度/积分的精度
    Fermi_energy_array = np.arange(-5, 5, plot_precision)
    h = hamiltonian()
    # import time
    # begin_time = time.time()
    for broadening in [0.5, 0.1, 0.01, 0.001, 0.0001]:
        total_DOS_array = total_DOS_for_Fermi_energy_array(Fermi_energy_array, h, broadening)
        sum_up = np.sum(total_DOS_array)*plot_precision
        print(f'Broadening为{broadening}时的积分结果：{sum_up}')
        # import matplotlib.pyplot as plt
        # plt.plot(Fermi_energy_array, total_DOS_array/sum_up, '-o')
        # plt.plot(Fermi_energy_array, total_DOS_array, '-o')  
        # plt.xlabel('Fermi energy')
        # plt.ylabel('Total DOS')
        # plt.show()
    # end_time = time.time()
    # print(end_time-begin_time)

if __name__ == '__main__':
    main()