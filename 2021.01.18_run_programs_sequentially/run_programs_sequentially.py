import os
import time

start = time.time()

print('程序1开始的时间：', time.ctime())
start1 = time.time()
os.chdir('D:')  # 代码位置
os.system('python a.py')  # 运行a.py
end1 = time.time()
print('程序1运行时间(min)=', (end1-start1)/60,'\n')

print('程序2开始的时间：', time.ctime())
start2 = time.time()
os.chdir('E:')  # 代码位置
os.system('python b.py')  # 运行b.py
end2 = time.time()
print('程序2运行时间(min)=', (end2-start2)/60, '\n')

end = time.time()
print('总运行时间(min)=', (end-start)/60)