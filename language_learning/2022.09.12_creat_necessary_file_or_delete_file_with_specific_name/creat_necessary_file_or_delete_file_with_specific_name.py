"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/25943
"""


def main():
    directory = 'E:/test'
    creat_necessary_file(directory)
    # delete_file_with_specific_name(directory)

    # import guan
    # guan.creat_necessary_file(directory)
    # guan.delete_file_with_specific_name(directory)


def creat_necessary_file(directory, filename='readme', file_format='.md', content='', overwrite=None, ignored_directory_with_words=[]):
    import os
    directory_with_file = []
    ignored_directory = []
    for root, dirs, files in os.walk(directory):
        for i0 in range(len(files)):
            if root not in directory_with_file:
                directory_with_file.append(root)
            if files[i0] == filename+file_format:
                if root not in ignored_directory:
                    ignored_directory.append(root)
    if overwrite == None:
        for root in ignored_directory:
            directory_with_file.remove(root)
    ignored_directory_more =[]
    for root in directory_with_file: 
        for word in ignored_directory_with_words:
            if word in root:
                if root not in ignored_directory_more:
                    ignored_directory_more.append(root)
    for root in ignored_directory_more:
        directory_with_file.remove(root) 
    for root in directory_with_file:
        os.chdir(root)
        f = open(filename+file_format, 'w', encoding="utf-8")
        f.write(content)
        f.close()
    

def delete_file_with_specific_name(directory, filename='readme', file_format='.md'):
      import os
      for root, dirs, files in os.walk(directory):
        for i0 in range(len(files)):
            if files[i0] == filename+file_format:
                os.remove(root+'/'+files[i0])


if __name__ == '__main__':
    main()