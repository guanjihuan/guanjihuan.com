"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/18038
"""

from bs4 import BeautifulSoup
import re
import urllib.request
import os
import pygame
import time
import ssl
import random
ssl._create_default_https_context = ssl._create_unverified_context
html = urllib.request.urlopen("https://www.guanjihuan.com/archives/4418").read().decode('utf-8')

# directory = 'words_mp3_breProns/' # 英音
directory = 'words_mp3_ameProns/' # 美音
pygame.mixer.init()
soup = BeautifulSoup(html, features='lxml')
contents = re.findall('<h2>.*?<h2>', html, re.S)
# random.shuffle(contents)  # 随机播放
for content in contents:
    soup2 = BeautifulSoup(content, features='lxml')
    all_h2 = soup2.find_all('h2')
    for h2 in all_h2:
        if re.search('\d*. ', h2.get_text()):
            word = re.findall('[a-zA-Z].*', h2.get_text(), re.S)[0]
            exist = os.path.exists(directory+word+'.mp3')
            if not exist:
                continue
            print(h2.get_text())
            # print('https://www.ldoceonline.com/dictionary/'+word)
            track = pygame.mixer.music.load(directory+word+'.mp3')
            pygame.mixer.music.play()
            translation = re.findall('<p>.*?</p>', content, re.S)[0][3:-4]
            time.sleep(2.5)
            print(translation, '\n')
            time.sleep(0.5)  # 调节间隔时间
            pygame.mixer.music.stop()