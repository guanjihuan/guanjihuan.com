import h5py
import numpy as np

# 写入数据
with h5py.File('data.h5', 'w') as f:
    f.create_dataset('array', data=np.random.rand(3, 3))
    f.attrs['info'] = '3x3随机矩阵'

# 读取数据
with h5py.File('data.h5', 'r') as f:
    array_data = f['array'][:]
    info = f.attrs['info']
    
print('数组数据:')
print(array_data)
print('信息:', info)