"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/4536
"""

import multiprocessing

def run_proc(name, a, num): # 要执行的代码
    num.value = a

if __name__ == '__main__':
    num1 = multiprocessing.Value('d', 0.0)  # 共享内存
    num2 = multiprocessing.Value('d', 0.0)  # 共享内存
    p1 = multiprocessing.Process(target=run_proc, args=('job1', 100, num1))
    p2 = multiprocessing.Process(target=run_proc, args=('job2', 200, num2))
    p1.start()
    p2.start()
    p1.join()
    p2.join() 
    print(num1.value)
    print(num2.value)