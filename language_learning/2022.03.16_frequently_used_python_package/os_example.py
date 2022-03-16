import os
os.getcwd()  # 获取路径
if os.path.exists('new_dir') == False: # 判断路径是否存在
    os.makedirs('new_dir') # 新建文件夹
os.chdir('new_dir')  # 切换到该文件夹
print(os.walk('/'))  # 游走目录