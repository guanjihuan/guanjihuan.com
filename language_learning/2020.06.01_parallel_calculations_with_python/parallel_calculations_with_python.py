from multiprocessing import Process
import os
import time

def run_proc(name): # 要执行的代码
    start_time = time.perf_counter()
    for i in range(300000000):
        x = 100000^1000000000000
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
    p = Process(target=run_proc, args=('job1',))
    p.start()
    p = Process(target=run_proc, args=('job2',))
    p.start()
    p = Process(target=run_proc, args=('job3',))
    p.start()
    p = Process(target=run_proc, args=('job4',))
    p.start()
    p.join()   # join()方法可以等待子进程结束后再继续往下运行
    end_time = time.perf_counter()
    print('CPU执行时间(s)=', (end_time-start_time))

