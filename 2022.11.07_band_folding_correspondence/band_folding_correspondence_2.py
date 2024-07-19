"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/27605
"""

import guan
import numpy as np


# double chains model with different potentials
unit_cell = np.array([[0, 0], [0, 0.5]])
hopping = np.eye(2)
hamiltonian_function_1 = guan.one_dimensional_fourier_transform_with_k(unit_cell, hopping)
k_array_1 = np.linspace(-np.pi, np.pi, 600)
eigenvalue_array_1 = guan.calculate_eigenvalue_with_one_parameter(k_array_1, hamiltonian_function_1)
# guan.plot(k_array_1, eigenvalue_array_1, xlabel='k', ylabel='E', style='k', title='double chains model with different potentials')

# n times band folding
n = 2
unit_cell = np.zeros((2*n, 2*n))
for i0 in range(int(n)):
    for j0 in range(int(n)):
        if abs(i0-j0)==1:
            unit_cell[i0, j0] = 1
for i0 in range(int(n)):
    unit_cell[n+i0, n+i0] = 0.5
    for j0 in range(int(n)):
        if abs(i0-j0)==1:
            unit_cell[n+i0, n+j0] = 1
hopping = np.zeros((2*n, 2*n))
hopping[0, n-1] = 1
hopping[n, 2*n-1] = 1
hamiltonian_function_2 = guan.one_dimensional_fourier_transform_with_k(unit_cell, hopping)
k_array_2 = np.linspace(-np.pi, np.pi, 620)
eigenvalue_array_2 = guan.calculate_eigenvalue_with_one_parameter(k_array_2, hamiltonian_function_2)
# guan.plot(k_array_2, eigenvalue_array_2, xlabel='k', ylabel='E', style='k', title='%i times band folding'%n)



### 以下通过速度和能量查找能带折叠前后的对应关系


# 获取速度
velocity_array_1 = []
for i0 in range(k_array_1.shape[0]-1):
    velocity_1 = (eigenvalue_array_1[i0+1]-eigenvalue_array_1[i0])/(k_array_1[i0+1]-k_array_1[i0])
    velocity_array_1.append(velocity_1)

# 获取速度
velocity_array_2 = []
for i0 in range(k_array_2.shape[0]-1):
    velocity_2 = (eigenvalue_array_2[i0+1]-eigenvalue_array_2[i0])/(k_array_2[i0+1]-k_array_2[i0])
    velocity_array_2.append(velocity_2*n)

dim = 2  # 维度为两倍

plt_1, fig_1, ax_1 = guan.import_plt_and_start_fig_ax()
plt_2, fig_2, ax_2 = guan.import_plt_and_start_fig_ax()
for j00 in range(dim):
    for i00 in range(n*dim):
        k_array_new_2 = []
        k_array_new_1 = []
        index_array_new_2 = []
        index_array_new_1 = []
        for i0 in range(k_array_2.shape[0]-1):
            for j0 in range(k_array_1.shape[0]-1):
                if  abs(eigenvalue_array_2[i0][i00]-eigenvalue_array_1[j0][j00])<1e-2 and abs(velocity_array_2[i0][i00]-velocity_array_1[j0][j00])<1e-2:
                    k_array_new_2.append(k_array_2[i0])
                    k_array_new_1.append(k_array_1[j0])
                    index_array_new_2.append(i0)
                    index_array_new_1.append(j0)
        if i00 == 0 and j00 == 0:
            guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, k_array_new_1, eigenvalue_array_1[index_array_new_1, j00], style='*r')
            guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, k_array_new_2, eigenvalue_array_2[index_array_new_2, i00], style='*r')
        elif i00 == 0 and j00 == 1:
            guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, k_array_new_1, eigenvalue_array_1[index_array_new_1, j00], style='*b')
            guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, k_array_new_2, eigenvalue_array_2[index_array_new_2, i00], style='*b')
        elif i00 == 1 and j00 == 0:
            guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, k_array_new_1, eigenvalue_array_1[index_array_new_1, j00], style='*g')
            guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, k_array_new_2, eigenvalue_array_2[index_array_new_2, i00], style='*g')
        elif i00 == 1 and j00 == 1:
            guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, k_array_new_1, eigenvalue_array_1[index_array_new_1, j00], style='*c')
            guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, k_array_new_2, eigenvalue_array_2[index_array_new_2, i00], style='*c')
        elif i00 == 2 and j00 == 0:
            guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, k_array_new_1, eigenvalue_array_1[index_array_new_1, j00], style='*m')
            guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, k_array_new_2, eigenvalue_array_2[index_array_new_2, i00], style='*m')
        elif i00 == 2 and j00 == 1:
            guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, k_array_new_1, eigenvalue_array_1[index_array_new_1, j00], style='*y')
            guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, k_array_new_2, eigenvalue_array_2[index_array_new_2, i00], style='*y')
        else:
            guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, k_array_new_1, eigenvalue_array_1[index_array_new_1, j00], style='*k')
            guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, k_array_new_2, eigenvalue_array_2[index_array_new_2, i00], style='*k')
guan.plot_without_starting_fig_ax(plt_1, fig_1, ax_1, [], [], xlabel='k', ylabel='E', title='double chains model with different potentials')
guan.plot_without_starting_fig_ax(plt_2, fig_2, ax_2, [], [], xlabel='k', ylabel='E', title='%i times band folding'%n)
plt_1.show()
plt_2.show()