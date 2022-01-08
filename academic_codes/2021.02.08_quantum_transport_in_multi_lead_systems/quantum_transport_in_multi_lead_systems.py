"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6075
"""

import numpy as np
import matplotlib.pyplot as plt
import copy
import time


def lead_matrix_00(y):  
    h00 = np.zeros((y, y))
    for y0 in range(y-1):
        h00[y0, y0+1] = 1
        h00[y0+1, y0] = 1
    return h00


def lead_matrix_01(y):
    h01 = np.identity(y)
    return h01


def scattering_region(x, y):
    h = np.zeros((x*y, x*y))
    for x0 in range(x-1):
        for y0 in range(y):
            h[x0*y+y0, (x0+1)*y+y0] = 1 # x方向的跃迁
            h[(x0+1)*y+y0, x0*y+y0] = 1
    for x0 in range(x):
        for y0 in range(y-1):
            h[x0*y+y0, x0*y+y0+1] = 1 # y方向的跃迁
            h[x0*y+y0+1, x0*y+y0] = 1 
    return h


def main():
    start_time = time.time()
    width = 5
    length = 50 
    fermi_energy_array = np.arange(-4, 4, .01)

    # 中心区的哈密顿量
    H_scattering_region = scattering_region(x=length, y=width)

    # 电极的h00和h01
    lead_h00 = lead_matrix_00(width)
    lead_h01 = lead_matrix_01(width)
    
    transmission_12_array = []
    transmission_13_array = []
    transmission_14_array = []
    transmission_15_array = []
    transmission_16_array = []
    transmission_1_all_array = []

    for fermi_energy in fermi_energy_array:
        print(fermi_energy)
        # 表面格林函数
        right_lead_surface, left_lead_surface = surface_green_function_lead(fermi_energy + 1e-9j, lead_h00, lead_h01, dim=width)

        # 由于镜面对称以及xy各项同性，因此这里六个电极的表面格林函数具有相同的形式
        lead_1 = copy.deepcopy(right_lead_surface)  # 镜面对称使得lead_1=lead_4
        lead_2 = copy.deepcopy(right_lead_surface)  # xy各项同性使得lead_2=lead_4
        lead_3 = copy.deepcopy(right_lead_surface)
        lead_4 = copy.deepcopy(right_lead_surface)  
        lead_5 = copy.deepcopy(right_lead_surface)
        lead_6 = copy.deepcopy(right_lead_surface)

        #   几何形状如下所示：
        #               lead2         lead3
        #   lead1(L)                          lead4(R)  
        #               lead6         lead5 

        # 电极到中心区的跃迁矩阵
        H_from_lead_1_to_center = np.zeros((width, width*length), dtype=complex)
        H_from_lead_2_to_center = np.zeros((width, width*length), dtype=complex)
        H_from_lead_3_to_center = np.zeros((width, width*length), dtype=complex)
        H_from_lead_4_to_center = np.zeros((width, width*length), dtype=complex)
        H_from_lead_5_to_center = np.zeros((width, width*length), dtype=complex)
        H_from_lead_6_to_center = np.zeros((width, width*length), dtype=complex)
        move = 0 # the step of leads 2,3,6,5 moving to center
        for i0 in range(width):
            H_from_lead_1_to_center[i0, i0] = 1
            H_from_lead_2_to_center[i0, width*(move+i0)+(width-1)] = 1
            H_from_lead_3_to_center[i0, width*(length-move-1-i0)+(width-1)] = 1
            H_from_lead_4_to_center[i0, width*(length-1)+i0] = 1
            H_from_lead_5_to_center[i0, width*(length-move-1-i0)+0] = 1
            H_from_lead_6_to_center[i0, width*(move+i0)+0] = 1

        # 自能    
        self_energy_1 = np.dot(np.dot(H_from_lead_1_to_center.transpose().conj(), lead_1), H_from_lead_1_to_center)
        self_energy_2 = np.dot(np.dot(H_from_lead_2_to_center.transpose().conj(), lead_2), H_from_lead_2_to_center)
        self_energy_3 = np.dot(np.dot(H_from_lead_3_to_center.transpose().conj(), lead_3), H_from_lead_3_to_center)
        self_energy_4 = np.dot(np.dot(H_from_lead_4_to_center.transpose().conj(), lead_4), H_from_lead_4_to_center)
        self_energy_5 = np.dot(np.dot(H_from_lead_5_to_center.transpose().conj(), lead_5), H_from_lead_5_to_center)
        self_energy_6 = np.dot(np.dot(H_from_lead_6_to_center.transpose().conj(), lead_6), H_from_lead_6_to_center)

        # 整体格林函数
        green = np.linalg.inv(fermi_energy*np.eye(width*length)-H_scattering_region-self_energy_1-self_energy_2-self_energy_3-self_energy_4-self_energy_5-self_energy_6)

        # Gamma矩阵
        gamma_1 = 1j*(self_energy_1-self_energy_1.transpose().conj())
        gamma_2 = 1j*(self_energy_2-self_energy_2.transpose().conj())
        gamma_3 = 1j*(self_energy_3-self_energy_3.transpose().conj())
        gamma_4 = 1j*(self_energy_4-self_energy_4.transpose().conj())
        gamma_5 = 1j*(self_energy_5-self_energy_5.transpose().conj())
        gamma_6 = 1j*(self_energy_6-self_energy_6.transpose().conj())

        # Transmission
        transmission_12 = np.trace(np.dot(np.dot(np.dot(gamma_1, green), gamma_2), green.transpose().conj()))
        transmission_13 = np.trace(np.dot(np.dot(np.dot(gamma_1, green), gamma_3), green.transpose().conj()))
        transmission_14 = np.trace(np.dot(np.dot(np.dot(gamma_1, green), gamma_4), green.transpose().conj()))
        transmission_15 = np.trace(np.dot(np.dot(np.dot(gamma_1, green), gamma_5), green.transpose().conj()))
        transmission_16 = np.trace(np.dot(np.dot(np.dot(gamma_1, green), gamma_6), green.transpose().conj()))

        transmission_12_array.append(np.real(transmission_12))
        transmission_13_array.append(np.real(transmission_13))
        transmission_14_array.append(np.real(transmission_14))
        transmission_15_array.append(np.real(transmission_15))
        transmission_16_array.append(np.real(transmission_16))
        transmission_1_all_array.append(np.real(transmission_12+transmission_13+transmission_14+transmission_15+transmission_16))
    
    Plot_Line(fermi_energy_array, transmission_12_array, xlabel='Fermi energy', ylabel='Transmission_12', title='', filename='a')
    Plot_Line(fermi_energy_array, transmission_13_array, xlabel='Fermi energy', ylabel='Transmission_13', title='', filename='a')
    Plot_Line(fermi_energy_array, transmission_14_array, xlabel='Fermi energy', ylabel='Transmission_14', title='', filename='a')
    Plot_Line(fermi_energy_array, transmission_15_array, xlabel='Fermi energy', ylabel='Transmission_15', title='', filename='a')
    Plot_Line(fermi_energy_array, transmission_16_array, xlabel='Fermi energy', ylabel='Transmission_16', title='', filename='a')
    Plot_Line(fermi_energy_array, transmission_1_all_array, xlabel='Fermi energy', ylabel='Transmission_1_all', title='', filename='a')
    end_time = time.time()
    print('运行时间=', end_time-start_time)



def Plot_Line(x, y, xlabel='x', ylabel='y', title='', filename='a'): 
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.20, left=0.18) 
    ax.plot(x, y, '-')
    ax.grid()
    ax.set_title(title, fontsize=20, fontfamily='Times New Roman')
    ax.set_xlabel(xlabel, fontsize=20, fontfamily='Times New Roman') 
    ax.set_ylabel(ylabel, fontsize=20, fontfamily='Times New Roman') 
    ax.tick_params(labelsize=20) 
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]  
    # plt.savefig(filename+'.jpg', dpi=300) 
    plt.show()
    plt.close('all')

def transfer_matrix(fermi_energy, h00, h01, dim):   # 转移矩阵T
    transfer = np.zeros((2*dim, 2*dim))*(0+0j)  
    transfer[0:dim, 0:dim] = np.dot(np.linalg.inv(h01), fermi_energy*np.identity(dim)-h00)  
    transfer[0:dim, dim:2*dim] = np.dot(-1*np.linalg.inv(h01), h01.transpose().conj())
    transfer[dim:2*dim, 0:dim] = np.identity(dim)
    transfer[dim:2*dim, dim:2*dim] = 0 
    return transfer  # 返回转移矩阵


def surface_green_function_lead(fermi_energy, h00, h01, dim):  # 电极的表面格林函数
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


if __name__ == '__main__':
    main()