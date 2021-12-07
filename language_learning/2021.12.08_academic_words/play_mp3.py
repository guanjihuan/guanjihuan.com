import pygame
import time
import os
import random

# directory = 'C:/Users/user/Desktop/words_mp3_breProns/' # 英音
directory = 'C:/Users/user/Desktop/words_mp3_ameProns/' # 美音
pygame.mixer.init()
for root, dirs, files in os.walk(directory):
    num_array = list(range(len(files)))
    random.shuffle(num_array)  # 随机播放
    for i0 in num_array:
        print(files[i0][:-4])
        print('https://www.ldoceonline.com/dictionary/'+files[i0][:-4], '\n')
        track = pygame.mixer.music.load(directory+files[i0])
        pygame.mixer.music.play()
        time.sleep(3)  # 调节间隔时间
        pygame.mixer.music.stop()