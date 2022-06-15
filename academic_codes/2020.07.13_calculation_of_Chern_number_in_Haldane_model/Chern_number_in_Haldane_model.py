"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/5133
"""

import numpy as np
from math import *   # 引入pi, cos等
import cmath
import time
import functools  # 使用偏函数functools.partial()


def hamiltonian(k1, k2, M, t1, t2, phi, a=1/sqrt(3)):  # Haldane哈密顿量（a为原子间距，不赋值的话默认为1/sqrt(3)）
    # 初始化为零矩阵
    h0 = np.zeros((2, 2), dtype=complex)
    h1 = np.zeros((2, 2), dtype=complex)
    h2 = np.zeros((2, 2), dtype=complex)

    # 质量项(mass term), 用于打开带隙
    h0[0, 0] = M
    h0[1, 1] = -M

    # 最近邻项
    h1[1, 0] = t1*(cmath.exp(1j*k2*a)+cmath.exp(1j*sqrt(3)/2*k1*a-1j/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j/2*k2*a))
    h1[0, 1] = h1[1, 0].conj()

    # # 最近邻项也可写成这种形式
    # h1[1, 0] = t1+t1*cmath.exp(1j*sqrt(3)/2*k1*a-1j*3/2*k2*a)+t1*cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a)
    # h1[0, 1] = h1[1, 0].conj()

    #次近邻项 # 对应陈数为-1
    h2[0, 0] = t2*cmath.exp(-1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))
    h2[1, 1] = t2*cmath.exp(1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))
    
    # # 次近邻项  # 对应陈数为1
    # h2[0, 0] = t2*cmath.exp(1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))
    # h2[1, 1] = t2*cmath.exp(-1j*phi)*(cmath.exp(1j*sqrt(3)*k1*a)+cmath.exp(-1j*sqrt(3)/2*k1*a+1j*3/2*k2*a)+cmath.exp(-1j*sqrt(3)/2*k1*a-1j*3/2*k2*a))

    matrix = h0 + h1 + h2 + h2.transpose().conj()
    return matrix


def main():
    start_clock = time.perf_counter()
    delta = 0.005
    chern_number = 0  # 陈数初始化
    
    # 几个坐标中常出现的项
    a = 1/sqrt(3)
    aa1 = 4*sqrt(3)*pi/9/a
    aa2 = 2*sqrt(3)*pi/9/a
    bb1 = 2*pi/3/a

    hamiltonian0 = functools.partial(hamiltonian, M=2/3, t1=1, t2=1/3, phi=pi/4, a=a)   # 使用偏函数，固定一些参数

    for kx in np.arange(-aa1, aa1, delta):
        print(kx)
        for ky in np.arange(-bb1, bb1, delta):
            if (-aa2<=kx<=aa2) or (kx>aa2 and -(aa1-kx)*tan(pi/3)<=ky<=(aa1-kx)*tan(pi/3)) or (kx<-aa2 and  -(kx-(-aa1))*tan(pi/3)<=ky<=(kx-(-aa1))*tan(pi/3)):  # 限制在六角格子布里渊区内

                H = hamiltonian0(kx, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H)
                vector = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 价带波函数
            
                H_delta_kx = hamiltonian0(kx+delta, ky) 
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx)
                vector_delta_kx = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]   # 略偏离kx的波函数

                H_delta_ky = hamiltonian0(kx, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_ky)
                vector_delta_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离ky的波函数
                
                H_delta_kx_ky = hamiltonian0(kx+delta, ky+delta)  
                eigenvalue, eigenvector = np.linalg.eig(H_delta_kx_ky)
                vector_delta_kx_ky = eigenvector[:, np.argsort(np.real(eigenvalue))[0]]  # 略偏离kx和ky的波函数
                
                Ux = np.dot(np.conj(vector), vector_delta_kx)/abs(np.dot(np.conj(vector), vector_delta_kx))
                Uy = np.dot(np.conj(vector), vector_delta_ky)/abs(np.dot(np.conj(vector), vector_delta_ky))
                Ux_y = np.dot(np.conj(vector_delta_ky), vector_delta_kx_ky)/abs(np.dot(np.conj(vector_delta_ky), vector_delta_kx_ky))
                Uy_x = np.dot(np.conj(vector_delta_kx), vector_delta_kx_ky)/abs(np.dot(np.conj(vector_delta_kx), vector_delta_kx_ky))

                F = cmath.log(Ux*Uy_x*(1/Ux_y)*(1/Uy))

                # 陈数(chern number)
                chern_number = chern_number + F

    chern_number = chern_number/(2*pi*1j)
    print('Chern number = ', chern_number)
    end_clock = time.perf_counter()
    print('CPU执行时间(min)=', (end_clock-start_clock)/60)


if __name__ == '__main__':
    main()