def main():
    directory = 'E:/test'
    creat_necessary_file(directory)
    # delete_file_with_specific_name(directory)

    # import guan
    # guan.creat_necessary_file(directory)
    # guan.delete_file_with_specific_name(directory)


def creat_necessary_file(directory, filename='readme', file_format='.md', content=''):
    import os
    directory_with_file = []
    for root, dirs, files in os.walk(directory):
        for i0 in range(len(files)):
            if root not in directory_with_file:
                directory_with_file.append(root)
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