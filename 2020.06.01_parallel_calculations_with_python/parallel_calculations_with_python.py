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

    # 串行
    print('串行程序')
    print('Process id = %s.' % os.getpid())
    start_time = time.perf_counter()
    run_proc('job1')
    run_proc('job2')
    run_proc('job3')
    run_proc('job4')
    end_time = time.perf_counter()
    print('CPU执行时间(s)=', (end_time-start_time), '\n')

    # 并行
    print('并行程序')
    print('Process id = %s.' % os.getpid())
    start_time = time.perf_counter()
    p1 = multiprocessing.Process(target=run_proc, args=('job1',))
    p2 = multiprocessing.Process(target=run_proc, args=('job2',))
    p3 = multiprocessing.Process(target=run_proc, args=('job3',))
    p4 = multiprocessing.Process(target=run_proc, args=('job4',))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()  # join()方法可以等待子进程结束后再继续往下运行
    p2.join()  
    p3.join()  
    p4.join()
    end_time = time.perf_counter()
    print('运行时间(s)=', (end_time-start_time))