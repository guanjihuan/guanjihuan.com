"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/26536
"""


def main():
    # 如果子文件夹中所有文件的数量小于5，输出路径。
    count_file_in_sub_directory(directory='./', smaller_than_num=5) 

    # import guan
    # guan.count_file_in_sub_directory(directory='./', smaller_than_num=5)


def count_file_in_sub_directory(directory='./', smaller_than_num=None):
    import os
    from collections import Counter
    dirs_list = []
    for root, dirs, files in os.walk(directory):
        if dirs != []:
            for i0 in range(len(dirs)):
                dirs_list.append(root+'/'+dirs[i0])
    for sub_dir in dirs_list:
        file_list = []
        for root, dirs, files in os.walk(sub_dir):
            for i0 in range(len(files)):
                file_list.append(files[i0])
        count_file = len(file_list)
        if smaller_than_num == None:
            print(sub_dir)
            print(count_file)
            print()
        else:
            if count_file<smaller_than_num:
                print(sub_dir)
                print(count_file)
                print()


if __name__ == '__main__':
    main()