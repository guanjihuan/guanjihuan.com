import guan

parameter_array = [1, 2, 3, 4]

sh_filename = 'a'
task_name = 'task'
py_filename = 'a'

guan.make_sh_file_for_bsub(sh_filename=sh_filename, command_line=f'python {py_filename}.py', cpu_num=1, task_name=task_name, queue_name='score', cd_dir=0)

guan.copy_py_sh_file_and_bsub_task(parameter_array, py_filename=py_filename, old_str_in_py='parameter = 0', new_str_in_py='parameter = ', sh_filename=sh_filename, task_name=task_name)