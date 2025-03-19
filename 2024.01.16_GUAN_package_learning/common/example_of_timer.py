# 函数计时器
import guan

@guan.timer_decorator
def test1(a, b):
    import time
    print(a)
    time.sleep(2)
    print(b)
    print('Run finished.')

for _ in range(3):
    test1(10, b=20)

print()

def test2(a, b):
    import time
    print(a)
    time.sleep(2)
    print(b)
    print('Run finished.')

for _ in range(3):
    guan.timer(test2, 10, b=20)