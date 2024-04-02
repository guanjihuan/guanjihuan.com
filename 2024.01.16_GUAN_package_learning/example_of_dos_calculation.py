# 使用格林函数计算态密度示例
import guan
import numpy as np

hamiltonian = guan.hamiltonian_of_finite_size_system_along_two_directions_for_square_lattice(2,2)
fermi_energy_array = np.linspace(-4, 4, 400)
total_dos_array = guan.total_density_of_states_with_fermi_energy_array(fermi_energy_array, hamiltonian, broadening=0.1)
guan.plot(fermi_energy_array, total_dos_array, xlabel='E', ylabel='Total DOS', style='-', fontfamily=None)

fermi_energy = 0
N1 = 3
N2 = 4
hamiltonian = guan.hamiltonian_of_finite_size_system_along_two_directions_for_square_lattice(N1,N2)
LDOS = guan.local_density_of_states_for_square_lattice(fermi_energy, hamiltonian, N1=N1, N2=N2)
print('square lattice:\n', LDOS, '\n')
h00 = guan.hamiltonian_of_finite_size_system_along_one_direction(N2)
h01 = np.identity(N2)
LDOS = guan.local_density_of_states_for_square_lattice_using_dyson_equation(fermi_energy, h00=h00, h01=h01, N2=N2, N1=N1)
print(LDOS, '\n\n')
LDOS2 = guan.local_density_of_states_for_square_lattice_using_dyson_equation_with_second_method(fermi_energy, h00, h01, N2, N1, internal_degree=1, broadening=0.01)
print(LDOS2, '\n\n')
guan.plot_contour(range(N1), range(N2), LDOS, fontfamily=None)
guan.plot_contour(range(N1), range(N2), LDOS2, fontfamily=None)

N1 = 3
N2 = 4
N3 = 5
hamiltonian = guan.hamiltonian_of_finite_size_system_along_three_directions_for_cubic_lattice(N1, N2, N3)
LDOS = guan.local_density_of_states_for_cubic_lattice(fermi_energy, hamiltonian, N1=N1, N2=N2, N3=N3)
print('cubic lattice:\n', LDOS, '\n')
h00 = guan.hamiltonian_of_finite_size_system_along_two_directions_for_square_lattice(N2, N3)
h01 = np.identity(N2*N3)
LDOS = guan.local_density_of_states_for_cubic_lattice_using_dyson_equation(fermi_energy, h00, h01, N3=N3, N2=N2, N1=N1)
print(LDOS)