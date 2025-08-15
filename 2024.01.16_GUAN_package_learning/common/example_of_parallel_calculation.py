# 并行计算
import guan
import time
import os

def run_proc(name):
    start_time = time.time()
    time.sleep(5)
    end_time = time.time()
    print ('Process id running on name %s = %s' % (name, os.getpid()), '; running time = %s' % (end_time-start_time))
    return f'name_{name}'

if __name__ == '__main__':
    result_array = guan.parallel_calculation_with_multiprocessing_Pool(func=run_proc, args_list=range(32), show_time=1)
    print(result_array)