"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/7516
"""

import numpy as np
from math import *   # 引入pi, cos等
import cmath
import time


def hamiltonian(kx, ky):  # 量子反常霍尔QAH模型（该参数对应的陈数为2）
    t1 = 1.0
    t2 = 1.0
    t3 = 0.5
    m = -1.0
    matrix = np.zeros((2, 2))*(1+0j)
    matrix[0, 1] = 2*t1*cos(kx)-1j*2*t1*cos(ky)
    matrix[1, 0] = 2*t1*cos(kx)+1j*2*t1*cos(ky)
    matrix[0, 0] = m+2*t3*sin(kx)+2*t3*sin(ky)+2*t2*cos(kx+ky)
    matrix[1, 1] = -(m+2*t3*sin(kx)+2*t3*sin(ky)+2*t2*cos(kx+ky))
    return matrix


def main():
    start_time = time.time()
    n = 100  # 积分密度
    delta = 1e-9  # 求导的偏离量
    chern_number = 0  # 陈数初始化
    for kx in np.arange(-pi, pi, 2*pi/n):
        for ky in np.arange(-pi, pi, 2*pi/n):
            H = hamiltonian(kx, ky)
            eigenvalue, eigenvector = np.linalg.eig(H)
            vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 价带波函数
           
            H_delta_kx = hamiltonian(kx+delta, ky) 
            eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
            vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]   # 略偏离kx的波函数

            H_delta_ky = hamiltonian(kx, ky+delta)  
            eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
            vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离ky的波函数

            H_delta_kx_ky = hamiltonian(kx+delta, ky+delta)  
            eigenvalue, eigenvector = np.linalg.eig(H_delta_kx_ky)
            vector_delta_kx_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离kx和ky的波函数

            # vector = vector*cmath.exp(-1j*1)
            # vector_delta_kx = vector_delta_kx*cmath.exp(-1j*1)
            # vector_delta_ky = vector_delta_ky*cmath.exp(-1j*1)
            # vector_delta_kx_ky = vector_delta_kx_ky*cmath.exp(-1j*(1+1e-8))
            

            rand = np.random.uniform(-pi, pi)
            vector_delta_kx_ky = vector_delta_kx_ky*cmath.exp(-1j*rand)

            # 寻找近似的同一的规范
            phase_1_pre = 0
            phase_2_pre = pi
            n_test = 10001
            for i0 in range(n_test):
                test_1 = np.sum(np.abs(vector_delta_kx_ky*cmath.exp(1j*phase_1_pre) - vector))
                test_2 = np.sum(np.abs(vector_delta_kx_ky*cmath.exp(1j*phase_2_pre) - vector))
                if test_1 < 1e-6:
                    phase = phase_1_pre
                    print('Done with i0=', i0)
                    break
                if i0 == n_test-1:
                    phase = phase_1_pre
                    print('Not Found with i0=', i0)
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
                
            vector_delta_kx_ky = vector_delta_kx_ky*cmath.exp(1j*phase)
            print('随机的规范=', rand)  # 可注释掉
            print('二分查找找到的规范=', phase)   # 可注释掉
            print()   # 可注释掉


            # 价带的波函数的贝里联络(berry connection) # 求导后内积
            A_x = np.dot(vector.transpose().conj(), (vector_delta_kx-vector)/delta)   # 贝里联络Ax（x分量）
            A_y = np.dot(vector.transpose().conj(), (vector_delta_ky-vector)/delta)   # 贝里联络Ay（y分量）
            
            A_x_delta_ky = np.dot(vector_delta_ky.transpose().conj(), (vector_delta_kx_ky-vector_delta_ky)/delta)  # 略偏离ky的贝里联络Ax
            A_y_delta_kx = np.dot(vector_delta_kx.transpose().conj(), (vector_delta_kx_ky-vector_delta_kx)/delta)  # 略偏离kx的贝里联络Ay

            # 贝里曲率(berry curvature)
            F = (A_y_delta_kx-A_y)/delta-(A_x_delta_ky-A_x)/delta

            # 陈数(chern number)
            chern_number = chern_number + F*(2*pi/n)**2
    chern_number = chern_number/(2*pi*1j)
    print('Chern number = ', chern_number)
    end_time = time.time()
    print('运行时间(min)=', (end_time-start_time)/60)


if __name__ == '__main__':
    main()
