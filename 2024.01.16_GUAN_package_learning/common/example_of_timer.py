# 函数计时器
import guan

@guan.timer_decorator
def test1(a, b):
    import time
    print(a)
    time.sleep(1)
    print(b)
    print('Run finished.')

for _ in range(2):
    test1(10, b=20)

print()

def test2(a, b):
    import time
    print(a)
    time.sleep(1)
    print(b)
    print('Run finished.')

for _ in range(2):
    guan.timer(test2, 100, b=200)