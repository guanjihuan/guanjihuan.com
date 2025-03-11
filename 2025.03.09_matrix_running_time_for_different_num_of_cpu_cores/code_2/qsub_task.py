import numpy as np
import os

cpu_num_array = np.arange(1, 33)

current_directory = os.getcwd()

for cpu_num in cpu_num_array:
    os.system(f'cd {current_directory}/task_{cpu_num} && qsub {current_directory}/task_{cpu_num}/task_{cpu_num}.sh')