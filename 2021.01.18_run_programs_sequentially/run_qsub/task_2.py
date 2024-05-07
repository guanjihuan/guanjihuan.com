import guan
y = guan.load_data(filename='result_1')
guan.dump_data(y, filename='result_2')
print(guan.get_time())