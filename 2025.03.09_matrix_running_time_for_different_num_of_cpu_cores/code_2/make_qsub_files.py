import guan  # https://py.guanjihuan.com | install: pip install --upgrade guan
import numpy as np
import os

cpu_num_array = np.arange(1, 33)

py_filename='matrix_running_time_for_different_num_of_cpu_cores_writing_into_files'
current_directory = os.getcwd()

for cpu_num in cpu_num_array:
    guan.make_directory(f'./task_{cpu_num}')
    os.system(f'cp ./{py_filename}.py ./task_{cpu_num}/{py_filename}.py')
    os.system(f'cd {current_directory}/task_{cpu_num}')
    guan.make_sh_file_for_qsub(sh_filename=f'./task_{cpu_num}/task_{cpu_num}', command_line=f'python {py_filename}.py', cpu_num=cpu_num, task_name=f'test_{cpu_num}', cd_dir=0)