"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4536
"""

import multiprocessing
import os
import time

def run_proc(name): # 要执行的代码
    start_time = time.perf_counter()
    time.sleep(2)
    end_time = time.perf_counter()
    print ('Process id running on %s = %s' % (name, os.getpid()), '; running time = %s' % (end_time-start_time))

if __name__ == '__main__':
    start_time = time.perf_counter()

    # 循环创建进程
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=run_proc, args=(f'job{i}',))
        processes.append(p)
        p.start()

    # 等待所有进程完成
    for p in processes:
        p.join()

    end_time = time.perf_counter()
    print('运行时间(s)=', (end_time-start_time))