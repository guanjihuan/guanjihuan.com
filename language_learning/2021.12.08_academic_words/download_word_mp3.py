from bs4 import BeautifulSoup
import re
import requests
import urllib.request
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
html = urllib.request.urlopen("https://www.guanjihuan.com/archives/4418").read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
all_a_tag = soup.find_all('a', href=True)
for a_tag in all_a_tag:
    href = a_tag['href']
    if re.search('https://www.ldoceonline.com/dictionary/', href):
        print(href[39:])
        exist_1 = os.path.exists('words_mp3_breProns/'+href[39:]+'.mp3')
        exist_2 = os.path.exists('words_mp3_breProns/'+href[39:]+'.mp3')
        if exist_1 and exist_2:
            continue
        header = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}   # 头部信息
        request = urllib.request.Request(href,headers=header)
        reponse = urllib.request.urlopen(request).read()
        soup2 = BeautifulSoup(reponse, features='lxml') 
        span = soup2.find_all('span', {"class":"speaker brefile fas fa-volume-up hideOnAmp"})
        for span0 in span:
            href2 = span0['data-src-mp3']
            if re.search('https://www.ldoceonline.com/media/english/breProns/', href2):
                print(href2)
                r = requests.get(href2, headers=header, stream=True)
                with open('words_mp3_breProns/'+href[39:]+'.mp3', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=32):
                        f.write(chunk)
            break
        span = soup2.find_all('span', {"class":"speaker amefile fas fa-volume-up hideOnAmp"})
        for span0 in span:
            href2 = span0['data-src-mp3']
            if re.search('https://www.ldoceonline.com/media/english/ameProns/', href2):
                print(href2)
                r = requests.get(href2, headers=header, stream=True)
                with open('words_mp3_ameProns/'+href[39:]+'.mp3', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=32):
                        f.write(chunk)
            break
        print()