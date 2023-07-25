from multiprocessing import Process
import time

def f(name):
    time.sleep(5)
    print('Hello', name)

if __name__ == '__main__':
    start_time = time.time()
    p1 = Process(target=f, args=('Bob',))
    p2 = Process(target=f, args=('Alice',))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end_time = time.time()
    print(end_time - start_time, '\n')

    start_time = time.time()
    f('Bob')
    f('Alice')
    end_time = time.time()
    print(end_time - start_time)