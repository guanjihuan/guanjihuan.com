"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4536
"""

from multiprocessing import Process
import os
import time

def run_proc(name, a=0, b=-1): # 要执行的代码
    start_time = time.perf_counter()
    time.sleep(2)
    end_time = time.perf_counter()
    print ('Process id running on %s = %s' % (name, os.getpid()), f'; Values: a={a}, b={b}', '; running time = %s' % (end_time-start_time))


if __name__ == '__main__':

    print('并行程序')
    print('Process id = %s.' % os.getpid())
    start_time = time.perf_counter()
    p1 = Process(target=run_proc, kwargs={'name':'job1', 'a':10, 'b':100})
    p2 = Process(target=run_proc, kwargs={'name':'job2', 'a':20})
    p3 = Process(target=run_proc, kwargs={'name':'job3', 'b':300})
    p4 = Process(target=run_proc, kwargs={'name':'job4'})
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