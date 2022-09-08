"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/25699
"""


def main():
    import os
    directory = 'E:/literature'
    write_file_list_in_markdown(directory)
    # write_file_list_in_markdown(directory, banned_type=['.md'], hide_file_type=1, divided_line=1, show_second_number=1, show_third_number=1)
    # write_file_list_in_markdown(directory, filename='a', reverse_positive_or_negative=1, starting_from_h1=None, banned_type=[], hide_file_type=None, divided_line=None, show_second_number=None, show_third_number=None)
    
    # import guan
    # guan.write_file_list_in_markdown(directory)
    # guan.write_file_list_in_markdown(directory, banned_type=['.md'], hide_file_type=1, divided_line=1, show_second_number=1, show_third_number=1)
    # guan.write_file_list_in_markdown(directory, filename='a', reverse_positive_or_negative=1, starting_from_h1=None, banned_type=[], hide_file_type=None, divided_line=None, show_second_number=None, show_third_number=None)


def write_file_list_in_markdown(directory, filename='a', reverse_positive_or_negative=1, starting_from_h1=None, banned_type=[], hide_file_type=None, divided_line=None, show_second_number=None, show_third_number=None): 
    import os
    f = open(filename+'.md', 'w', encoding="utf-8")
    filenames1 = os.listdir(directory)
    u0 = 0
    for filename1 in filenames1[::reverse_positive_or_negative]:
        filename1_with_path = os.path.join(directory,filename1) 
        if os.path.isfile(filename1_with_path):  # 文件
            if os.path.splitext(filename1)[1] not in banned_type:
                if hide_file_type == None:
                    f.write('+ '+str(filename1)+'\n')
                else:
                    f.write('+ '+str(os.path.splitext(filename1)[0])+'\n')
        else:  # 文件夹
            u0 += 1
            if divided_line != None and u0 != 1:
                f.write('\n--------\n\n')
            if starting_from_h1 == None:
                f.write('#')
            f.write('# '+str(filename1)+'\n')

            filenames2 = os.listdir(filename1_with_path) 
            i0 = 0     
            for filename2 in filenames2[::reverse_positive_or_negative]:
                filename2_with_path = os.path.join(directory, filename1, filename2) 
                if os.path.isfile(filename2_with_path):  # 文件
                    if os.path.splitext(filename2)[1] not in banned_type:
                        if hide_file_type == None:
                            f.write('+ '+str(filename2)+'\n')
                        else:
                            f.write('+ '+str(os.path.splitext(filename2)[0])+'\n')
                else:    # 文件夹
                    i0 += 1
                    if starting_from_h1 == None:
                        f.write('#')
                    if show_second_number != None:
                        f.write('## '+str(i0)+'. '+str(filename2)+'\n')
                    else:
                        f.write('## '+str(filename2)+'\n')
                    
                    j0 = 0
                    filenames3 = os.listdir(filename2_with_path)
                    for filename3 in filenames3[::reverse_positive_or_negative]:
                        filename3_with_path = os.path.join(directory, filename1, filename2, filename3) 
                        if os.path.isfile(filename3_with_path):    # 文件
                            if os.path.splitext(filename3)[1] not in banned_type:
                                if hide_file_type == None:
                                    f.write('+ '+str(filename3)+'\n')
                                else:
                                    f.write('+ '+str(os.path.splitext(filename3)[0])+'\n')
                        else:   # 文件夹
                            j0 += 1
                            if starting_from_h1 == None:
                                f.write('#')
                            if show_third_number != None:
                                f.write('### ('+str(j0)+') '+str(filename3)+'\n')
                            else:
                                f.write('### '+str(filename3)+'\n')

                            filenames4 = os.listdir(filename3_with_path)
                            for filename4 in filenames4[::reverse_positive_or_negative]:
                                filename4_with_path = os.path.join(directory, filename1, filename2, filename3, filename4) 
                                if os.path.isfile(filename4_with_path):   # 文件
                                    if os.path.splitext(filename4)[1] not in banned_type:
                                        if hide_file_type == None:
                                            f.write('+ '+str(filename4)+'\n')
                                        else:
                                            f.write('+ '+str(os.path.splitext(filename4)[0])+'\n')
                                else:     # 文件夹
                                    if starting_from_h1 == None:
                                        f.write('#')
                                    f.write('#### '+str(filename4)+'\n')

                                    filenames5 = os.listdir(filename4_with_path)
                                    for filename5 in filenames5[::reverse_positive_or_negative]:
                                        filename5_with_path = os.path.join(directory, filename1, filename2, filename3, filename4, filename5) 
                                        if os.path.isfile(filename5_with_path):    # 文件
                                            if os.path.splitext(filename5)[1] not in banned_type:
                                                if hide_file_type == None:
                                                    f.write('+ '+str(filename5)+'\n')
                                                else:
                                                    f.write('+ '+str(os.path.splitext(filename5)[0])+'\n')
                                        else:   # 文件夹
                                            if starting_from_h1 == None:
                                                f.write('#')
                                            f.write('##### '+str(filename5)+'\n')
    f.close()


if __name__ == '__main__':
    main()