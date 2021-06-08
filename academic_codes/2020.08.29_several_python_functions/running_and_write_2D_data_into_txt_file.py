import numpy as np
from math import * 
# import os
# os.chdir('D:/data')  # 设置路径 


f = open('a.txt', 'w')
f.write('0       ')
for k1 in np.arange(-pi, pi, 0.05):
    f.write(str(k1)+'   ')
f.write('\n')  
for k2 in np.arange(-pi, pi, 0.05):
    f.write(str(k2)+'   ') 
    for k1 in np.arange(-pi, pi, 0.05):
        data = 1000  # 运算数据
        f.write(str(data)+'   ') 
    f.write('\n') 
f.close()