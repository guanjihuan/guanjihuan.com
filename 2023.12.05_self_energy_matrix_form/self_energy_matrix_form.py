"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37881
"""

import guan
import numpy as np

Nx = 10
Ny = 3
fermi_energy = 0

h00 = guan.hamiltonian_of_finite_size_system_along_one_direction(N=Ny)
h01 = np.eye(Ny)

# 电极和中心区之间的跃迁
h_LC = np.zeros((Ny, Nx*Ny))
h_CR = np.zeros((Nx*Ny, Ny))
for iy in range(Ny):
    h_LC[iy, 0+iy] = 1
    h_CR[(Nx-1)*Ny+iy, iy] = 1

# 和中心区哈密顿量耦合后的电极自能
right_self_energy, left_self_energy, gamma_right, gamma_left = guan.self_energy_of_lead_with_h_LC_and_h_CR(fermi_energy, h00, h01, h_LC, h_CR)

print(right_self_energy.shape)
print(left_self_energy.shape)
print()

# 找到矩阵元素非零的坐标
num = len(right_self_energy)
for i1 in range(num):
    for i2 in range(num):
        if abs(right_self_energy[i1, i2])>1e-8:
            print((i1, i2))
print()

num = len(left_self_energy)
for i1 in range(num):
    for i2 in range(num):
        if abs(left_self_energy[i1, i2])>1e-8:
            print((i1, i2))