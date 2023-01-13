"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/26113
"""

# 仅支持文件名判断是否重复，不支持对文件内容的判断。
# 如需对文件名和内容都判断，需要计算文件的哈希值。这里暂时不考虑。


def main():
    directory = 'E:/test'
    repeated_file = find_repeated_file_with_same_filename(directory)
    print(repeated_file)

    # import guan
    # repeated_file = guan.find_repeated_file_with_same_filename(directory='./', ignored_directory_with_words=[], ignored_file_with_words=[], num=1000)
    # print(repeated_file)


def find_repeated_file_with_same_filename(directory='./', ignored_directory_with_words=[], ignored_file_with_words=[], num=1000):
    import os
    from collections import Counter
    file_list = []
    for root, dirs, files in os.walk(directory):
        for i0 in range(len(files)):
            file_list.append(files[i0])
            for word in ignored_directory_with_words:
                if word in root:
                    file_list.remove(files[i0])       
            for word in ignored_file_with_words:
                if word in files[i0]:
                    try:
                        file_list.remove(files[i0])   
                    except:
                        pass 
    count_file = Counter(file_list).most_common(num)
    repeated_file = []
    for item in count_file:
        if item[1]>1:
            repeated_file.append(item)
    return repeated_file


if __name__ == '__main__':
    main()