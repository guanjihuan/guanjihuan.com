import os
code_path = os.getcwd() # 当前代码文件的路径
data_path = code_path.replace('\\', '/')  # \改为/，防止路径报错
data_path = code_path.replace('codes', 'data') # 把路径中codes改为data
if os.path.exists(data_path) == False: # 如果文件夹不存在，新建文件夹
    os.makedirs(data_path)
os.chdir(data_path) # 转到数据的存放路径
with open('data.txt', 'w') as f: # 保存数据
    f.write('Hello world') 