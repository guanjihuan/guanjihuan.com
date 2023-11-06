"""
This code is supported by the website: https://www.guanjihuan.com
"""

from urllib import response
from bs4 import BeautifulSoup
import re
import requests
import urllib.request
import os
import ssl
from urllib.request import urlopen

ssl._create_default_https_context = ssl._create_unverified_context
html = urllib.request.urlopen("https://www.guanjihuan.com/archives/10897").read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
all_a_tag = soup.find_all('a', href=True)
for a_tag in all_a_tag:
    href = a_tag['href']
    if re.search('https://www.merriam-webster.com/dictionary/', href):
        print(href[43:])
        exist = os.path.exists('prons/'+href[43:]+'.mp3')
        if exist:
            continue
        header = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}   # 头部信息
        html = urlopen(href).read().decode('utf-8')
        mp3_file = re.findall('https://media.merriam-webster.com/audio/prons/en/us/mp3/.*.mp3",', html, re.S)[0][:-2]
        print(mp3_file[:-2])
        print()
        r = requests.get(mp3_file, headers=header, stream=True)
        with open('prons/'+href[43:]+'.mp3', 'wb') as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)