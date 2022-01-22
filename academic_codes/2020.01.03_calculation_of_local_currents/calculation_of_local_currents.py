"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/3888
"""

import numpy as np
import matplotlib.pyplot as plt
import time


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
    G_n = Green_n(fermi_energy+1j*1e-9, h00, h01, width, length)
    # 下面是提取数据并画图
    direction_x = np.zeros((width, length))
    direction_y = np.zeros((width, length))
    for length0 in range(length-1):
        for width0 in range(width):
            direction_x[width0, length0] = G_n[width*length0+width0, width*(length0+1)+width0]
    for length0 in range(length):
        for width0 in range(width-1):
            direction_y[width0, length0] = G_n[width*length0+width0, width*length0+width0+1]
    # print(direction_x)
    # print(direction_y)
    X, Y = np.meshgrid(range(length), range(width))
    plt.quiver(X, Y, direction_x, direction_y)
    plt.show()
    end_time = time.time()
    print('运行时间=', end_time-start_time)



def transfer_matrix(fermi_energy, h00, h01, dim):   # 转移矩阵T。dim是传递矩阵h00和h01的维度
    transfer = np.zeros((2*dim, 2*dim), dtype=complex)
    transfer[0:dim, 0:dim] = np.dot(np.linalg.inv(h01), fermi_energy*np.identity(dim)-h00)   # np.dot()等效于np.matmul()
    transfer[0:dim, dim:2*dim] = np.dot(-1*np.linalg.inv(h01), h01.transpose().conj())
    transfer[dim:2*dim, 0:dim] = np.identity(dim)
    transfer[dim:2*dim, dim:2*dim] = 0  # a:b代表 a <= x < b
    return transfer  # 返回转移矩阵


def green_function_lead(fermi_energy, h00, h01, dim):  # 电极的表面格林函数
    transfer = transfer_matrix(fermi_energy, h00, h01, dim)
    eigenvalue, eigenvector = np.linalg.eig(transfer)
    ind = np.argsort(np.abs(eigenvalue))
    temp = np.zeros((2*dim, 2*dim))*(1+0j)
    i0 = 0
    for ind0 in ind:
        temp[:, i0] = eigenvector[:, ind0]
        i0 += 1
    s1 = temp[dim:2*dim, 0:dim]
    s2 = temp[0:dim, 0:dim]
    s3 = temp[dim:2*dim, dim:2*dim]
    s4 = temp[0:dim, dim:2*dim]
    right_lead_surface = np.linalg.inv(fermi_energy*np.identity(dim)-h00-np.dot(np.dot(h01, s2), np.linalg.inv(s1)))
    left_lead_surface = np.linalg.inv(fermi_energy*np.identity(dim)-h00-np.dot(np.dot(h01.transpose().conj(), s3), np.linalg.inv(s4)))
    return right_lead_surface, left_lead_surface  # 返回右电极的表面格林函数和左电极的表面格林函数


def self_energy_lead(fermi_energy, h00, h01, width, length):  # 电极的自能
    h_LC = matrix_LC(width, length)
    h_CR = matrix_CR(width, length)
    right_lead_surface, left_lead_surface = green_function_lead(fermi_energy, h00, h01, width)
    right_self_energy = np.dot(np.dot(h_CR, right_lead_surface), h_CR.transpose().conj())
    left_self_energy = np.dot(np.dot(h_LC.transpose().conj(), left_lead_surface), h_LC)
    return right_self_energy, left_self_energy  # 返回右电极的自能和左电极的自能


def Green_n(fermi_energy, h00, h01, width, length):  # 计算G_n
    right_self_energy, left_self_energy = self_energy_lead(fermi_energy, h00, h01, width, length)
    hamiltonian = matrix_center(width, length)
    green = np.linalg.inv(fermi_energy*np.identity(width*length)-hamiltonian-left_self_energy-right_self_energy)
    right_self_energy = (right_self_energy - right_self_energy.transpose().conj())*1j
    left_self_energy = (left_self_energy - left_self_energy.transpose().conj())*1j
    G_n = np.imag(np.dot(np.dot(green, left_self_energy), green.transpose().conj()))
    return G_n


if __name__ == '__main__':
    main()