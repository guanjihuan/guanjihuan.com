# 数组分割
import numpy as np
import guan
task_num = 4
parameter_array_all = np.arange(0, 17, 1) 
for task_index in range(task_num):
    parameter_array = guan.preprocess_for_parallel_calculations(parameter_array_all, task_num, task_index)
    print(parameter_array)
    print()