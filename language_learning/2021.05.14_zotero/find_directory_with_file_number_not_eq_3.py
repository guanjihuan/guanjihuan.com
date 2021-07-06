# 在E:\zotero\storage里的每个文件夹中一般有3个文件（包括隐藏文件），有个别无法解析或其他原因，会只有1个文件或者2个文件。这个其实没什么影响，但如果有强迫症可以通过以下python代码找出文件个数不等于3的文件夹。

import os

def find_files_and_directory(path):
    file = []
    directory = []
    for path in path:
        filenames = os.listdir(path)
        for filename in filenames:
            filename = os.path.join(path,filename) 
            if os.path.isfile(filename): # 如果是文件
                file.append(filename) 
            else:  # 如果是文件夹
                directory.append(filename)
    return file, directory

file, directory = find_files_and_directory(['E:/zotero/storage'])

i0 = 0
for path in directory:
    file, directory = find_files_and_directory([path])
    if len(file)!=3:
        i0 += 1
        print(path, '文件夹中有', len(file), '个文件')
print('文件夹中文件个数不等于3的总个数:', i0)