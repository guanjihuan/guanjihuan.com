# 变量写入文件
import guan
import numpy as np
data = np.array([1, 2, 3])
guan.dump_data(data, filename='a')
loaded_data = guan.load_data(filename='a')
print(loaded_data)