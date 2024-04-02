# 数组分割示例
import numpy as np
import guan
cpus = 4
parameter_array_all = np.arange(0, 17, 1) 
for task_index in range(cpus):
    parameter_array = guan.preprocess_for_parallel_calculations(parameter_array_all, cpus, task_index)
    print(parameter_array)
    print()