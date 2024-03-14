import guan
import numpy as np
import datetime

file_list_60 = guan.get_all_filenames_in_directory(directory='./all_to_2024_03_07/stock_data_60', \
                                        file_format=None, show_root_path=0, sort=1, include_subdirectory=1)
file_list_00 = guan.get_all_filenames_in_directory(directory='./all_to_2024_03_07/stock_data_00', \
                                        file_format=None, show_root_path=0, sort=1, include_subdirectory=1)


len_stock_60 = len(file_list_60)
guan.make_directory('./2018_01_01_to_2024_03_07/')
guan.make_directory('./2018_01_01_to_2024_03_07/stock_data_60/')
for i00 in range(len_stock_60):
    stock_data = guan.load_data('./all_to_2024_03_07/stock_data_60/'+file_list_60[i00], file_format='')
    num_data = len(stock_data)
    new_stock_data = []
    for i0 in range(num_data):
        if stock_data[i0, 0]>datetime.date(2018, 1, 1):
            new_stock_data.append(list(stock_data[i0, :]))
    new_stock_data = np.array(new_stock_data)
    guan.dump_data(data=new_stock_data, filename='./2018_01_01_to_2024_03_07/stock_data_60/'+file_list_60[i00], file_format='')

print('数据处理结束1')

len_stock_00 = len(file_list_00)
guan.make_directory('./2018_01_01_to_2024_03_07/stock_data_00/')
for i00 in range(len_stock_00):
    stock_data = guan.load_data('./all_to_2024_03_07/stock_data_00/'+file_list_00[i00], file_format='')
    num_data = len(stock_data)
    new_stock_data = []
    for i0 in range(num_data):
        if stock_data[i0, 0]>datetime.date(2018, 1, 1):
            new_stock_data.append(list(stock_data[i0, :]))
    new_stock_data = np.array(new_stock_data)
    guan.dump_data(data=new_stock_data, filename='./2018_01_01_to_2024_03_07/stock_data_00/'+file_list_00[i00], file_format='')

print('数据处理结束2')