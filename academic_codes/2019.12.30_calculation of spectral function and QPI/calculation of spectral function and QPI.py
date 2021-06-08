"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/3785
"""

import numpy as np
from math import *
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time


def green_function(fermi_energy, k1, k2, hamiltonian):  # 计算格林函数
    matrix0 = hamiltonian(k1, k2)
    dim = matrix0.shape[0]
    green = np.linalg.inv(fermi_energy * np.identity(dim) - matrix0)
    return green


def spectral_function(fermi_energy, k1, k2, hamiltonian):  # 计算谱函数
    dim1 = k1.shape[0]
    dim2 = k2.shape[0]
    spectrum = np.zeros((dim1, dim2))
    i0 = 0
    for k10 in k1:
        j0 = 0
        for k20 in k2:
            green = green_function(fermi_energy, k10, k20, hamiltonian)
            spectrum[i0, j0] = (np.imag(green[0,0])+np.imag(green[2,2]))/(-pi)
            j0 += 1
        i0 += 1
    # print(spectrum)
    print()
    print('Spectral function显示的网格点 =', k1.shape[0], '*', k1.shape[0], '; 步长 =', k1[1] - k1[0])
    print()
    return spectrum


def qpi(fermi_energy, q1, q2, hamiltonian, potential_i):   # 计算QPI
    dim = hamiltonian(0, 0).shape[0]
    ki1 = np.arange(-pi, pi, 0.01)   # 计算gamma_0时，k的积分密度
    ki2 = np.arange(-pi, pi, 0.01)    
    print('gamma_0的积分网格点 =', ki1.shape[0], '*', ki1.shape[0], '; 步长 =', ki1[1] - ki1[0])
    gamma_0 = integral_of_green(fermi_energy, ki1, ki2, hamiltonian)/np.square(2*pi)
    t_matrix = np.dot(np.linalg.inv(np.identity(dim)-np.dot(potential_i, gamma_0)), potential_i)
    ki1 = np.arange(-pi, pi, 0.06)   # 计算induced_local_density时，k的积分密度
    ki2 = np.arange(-pi, pi, 0.06) 
    print('局域态密度变化的积分网格点 =', ki1.shape[0], '*', ki1.shape[0], '; 步长 =', ki1[1] - ki1[0])
    print('QPI显示的网格点 =', q1.shape[0], '*', q1.shape[0], '; 步长 =', q1[1] - q1[0])
    step_length = ki1[1] - ki1[0]
    induced_local_density = np.zeros((q1.shape[0], q2.shape[0]))*(1+0j)
    print()
    i0 = 0
    for q10 in q1:
        print('i0=', i0)
        j0 = 0
        for q20 in q2:
            for ki10 in ki1: 
                for ki20 in ki2:
                    green_01 = green_function(fermi_energy, ki10, ki20, hamiltonian)
                    green_02 = green_function(fermi_energy, ki10+q10, ki20+q20, hamiltonian)
                    induced_green = np.dot(np.dot(green_01, t_matrix), green_02)
                    temp = induced_green[0, 0]-induced_green[0, 0].conj()+induced_green[2, 2]-induced_green[2, 2].conj() 
                    induced_local_density[i0, j0] = induced_local_density[i0, j0]+temp*np.square(step_length)
            j0 += 1
        i0 += 1
        write_matrix_k1_k2(q1, q2, np.real(induced_local_density*1j/np.square(2*pi)/(2*pi)), 'QPI')  # 数据写入文件（临时写入，会被多次替代）
    induced_local_density = np.real(induced_local_density*1j/np.square(2*pi)/(2*pi))
    return induced_local_density


def integral_of_green(fermi_energy, ki1, ki2, hamiltonian):  # 在计算QPI时需要对格林函数积分
    dim = hamiltonian(0, 0).shape[0]
    integral_value = np.zeros((dim, dim))*(1+0j)
    step_length = ki1[1]-ki1[0]
    for ki10 in ki1:
        for ki20 in ki2:
            green = green_function(fermi_energy, ki10, ki20, hamiltonian)
            integral_value = integral_value+green*np.square(step_length)
    return integral_value


def write_matrix_k1_k2(x1, x2, value, filename='matrix_k1_k2'):  # 把矩阵数据写入文件（格式化输出）
    with open(filename+'.txt', 'w') as f:
        np.set_printoptions(suppress=True)  # 取消输出科学记数法
        f.write('0           ')
        for x10 in x1:
            f.write(str(x10)+'   ')
        f.write('\n')
        i0 = 0
        for x20 in x2:
            f.write(str(x20))
            for j0 in range(x1.shape[0]):
                f.write('  '+str(value[i0, j0])+'   ')
            f.write('\n')
            i0 += 1


def plot_contour(x1, x2, value, filename='contour'):  # 直接画出contour图像（保存图像）
    plt.contourf(x1, x2, value)  #, cmap=plt.cm.hot)
    plt.savefig(filename+'.eps')
    # plt.show()


def hamiltonian(kx, ky):   # 体系的哈密顿量
    t1 = -1; t2 = 1.3;  t3 = -0.85; t4 = -0.85; delta_0 = 0.1; mu = 1.54
    epsilon_x = -2*t1*cos(kx)-2*t2*cos(ky)-4*t3*cos(kx)*cos(ky)
    epsilon_y = -2*t1*cos(ky)-2*t2*cos(kx)-4*t3*cos(kx)*cos(ky)
    epsilon_xy = -4*t4*sin(kx)*sin(ky)
    delta_1 = delta_0*cos(kx)*cos(ky)
    delta_2 = delta_0*cos(kx)*cos(ky)
    h = np.zeros((4, 4))
    h[0, 0] = epsilon_x-mu
    h[1, 1] = -epsilon_x+mu
    h[2, 2] = epsilon_y-mu
    h[3, 3] = -epsilon_y+mu

    h[0, 1] = delta_1
    h[1, 0] = delta_1
    h[0, 2] = epsilon_xy
    h[2, 0] = epsilon_xy
    h[0, 3] = 0
    h[3, 0] = 0

    h[1, 2] = 0
    h[2, 1] = 0
    h[1, 3] = -epsilon_xy
    h[3, 1] = -epsilon_xy

    h[2, 3] = delta_2
    h[3, 2] = delta_2
    return h


def main():    # 主程序
    start_clock = time.perf_counter()
    fermi_energy = 0.07  # 费米能
    energy_broadening_width = 0.005  # 展宽
    k1 = np.arange(-pi, pi, 0.01)   # 谱函数的图像精度
    k2 = np.arange(-pi, pi, 0.01)   
    spectrum = spectral_function(fermi_energy+energy_broadening_width*1j, k1, k2, hamiltonian)   # 调用谱函数子程序
    write_matrix_k1_k2(k1, k2, spectrum, 'Spectral_function')  # 把谱函数的数据写入文件
    # plot_contour(k1, k2, spectrum, 'Spectral_function')  # 直接显示谱函数的图像（保存图像）

    q1 = np.arange(-pi, pi, 0.01)   # QPI数的图像精度
    q2 = np.arange(-pi, pi, 0.01) 
    potential_i = (0.4+0j)*np.identity(hamiltonian(0, 0).shape[0])  # 杂质势
    potential_i[1, 1] = - potential_i[1, 1]   # for nonmagnetic
    potential_i[3, 3] = - potential_i[3, 3] 
    induced_local_density = qpi(fermi_energy+energy_broadening_width*1j, q1, q2, hamiltonian, potential_i)  # 调用QPI子程序
    write_matrix_k1_k2(q1, q2, induced_local_density, 'QPI')  # 把QPI数据写入文件（这里用的方法是计算结束后一次性把数据写入）
    # plot_contour(q1, q2, induced_local_density, 'QPI')  # 直接显示QPI图像（保存图像）
    end_clock = time.perf_counter()
    print('CPU执行时间=', end_clock - start_clock)


if __name__ == '__main__':
    main()
