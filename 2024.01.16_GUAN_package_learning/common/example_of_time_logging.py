# 运行统计
import guan
import time
guan.statistics_with_day_and_time(content='start')
for i in range(3):
    time.sleep(5)
    guan.statistics_with_day_and_time(f'end_of_{i}')