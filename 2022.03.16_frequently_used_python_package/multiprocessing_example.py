from multiprocessing import Process
import time

def f(name):
    for i in range(5):
        time.sleep(1)
        print('Hello', name, i)

if __name__ == '__main__':
    start_time = time.time()
    f('A')
    f('B')
    end_time = time.time()
    print(end_time - start_time, '\n')

    start_time = time.time()
    p1 = Process(target=f, args=('A',))
    p2 = Process(target=f, args=('B',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end_time = time.time()
    print(end_time - start_time)