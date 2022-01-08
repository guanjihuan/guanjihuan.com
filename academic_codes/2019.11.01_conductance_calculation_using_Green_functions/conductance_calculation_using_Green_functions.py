"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/948
"""

import numpy as np
import matplotlib.pyplot as plt
import copy
import time


def matrix_00(width=10):  # 不赋值时默认为10
    h00 = np.zeros((width, width))
    for width0 in range(width-1):
        h00[width0, width0+1] = 1
        h00[width0+1, width0] = 1
    return h00


def matrix_01(width=10):  # 不赋值时默认为10
    h01 = np.identity(width)
    return h01


def main():
    start_time = time.time()
    h00 = matrix_00(width=5)
    h01 = matrix_01(width=5)
    fermi_energy_array = np.arange(-4, 4, .01)
    plot_conductance_energy(fermi_energy_array, h00, h01)
    end_time = time.time()
    print('运行时间=', end_time-start_time)


def plot_conductance_energy(fermi_energy_array, h00, h01):  # 画电导与费米能关系图
    dim = fermi_energy_array.shape[0]
    cond = np.zeros(dim)
    i0 = 0
    for fermi_energy0 in fermi_energy_array:
        cond0 = np.real(conductance(fermi_energy0 + 1e-12j, h00, h01))
        cond[i0] = cond0
        i0 += 1
    plt.plot(fermi_energy_array, cond, '-k')
    plt.show()


def transfer_matrix(fermi_energy, h00, h01, dim):   # 转移矩阵T。dim是传递矩阵h00和h01的维度
    transfer = np.zeros((2*dim, 2*dim), dtype=complex)
    transfer[0:dim, 0:dim] = np.dot(np.linalg.inv(h01), fermi_energy*np.identity(dim)-h00)   # np.dot()等效于np.matmul()
    transfer[0:dim, dim:2*dim] = np.dot(-1*np.linalg.inv(h01), h01.transpose().conj())
    transfer[dim:2*dim, 0:dim] = np.identity(dim)
    transfer[dim:2*dim, dim:2*dim] = 0  # a:b代表 a <= x < b，左闭右开
    return transfer  # 返回转移矩阵


def green_function_lead(fermi_energy, h00, h01, dim):  # 电极的表面格林函数
    transfer = transfer_matrix(fermi_energy, h00, h01, dim)
    eigenvalue, eigenvector = np.linalg.eig(transfer)
    ind = np.argsort(np.abs(eigenvalue))
    temp = np.zeros((2*dim, 2*dim), dtype=complex)
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


def self_energy_lead(fermi_energy, h00, h01, dim):  # 电极的自能
    right_lead_surface, left_lead_surface = green_function_lead(fermi_energy, h00, h01, dim)
    right_self_energy = np.dot(np.dot(h01, right_lead_surface), h01.transpose().conj())
    left_self_energy = np.dot(np.dot(h01.transpose().conj(), left_lead_surface), h01)
    return right_self_energy, left_self_energy  # 返回右边电极自能和左边电极自能


def conductance(fermi_energy, h00, h01, nx=300):  # 计算电导
    dim = h00.shape[0]
    right_self_energy, left_self_energy = self_energy_lead(fermi_energy, h00, h01, dim)
    for ix in range(nx):
        if ix == 0:
            green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00-left_self_energy)
            green_0n_n = copy.deepcopy(green_nn_n)  # 如果直接用等于，两个变量会指向相同的id，改变一个值，另外一个值可能会发生改变，容易出错，所以要用上这个COPY
        elif ix != nx-1:
            green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00-np.dot(np.dot(h01.transpose().conj(), green_nn_n), h01))
            green_0n_n = np.dot(np.dot(green_0n_n, h01), green_nn_n)
        else:
            green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00-np.dot(np.dot(h01.transpose().conj(), green_nn_n), h01)-right_self_energy)
            green_0n_n = np.dot(np.dot(green_0n_n, h01), green_nn_n)
    gamma_right = (right_self_energy - right_self_energy.transpose().conj())*(0+1j)
    gamma_left = (left_self_energy - left_self_energy.transpose().conj())*(0+1j)
    transmission = np.trace(np.dot(np.dot(np.dot(gamma_left, green_0n_n), gamma_right), green_0n_n.transpose().conj()))
    return transmission  # 返回电导值


if __name__ == '__main__':
    main()
