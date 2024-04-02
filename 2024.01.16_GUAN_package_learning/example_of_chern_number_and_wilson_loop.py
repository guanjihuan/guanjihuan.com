# 陈数和Wilson loop计算示例
import guan
import numpy as np
chern_number = guan.calculate_chern_number_for_square_lattice_with_efficient_method(guan.hamiltonian_of_one_QAH_model, precision=100)
print('\nChern number=', chern_number, '\n')
wilson_loop_array = guan.calculate_wilson_loop(guan.hamiltonian_of_ssh_model)
print('Wilson loop =', wilson_loop_array)
p = np.log(wilson_loop_array)/2/np.pi/1j
print('\np =', p, '\n')