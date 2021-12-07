"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/18038
"""

import pygame
import time
import os
import random

# directory = 'words_mp3_breProns/' # 英音
directory = 'words_mp3_ameProns/' # 美音
pygame.mixer.init()
for root, dirs, files in os.walk(directory):
    num_array = list(range(len(files)))
    random.shuffle(num_array)  # 随机播放
    j0 = 0
    for i0 in num_array:
        j0 += 1
        print(j0)
        print(files[i0][:-4])
        print('https://www.ldoceonline.com/dictionary/'+files[i0][:-4], '\n')
        track = pygame.mixer.music.load(directory+files[i0])
        pygame.mixer.music.play()
        time.sleep(3)  # 调节间隔时间
        pygame.mixer.music.stop()