"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/6075
"""

import numpy as np
import time
import guan

def get_lead_h00(width):  
    h00 = np.zeros((width, width))
    for i0 in range(width-1):
        h00[i0, i0+1] = 1
        h00[i0+1, i0] = 1
    return h00


def get_lead_h01(width):
    h01 = np.identity(width)
    return h01


def get_center_hamiltonian(Nx, Ny):
    h = np.zeros((Nx*Ny, Nx*Ny))
    for x0 in range(Nx-1):
        for y0 in range(Ny):
            h[x0*Ny+y0, (x0+1)*Ny+y0] = 1 # x方向的跃迁
            h[(x0+1)*Ny+y0, x0*Ny+y0] = 1
    for x0 in range(Nx):
        for y0 in range(Ny-1):
            h[x0*Ny+y0, x0*Ny+y0+1] = 1 # y方向的跃迁
            h[x0*Ny+y0+1, x0*Ny+y0] = 1 
    return h


def main():
    start_time = time.time()
    width = 5
    length = 50 
    fermi_energy_array = np.arange(-4, 4, .01)
    # 中心区的哈密顿量
    center_hamiltonian = get_center_hamiltonian(Nx=length, Ny=width)
    # 电极的h00和h01
    lead_h00 = get_lead_h00(width)
    lead_h01 = get_lead_h01(width)
    transmission_12_array = []
    transmission_13_array = []
    transmission_14_array = []
    transmission_15_array = []
    transmission_16_array = []
    transmission_1_all_array = []
    for fermi_energy in fermi_energy_array:
        print(fermi_energy)
        #   几何形状如下所示：
        #               lead2         lead3
        #   lead1(L)                          lead4(R)  
        #               lead6         lead5 

        transmission_12, transmission_13, transmission_14, transmission_15, transmission_16 = guan.calculate_six_terminal_transmissions_from_lead_1(fermi_energy, h00_for_lead_4=lead_h00, h01_for_lead_4=lead_h01, h00_for_lead_2=lead_h00, h01_for_lead_2=lead_h01, center_hamiltonian=center_hamiltonian, width=width, length=length, internal_degree=1, moving_step_of_leads=0)
        transmission_12_array.append(transmission_12)
        transmission_13_array.append(transmission_13)
        transmission_14_array.append(transmission_14)
        transmission_15_array.append(transmission_15)
        transmission_16_array.append(transmission_16)
        transmission_1_all_array.append(\
            transmission_12+transmission_13+transmission_14+transmission_15+transmission_16)

        # transmission_matrix = guan.calculate_six_terminal_transmission_matrix(fermi_energy, h00_for_lead_4=lead_h00, h01_for_lead_4=lead_h01, h00_for_lead_2=lead_h00, h01_for_lead_2=lead_h01, center_hamiltonian=center_hamiltonian, width=width, length=length, internal_degree=1, moving_step_of_leads=0)
        # transmission_12_array.append(transmission_matrix[0, 1])
        # transmission_13_array.append(transmission_matrix[0, 2])
        # transmission_14_array.append(transmission_matrix[0, 3])
        # transmission_15_array.append(transmission_matrix[0, 4])
        # transmission_16_array.append(transmission_matrix[0, 5])
        # transmission_1_all_array.append(transmission_matrix[0, 1]+transmission_matrix[0, 2]+transmission_matrix[0, 3]+transmission_matrix[0, 4]+transmission_matrix[0, 5])

    guan.plot(fermi_energy_array, transmission_12_array, xlabel='Fermi energy', ylabel='Transmission_12')
    guan.plot(fermi_energy_array, transmission_13_array, xlabel='Fermi energy', ylabel='Transmission_13')
    guan.plot(fermi_energy_array, transmission_14_array, xlabel='Fermi energy', ylabel='Transmission_14')
    guan.plot(fermi_energy_array, transmission_15_array, xlabel='Fermi energy', ylabel='Transmission_15')
    guan.plot(fermi_energy_array, transmission_16_array, xlabel='Fermi energy', ylabel='Transmission_16')
    guan.plot(fermi_energy_array, transmission_1_all_array, xlabel='Fermi energy', ylabel='Transmission_1_all')
    end_time = time.time()
    print('运行时间（分）=', (end_time-start_time)/60)


if __name__ == '__main__':
    main()