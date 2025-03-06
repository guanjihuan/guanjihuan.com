# 电导和散射矩阵的计算
import guan
import numpy as np

fermi_energy_array = np.linspace(-4, 4, 400)
h00 = guan.hamiltonian_of_finite_size_system_along_one_direction(4)
h01 = np.identity(4)
conductance_array = guan.calculate_conductance_with_fermi_energy_array(fermi_energy_array, h00, h01)
guan.plot(fermi_energy_array, conductance_array, xlabel='E', ylabel='Conductance', style='-', fontfamily=None)

fermi_energy = 0
guan.print_or_write_scattering_matrix(fermi_energy, h00, h01)