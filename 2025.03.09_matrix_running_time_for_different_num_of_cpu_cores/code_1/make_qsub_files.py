import guan  # https://py.guanjihuan.com | install: pip install --upgrade guan
import numpy as np

cpu_num_array = np.arange(1, 17)

sh_filename = 'task'
task_name = 'test'
py_filename='matrix_running_time_for_different_num_of_cpu_cores'

for cpu_num in cpu_num_array:
    guan.make_sh_file_for_qsub(sh_filename=sh_filename+'_'+str(cpu_num), command_line=f'python {py_filename}.py', cpu_num=cpu_num, task_name=task_name+'_'+str(cpu_num), cd_dir=0)