from multiprocessing import Process
import os
import time
import numpy as np
import guan

def main(parameter_array, task_index):
    print ('Process id = %s' % (os.getpid()))
    result_array = []
    for parameter in parameter_array:
        result = parameter*2
        result_array.append(result)
    time.sleep(np.random.uniform(1,10))
    guan.write_one_dimensional_data(parameter_array, result_array, filename='task_index='+str(task_index))

if __name__ == '__main__':
    cpus = 4
    parameter_array_all = np.arange(0, 17, 1) 
    start_time = time.perf_counter()
    process_array = []
    for task_index in range(cpus):
        parameter_array = guan.preprocess_for_parallel_calculations(parameter_array_all, cpus, task_index)
        process_array.append(Process(target=main, args=(parameter_array, task_index)))
    for process in process_array: # 运行子进程
        process.start()
    for process in process_array: # 等待子进程完成
        process.join() 
    end_time = time.perf_counter()
    print('运行时间=', (end_time-start_time), '\n')
    f = open('result.txt', 'w')
    for task_index in range(cpus):
        with open('task_index='+str(task_index)+'.txt', 'r') as f0:
            text = f0.read()
        f.write(text)
    f.close()