"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/29200
"""

import os

parameter_str_array = ['np.arange(1, 11, 1)', 'np.arange(11, 21, 1)']

index = 0
for parameter_str in parameter_str_array:
    index += 1

    # 以下处理代码文件
    old_file = 'a.py'
    new_file = 'a'+str(index)+'.py'

    # 说明：linux系统下复制用cp，windows系统下复制用copy
    os.system('cp '+old_file+' '+new_file)  # 复制python代码文件
    with open(new_file, 'r') as f:  # 读取
        content  = f.read()
    
    old_str = 'parameter_array_labeled_for_replacement = []'
    new_str = 'parameter_array_labeled_for_replacement = ' + parameter_str
    content = content.replace(old_str, new_str)

    # 如果程序需要将数据写入文件，除了需要替代参数，还需要替代文件名，方法和以上相同

    with open('a'+str(index)+'.py', 'w') as f: # 写入
        f.write(content)



    # 以下处理任务上传文件
    old_file = 'a.sh'
    new_file = 'a'+str(index)+'.sh'

    os.system('cp '+old_file+' '+new_file)  # 复制任务调度系统的sh上传文件
    with open(new_file, 'r') as f:  # 读取
        content  = f.read()
    
    old_str = 'python a.py'
    new_str = 'python a'+str(index)+'.py'
    content = content.replace(old_str, new_str)

    old_str = 'task'
    new_str = 'task_'+str(index)
    content = content.replace(old_str, new_str)

    with open('a'+str(index)+'.sh', 'w') as f: # 写入
        f.write(content)



    # 提交任务
    os.system('qsub '+new_file)