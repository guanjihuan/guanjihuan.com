import numpy as np

# 设置
cpus = 7  # 使用的CPU个数（等于提交任务的个数）
parameter_array_all = np.arange(0, 10, 0.1) # 需要计算的参数


# 通过.sh脚本文件修改的任务指标。job_index从0开始，最大值为cpus-1
job_index = -1


# 预处理
len_of_parameter_all = len(parameter_array_all)  # 需要计算参数的个数
if len_of_parameter_all%cpus == 0:
	len_parameter = int(len_of_parameter_all/cpus) # 一个CPU/任务需要计算参数的个数
	parameter_array = parameter_array_all[job_index*len_parameter:(job_index+1)*len_parameter]
else:
	len_parameter = int(len_of_parameter_all/(cpus-1)) # 一个CPU/任务需要计算参数的个数
	if job_index != cpus-1:
		parameter_array = parameter_array_all[job_index*len_parameter:(job_index+1)*len_parameter]
	else:
		parameter_array = parameter_array_all[job_index*len_parameter:len_of_parameter_all]


# 任务
with open('a'+str(job_index)+'.txt', 'w') as f:
	for parameter in parameter_array:
		result = parameter**2
		f.write(str(parameter)+'            '+str(result)+'\n')