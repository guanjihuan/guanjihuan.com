import os
import time
os.system('qsub task_1.sh')
while True:
    if os.path.exists('./complete_1.txt'):
        os.system('qsub task_2.sh')
        break
    time.sleep(180)