"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/25453
"""

import os

# 选取某个目录
directory = 'E:/'

def main():
    for root, dirs, files in os.walk(directory):
        for i0 in range(len(files)):
            if 'pdf' in files[i0] or 'djvu' in files[i0]: # 满足某个条件的文件 

                # 显示旧文件名
                name = files[i0]
                print(name) # 显示旧文件名

                # 显示新文件名
                new_name = modify_name(name)
                print(new_name)
                print()

                # # 修改文件名。注意：需要检查前面的代码，尤其是modify_name的规则看是否都满足，再运行下面的代码，否则文件名的修改会出现遗漏或混乱。
                # if new_name != None:
                #     os.rename(root+'/'+name, root+'/'+new_name) 
        

def modify_name(name):  # 按某种规则修改文件名
    array = name.split(' - ')  # 通过' - '把这类型的文件名切开
    if len(array) != 3:
        print('Miss:', name)
        new_name = None  # 如果不满足规则，则不修改
    else:
        new_name= array[1]+' - '+array[0]+' - '+array[2] # 做个对调
    return new_name


if __name__ == '__main__':
    main()