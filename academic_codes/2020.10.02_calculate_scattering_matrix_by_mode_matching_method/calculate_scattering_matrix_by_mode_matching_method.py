"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6352
"""

import numpy as np
import matplotlib.pyplot as plt
from math import *
import copy
import time
# import os
# os.chdir('D:/data') 


def main():
    start_time = time.time()
    h00 = matrix_00()  # 方格子模型
    h01 = matrix_01()  # 方格子模型
    fermi_energy = 0.1
    write_transmission_matrix(fermi_energy, h00, h01)  # 输出无散射的散射矩阵
    end_time = time.time()
    print('运行时间=', end_time - start_time, '秒')


def matrix_00(width=4): 
    h00 = np.zeros((width, width))
    for width0 in range(width-1):
        h00[width0, width0+1] = 1
        h00[width0+1, width0] = 1
    return h00


def matrix_01(width=4): 
    h01 = np.identity(width)
    return h01


def transfer_matrix(fermi_energy, h00, h01, dim):  # 转移矩阵
    transfer = np.zeros((2*dim, 2*dim))*(0+0j) 
    transfer[0:dim, 0:dim] = np.dot(np.linalg.inv(h01), fermi_energy*np.identity(dim)-h00) 
    transfer[0:dim, dim:2*dim] = np.dot(-1*np.linalg.inv(h01), h01.transpose().conj())
    transfer[dim:2*dim, 0:dim] = np.identity(dim)
    transfer[dim:2*dim, dim:2*dim] = 0
    return transfer


def complex_wave_vector(fermi_energy, h00, h01, dim):  # 获取通道的复数波矢，并按照波矢的实部Re(k)排序
    transfer = transfer_matrix(fermi_energy, h00, h01, dim)
    eigenvalue, eigenvector = np.linalg.eig(transfer)
    k_channel = np.log(eigenvalue)/1j
    ind = np.argsort(np.real(k_channel))
    k_channel = np.sort(k_channel)
    temp = np.zeros((2*dim, 2*dim))*(1+0j)
    temp2 = np.zeros((2*dim))*(1+0j)
    i0 = 0
    for ind0 in ind:
        temp[:, i0] = eigenvector[:, ind0]
        temp2[i0] = eigenvalue[ind0]
        i0 += 1
    eigenvalue = copy.deepcopy(temp2)
    temp = normalization_of_eigenvector(temp[0:dim, :], dim)
    velocity = np.zeros((2*dim))*(1+0j)
    for dim0 in range(2*dim):
        velocity[dim0] = eigenvalue[dim0]*np.dot(np.dot(temp[0:dim, :].transpose().conj(), h01),temp[0:dim, :])[dim0, dim0]
    velocity = -2*np.imag(velocity)
    eigenvector = copy.deepcopy(temp) 
    return k_channel, velocity, eigenvalue, eigenvector  # 返回通道的对应的波矢、费米速度、本征值、本征态


def normalization_of_eigenvector(eigenvector, dim):  # 波函数归一化
    factor = np.zeros(2*dim)*(1+0j)
    for dim0 in range(dim):
        factor = factor+np.square(np.abs(eigenvector[dim0, :]))
    for dim0 in range(2*dim):
        eigenvector[:, dim0] = eigenvector[:, dim0]/np.sqrt(factor[dim0])
    return eigenvector


def calculation_of_lambda_u_f(fermi_energy, h00, h01, dim):   # 对所有通道（包括active和evanescent）进行分类，并计算F
    k_channel, velocity, eigenvalue, eigenvector = complex_wave_vector(fermi_energy, h00, h01, dim)
    ind_right_active = 0; ind_right_evanescent = 0; ind_left_active = 0; ind_left_evanescent = 0
    k_right = np.zeros(dim)*(1+0j); k_left = np.zeros(dim)*(1+0j)
    velocity_right = np.zeros(dim)*(1+0j); velocity_left = np.zeros(dim)*(1+0j)
    lambda_right = np.zeros(dim)*(1+0j); lambda_left = np.zeros(dim)*(1+0j)
    u_right = np.zeros((dim, dim))*(1+0j); u_left = np.zeros((dim, dim))*(1+0j)
    for dim0 in range(2*dim):
        if_active = if_active_channel(k_channel[dim0])
        direction = direction_of_channel(velocity[dim0], k_channel[dim0])
        if direction == 1:      # 向右运动的通道
            if if_active == 1:  # 可传播通道（active channel）
                k_right[ind_right_active] = k_channel[dim0]
                velocity_right[ind_right_active] = velocity[dim0]
                lambda_right[ind_right_active] = eigenvalue[dim0]
                u_right[:, ind_right_active] = eigenvector[:, dim0]
                ind_right_active += 1
            else:               # 衰减通道（evanescent channel）
                k_right[dim-1-ind_right_evanescent] = k_channel[dim0]
                velocity_right[dim-1-ind_right_evanescent] = velocity[dim0]
                lambda_right[dim-1-ind_right_evanescent] = eigenvalue[dim0]
                u_right[:, dim-1-ind_right_evanescent] = eigenvector[:, dim0]
                ind_right_evanescent += 1
        else:                   # 向左运动的通道
            if if_active == 1:  # 可传播通道（active channel）
                k_left[ind_left_active] = k_channel[dim0]
                velocity_left[ind_left_active] = velocity[dim0]
                lambda_left[ind_left_active] = eigenvalue[dim0]
                u_left[:, ind_left_active] = eigenvector[:, dim0]
                ind_left_active += 1
            else:               # 衰减通道（evanescent channel）
                k_left[dim-1-ind_left_evanescent] = k_channel[dim0]
                velocity_left[dim-1-ind_left_evanescent] = velocity[dim0]
                lambda_left[dim-1-ind_left_evanescent] = eigenvalue[dim0]
                u_left[:, dim-1-ind_left_evanescent] = eigenvector[:, dim0]
                ind_left_evanescent += 1
    lambda_matrix_right = np.diag(lambda_right)
    lambda_matrix_left = np.diag(lambda_left)
    f_right = np.dot(np.dot(u_right, lambda_matrix_right), np.linalg.inv(u_right))
    f_left = np.dot(np.dot(u_left, lambda_matrix_left), np.linalg.inv(u_left))
    return k_right, k_left, velocity_right, velocity_left, f_right, f_left, u_right, u_left, ind_right_active 
    # 分别返回向右和向左的运动的波矢k、费米速度velocity、F值、U值、可向右传播的通道数


def if_active_channel(k_channel):  # 判断是可传播通道还是衰减通道
    if np.abs(np.imag(k_channel)) < 1e-7:
        if_active = 1
    else:
        if_active = 0
    return if_active


def direction_of_channel(velocity, k_channel):  # 判断通道对应的费米速度方向
    if if_active_channel(k_channel) == 1:
        direction = np.sign(velocity)
    else:
        direction = np.sign(np.imag(k_channel))
    return direction


def calculation_of_green_function(fermi_energy, h00, h01, dim, scatter_type=0, scatter_intensity=0.2, scatter_length=20):  # 计算格林函数
    k_right, k_left, velocity_right, velocity_left, f_right, f_left, u_right, u_left, ind_right_active = calculation_of_lambda_u_f(fermi_energy, h00, h01, dim)
    right_self_energy = np.dot(h01, f_right)
    left_self_energy = np.dot(h01.transpose().conj(), np.linalg.inv(f_left))
    nx = 300
    for nx0 in range(nx):
        if nx0 == 0:
            green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00-left_self_energy)
            green_00_n = copy.deepcopy(green_nn_n)
            green_0n_n = copy.deepcopy(green_nn_n)
            green_n0_n = copy.deepcopy(green_nn_n)
        elif nx0 != nx-1:
            if scatter_type == 0:  # 无散射
                green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00-np.dot(np.dot(h01.transpose().conj(), green_nn_n), h01))
            elif scatter_type == 1:  # 势垒散射
                h00_scatter = h00 + scatter_intensity * np.identity(dim)
                if int(nx/2)-int(scatter_length/2) <= nx0 < int(nx/2)+int((scatter_length+1)/2):
                    green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00_scatter - np.dot(np.dot(h01.transpose().conj(), green_nn_n), h01))
                else:      
                    green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00-np.dot(np.dot(h01.transpose().conj(), green_nn_n), h01))   
        else:
            green_nn_n = np.linalg.inv(fermi_energy*np.identity(dim)-h00-right_self_energy-np.dot(np.dot(h01.transpose().conj(), green_nn_n), h01))

        green_00_n = green_00_n+np.dot(np.dot(np.dot(np.dot(green_0n_n, h01), green_nn_n), h01.transpose().conj()), green_n0_n)
        green_0n_n = np.dot(np.dot(green_0n_n, h01), green_nn_n)
        green_n0_n = np.dot(np.dot(green_nn_n, h01.transpose().conj()), green_n0_n)
    return green_00_n, green_n0_n, k_right, k_left, velocity_right, velocity_left, f_right, f_left, u_right, u_left, ind_right_active


def transmission_with_detailed_modes(fermi_energy, h00, h01, scatter_type=0, scatter_intensity=0.2, scatter_length=20):  # 计算散射矩阵
    dim = h00.shape[0]
    green_00_n, green_n0_n, k_right, k_left, velocity_right, velocity_left, f_right, f_left, u_right, u_left, ind_right_active = calculation_of_green_function(fermi_energy, h00, h01, dim, scatter_type, scatter_intensity, scatter_length)
    temp = np.dot(h01.transpose().conj(), np.linalg.inv(f_right)-np.linalg.inv(f_left))
    transmission_matrix = np.dot(np.dot(np.linalg.inv(u_right), np.dot(green_n0_n, temp)), u_right) 
    reflection_matrix = np.dot(np.dot(np.linalg.inv(u_left), np.dot(green_00_n, temp)-np.identity(dim)), u_right)
    for dim0 in range(dim):
        for dim1 in range(dim):
            if_active = if_active_channel(k_right[dim0])*if_active_channel(k_right[dim1])
            if if_active == 1:
                transmission_matrix[dim0, dim1] = np.sqrt(np.abs(velocity_right[dim0]/velocity_right[dim1])) * transmission_matrix[dim0, dim1]
                reflection_matrix[dim0, dim1] = np.sqrt(np.abs(velocity_left[dim0] / velocity_right[dim1]))*reflection_matrix[dim0, dim1]
            else:
                transmission_matrix[dim0, dim1] = 0
                reflection_matrix[dim0, dim1] = 0
    sum_of_tran_refl_array = np.sum(np.square(np.abs(transmission_matrix[0:ind_right_active, 0:ind_right_active])), axis=0)+np.sum(np.square(np.abs(reflection_matrix[0:ind_right_active, 0:ind_right_active])), axis=0)
    for sum_of_tran_refl in sum_of_tran_refl_array:
        if sum_of_tran_refl > 1.001:
            print('错误警告：散射矩阵的计算结果不归一！  Error Alert: scattering matrix is not normalized!')
    return transmission_matrix, reflection_matrix, k_right, k_left, velocity_right, velocity_left, ind_right_active


def write_transmission_matrix(fermi_energy, h00, h01, scatter_type=0, scatter_intensity=0.2, scatter_length=20):   # 输出
    transmission_matrix, reflection_matrix, k_right, k_left, velocity_right, velocity_left, ind_right_active, \
        = transmission_with_detailed_modes(fermi_energy, h00, h01, scatter_type, scatter_intensity, scatter_length)
    dim = h00.shape[0]
    np.set_printoptions(suppress=True)  # 取消科学计数法输出
    print('\n可传播的通道数（向右）active_channel (right) = ', ind_right_active)
    print('衰减的通道数（向右） evanescent_channel (right) = ', dim-ind_right_active, '\n')
    print('向右可传播的通道数对应的波矢 k_right:\n', np.real(k_right[0:ind_right_active]))
    print('向左可传播的通道数对应的波矢 k_left:\n', np.real(k_left[0:ind_right_active]), '\n')
    print('向右可传播的通道数对应的费米速度 velocity_right:\n', np.real(velocity_right[0:ind_right_active]))
    print('向左可传播的通道数对应的费米速度 velocity_left:\n', np.real(velocity_left[0:ind_right_active]), '\n')
    print('透射矩阵 transmission_matrix:\n', np.square(np.abs(transmission_matrix[0:ind_right_active, 0:ind_right_active])))
    print('反射矩阵 reflection_matrix:\n', np.square(np.abs(reflection_matrix[0:ind_right_active, 0:ind_right_active])), '\n')
    print('透射矩阵列求和 total transmission of channels =\n', np.sum(np.square(np.abs(transmission_matrix[0:ind_right_active, 0:ind_right_active])), axis=0))
    print('反射矩阵列求和 total reflection of channels =\n',np.sum(np.square(np.abs(reflection_matrix[0:ind_right_active, 0:ind_right_active])), axis=0))
    print('透射以及反射矩阵列求和 sum of transmission and reflection of channels =\n', np.sum(np.square(np.abs(transmission_matrix[0:ind_right_active, 0:ind_right_active])), axis=0) + np.sum(np.square(np.abs(reflection_matrix[0:ind_right_active, 0:ind_right_active])), axis=0))
    print('总电导 total conductance = ', np.sum(np.square(np.abs(transmission_matrix[0:ind_right_active, 0:ind_right_active]))), '\n')

    # 下面把以上信息写入文件中
    with open('a.txt', 'w') as f:
        f.write('Active_channel (right or left) = ' + str(ind_right_active) + '\n')
        f.write('Evanescent_channel (right or left) = ' + str(dim - ind_right_active) + '\n\n')
        f.write('Channel            K                           Velocity\n')
        for ind0 in range(ind_right_active):
            f.write('   '+str(ind0 + 1) + '   |    '+str(np.real(k_right[ind0]))+'            ' + str(np.real(velocity_right[ind0]))+'\n')
        f.write('\n')
        for ind0 in range(ind_right_active):
            f.write('  -' + str(ind0 + 1) + '   |    ' + str(np.real(k_left[ind0])) + '            ' + str(np.real(velocity_left[ind0])) + '\n')
        f.write('\n\nScattering_matrix:\n          ')
        for ind0 in range(ind_right_active):
            f.write(str(ind0+1)+'         ')
        f.write('\n')
        for ind1 in range(ind_right_active):
            f.write('  '+str(ind1+1)+'   ')
            for ind2 in range(ind_right_active):
                f.write('%f' % np.square(np.abs(transmission_matrix[ind1, ind2]))+'  ')
            f.write('\n')
        f.write('\n')
        for ind1 in range(ind_right_active):
            f.write(' -'+str(ind1+1)+'   ')
            for ind2 in range(ind_right_active):
                f.write('%f' % np.square(np.abs(reflection_matrix[ind1, ind2]))+'  ')
            f.write('\n')
        f.write('\n')
        f.write('Total transmission of channels:\n'+str(np.sum(np.square(np.abs(transmission_matrix[0:ind_right_active, 0:ind_right_active])), axis=0))+'\n')
        f.write('Total conductance = '+str(np.sum(np.square(np.abs(transmission_matrix[0:ind_right_active, 0:ind_right_active]))))+'\n')



if __name__ == '__main__':
    main()
