import guan
import numpy as np

fermi_energy_array = np.linspace(-4, 4, 400)
h00 = guan.finite_size_along_one_direction(5)
h01 = np.identity(5)
conductance_array = guan.calculate_conductance_with_fermi_energy_array(fermi_energy_array, h00, h01)
guan.plot(fermi_energy_array, conductance_array, xlabel='E', ylabel='Conductance', type='-')