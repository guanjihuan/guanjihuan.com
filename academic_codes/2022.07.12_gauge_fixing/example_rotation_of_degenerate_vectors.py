"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/22604
"""

import numpy as np
import math
import cmath
# from numba import jit

# @jit
def rotation_of_degenerate_vectors(vector1, vector2, index1=None, index2=None, precision=0.01, criterion=0.01, show_theta=0):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    if index1 == None:
        index1 = np.argmax(np.abs(vector1))
    if index2 == None:
        index2 = np.argmax(np.abs(vector2))
    if np.abs(vector1[index2])>criterion or np.abs(vector2[index1])>criterion:
        for theta in np.arange(0, 2*math.pi, precision):
            if show_theta==1:
                print(theta)
            for phi1 in np.arange(0, 2*math.pi, precision):
                for phi2 in np.arange(0, 2*math.pi, precision):
                    vector1_test = cmath.exp(1j*phi1)*vector1*math.cos(theta)+cmath.exp(1j*phi2)*vector2*math.sin(theta)
                    vector2_test = -cmath.exp(-1j*phi2)*vector1*math.sin(theta)+cmath.exp(-1j*phi1)*vector2*math.cos(theta)
                    if np.abs(vector1_test[index2])<criterion and np.abs(vector2_test[index1])<criterion:
                        vector1 = vector1_test
                        vector2 = vector2_test
                        break
                if np.abs(vector1_test[index2])<criterion and np.abs(vector2_test[index1])<criterion:
                    break
            if np.abs(vector1_test[index2])<criterion and np.abs(vector2_test[index1])<criterion:
                break
    return vector1, vector2

def hamiltonian_of_BBH_model(kx, ky, gamma_x=0.5, gamma_y=0.5, lambda_x=1, lambda_y=1):
    # label of atoms in a unit cell
    # (2) —— (0)
    #  |      |
    # (1) —— (3)   
    hamiltonian = np.zeros((4, 4), dtype=complex)
    hamiltonian[0, 2] = gamma_x+lambda_x*cmath.exp(1j*kx)
    hamiltonian[1, 3] = gamma_x+lambda_x*cmath.exp(-1j*kx)
    hamiltonian[0, 3] = gamma_y+lambda_y*cmath.exp(1j*ky)
    hamiltonian[1, 2] = -gamma_y-lambda_y*cmath.exp(-1j*ky)
    hamiltonian[2, 0] = np.conj(hamiltonian[0, 2])
    hamiltonian[3, 1] = np.conj(hamiltonian[1, 3])
    hamiltonian[3, 0] = np.conj(hamiltonian[0, 3])
    hamiltonian[2, 1] = np.conj(hamiltonian[1, 2]) 
    return hamiltonian

# For kx=0
print('\nFor kx=0:\n')
eigenvalue, eigenvector = np.linalg.eigh(hamiltonian_of_BBH_model(kx=0, ky=0))
print(eigenvalue, '\n')
print(eigenvector[:, 0])
print(eigenvector[:, 1], '\n')

# For kx=0.005
print('\nFor kx=0.005:\n')
eigenvalue, eigenvector = np.linalg.eigh(hamiltonian_of_BBH_model(kx=0.005, ky=0))
print(eigenvalue, '\n')
print(eigenvector[:, 0])
print(eigenvector[:, 1], '\n\n')

# Rotaion
vector1, vector2 = rotation_of_degenerate_vectors(eigenvector[:, 0], eigenvector[:, 1], precision=0.01, criterion=0.01, show_theta=1)
print()
print(vector1)
print(vector2, '\n')


# # 可直接使用Guan软件包来调用以上函数：https://py.guanjihuan.com。
# # 安装命令：pip install --upgrade guan。
# import guan
# vector1, vector2 = guan.rotation_of_degenerate_vectors(vector1, vector2, index1=None, index2=None, precision=0.01, criterion=0.01, show_theta=0)
# hamiltonian = guan.hamiltonian_of_BBH_model(kx, ky, gamma_x=0.5, gamma_y=0.5, lambda_x=1, lambda_y=1)