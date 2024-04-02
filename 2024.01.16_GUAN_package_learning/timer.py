# 函数的计时器
import guan

@guan.timer_decorator
def my_function():
    import time
    time.sleep(2)
    print('Run finished！')

for _ in range(3):
    my_function()