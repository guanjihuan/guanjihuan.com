"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4536
"""

import multiprocessing
import os
import time

def run_proc(name):
    start_time = time.perf_counter()
    time.sleep(2)
    end_time = time.perf_counter()
    print ('Process id running on %s = %s' % (name, os.getpid()), '; running time = %s' % (end_time-start_time))

if __name__ == '__main__':
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        results = pool.map(run_proc, range(64))
    end_time = time.time()
    print(end_time - start_time)