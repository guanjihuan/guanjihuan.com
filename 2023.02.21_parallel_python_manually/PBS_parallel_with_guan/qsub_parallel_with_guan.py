import guan

parameter_array = [1, 2, 3, 4]

guan.make_sh_file_for_qsub(sh_filename='a', command_line='python a.py', cpu_num=1, task_name='task', cd_dir=0)

guan.copy_py_sh_file_and_qsub_task(parameter_array=parameter_array, py_filename='a', old_str_in_py='parameter=0', new_str_in_py='parameter=', sh_filename='a', qsub_task_name='task')