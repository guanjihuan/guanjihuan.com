"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/25685
"""

# 注意：这个程序请小心使用，防止误操作把系统文件或个人文件破坏。在选取好directory目录后，请经过再三确认无误后再运行，尤其是directory的层级不能太高。


def main():
    # 选取某个目录
    directory = 'E:/test/all_files'
    move_all_files_to_root_directory(directory)
    
    # import guan
    # guan.move_all_files_to_root_directory(directory)


def move_all_files_to_root_directory(directory):
    import os
    import shutil
    for root, dirs, files in os.walk(directory):
        for i0 in range(len(files)):
            # print(root) # 文件对应目录
            # print(files[i0], '\n') # 文件
            shutil.move(root+'/'+files[i0], directory+'/'+files[i0]) # 移动所有文件至根目录
    for i0 in range(100): # 多次尝试删除层数比较多的空文件夹，例如100层
        for root, dirs, files in os.walk(directory):
            try:
                os.rmdir(root) # 删除空文件夹
            except:
                pass


if __name__ == '__main__':
    main()