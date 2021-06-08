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