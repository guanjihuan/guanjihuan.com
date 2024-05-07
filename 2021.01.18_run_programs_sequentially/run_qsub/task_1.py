import time
import guan
print(guan.get_time())
time.sleep(60)
x = ['test_001']
guan.dump_data(x, filename='result_1')
print(guan.get_time())
guan.make_file('./complete_1.txt')