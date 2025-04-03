import numpy as np
import os

cpu_num_array = np.arange(1, 9)

for cpu_num in cpu_num_array:
    os.system(f'qsub task_{cpu_num}.sh')