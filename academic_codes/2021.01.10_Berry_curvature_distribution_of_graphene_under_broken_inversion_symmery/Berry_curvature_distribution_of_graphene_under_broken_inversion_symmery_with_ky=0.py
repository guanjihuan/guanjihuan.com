"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/8536
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *  
import cmath
import time


def hamiltonian(k1, k2, t1=2.82*sqrt(3)/2, a=1/sqrt(3)):  # 石墨烯哈密顿量(a为原子间距，不赋值的话默认为1/sqrt(3)）
    h = np.zeros((2, 2))*(1+0j)
    h[0, 0] = 0.28/2
    h[1, 1] = -0.28/2
    h[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h[0, 1] = h[1, 0].conj()
    return h


def main():
    start_time = time.time()
    n = 2000  # 取点密度
    delta = 1e-9  # 求导的偏离量
    for band in range(2):
        F_all = []  # 贝里曲率
        for kx in np.linspace(-2*pi, 2*pi, n):
            for ky in [0]: # 这里只考虑ky=0对称轴上的情况 # np.linspace(-pi, pi, n):
                H = hamiltonian(kx, ky)
                eigenvalue, eigenvector = np.linalg.eig(H)
                vector = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]  # 价带波函数
                # print(np.argsort(np.real(eigenvalue))[0])  # 排序索引（从小到大）
                # print(eigenvalue)  # 排序前的本征值
                # print(np.sort(np.real(eigenvalue)))  # 排序后的本征值（从小到大）
            
                H_delta_kx = hamiltonian(kx+delta, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
                vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]   # 略偏离kx的波函数
                # vector_delta_kx = find_vector_with_the_same_gauge(vector_delta_kx, vector)  # 如果波函数不连续需要使用这个

                H_delta_ky = hamiltonian(kx, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
                vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]  # 略偏离ky的波函数
                # vector_delta_ky = find_vector_with_the_same_gauge(vector_delta_ky, vector)  # 如果波函数不连续需要使用这个

                H_delta_kx_ky = hamiltonian(kx+delta, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx_ky)
                vector_delta_kx_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[band]]  # 略偏离kx和ky的波函数
                # vector_delta_kx_ky = find_vector_with_the_same_gauge(vector_delta_kx_ky, vector)  # 如果波函数不连续需要使用这个

                # 价带的波函数的贝里联络(berry connection) # 求导后内积
                A_x = np.dot(vector.transpose().conj(), (vector_delta_kx-vector)/delta)   # 贝里联络Ax（x分量）
                A_y = np.dot(vector.transpose().conj(), (vector_delta_ky-vector)/delta)   # 贝里联络Ay（y分量）
                
                A_x_delta_ky = np.dot(vector_delta_ky.transpose().conj(), (vector_delta_kx_ky-vector_delta_ky)/delta)  # 略偏离ky的贝里联络Ax
                A_y_delta_kx = np.dot(vector_delta_kx.transpose().conj(), (vector_delta_kx_ky-vector_delta_kx)/delta)  # 略偏离kx的贝里联络Ay

                # 贝里曲率(berry curvature)
                F = ((A_y_delta_kx-A_y)/delta-(A_x_delta_ky-A_x)/delta)*1j
                # print(F)
                F_all = np.append(F_all,[F], axis=0) 
        plt.plot(np.linspace(-2*pi, 2*pi, n)/pi, np.real(F_all))
        plt.xlabel('k_x (pi)')
        plt.ylabel('Berry curvature')
        if band==0:
            plt.title('Valence Band')
        else:
            plt.title('Conductance Band')
        plt.show()
    end_time = time.time()
    print('运行时间(min)=', (end_time-start_time)/60)


def find_vector_with_the_same_gauge(vector_1, vector_0):
    # 寻找近似的同一的规范
    phase_1_pre = 0
    phase_2_pre = pi
    n_test = 10001
    for i0 in range(n_test):
        test_1 = np.sum(np.abs(vector_1*cmath.exp(1j*phase_1_pre) - vector_0))
        test_2 = np.sum(np.abs(vector_1*cmath.exp(1j*phase_2_pre) - vector_0))
        if test_1 < 1e-9:
            phase = phase_1_pre
            # print('Done with i0=', i0)
            break
        if i0 == n_test-1:
            phase = phase_1_pre
            print('Gauge Not Found with i0=', i0)
        if test_1 < test_2:
            if i0 == 0:
                phase_1 = phase_1_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_1_pre+(phase_2_pre-phase_1_pre)/2
            else:
                phase_1 = phase_1_pre
                phase_2 = phase_1_pre+(phase_2_pre-phase_1_pre)/2
        else:
            if i0 == 0:
                phase_1 = phase_2_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_2_pre+(phase_2_pre-phase_1_pre)/2
            else:
                phase_1 = phase_2_pre-(phase_2_pre-phase_1_pre)/2
                phase_2 = phase_2_pre 
        phase_1_pre = phase_1
        phase_2_pre = phase_2
           
    vector_1 = vector_1*cmath.exp(1j*phase)
    # print('二分查找找到的规范=', phase)   
    return vector_1



if __name__ == '__main__':
    main()