"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/13623
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re  
from collections import Counter
import datetime
import random
import time


# time.sleep(random.uniform(0,1800))  # 爬虫简单伪装，在固定时间后0到30分钟后开始运行。调试的时候把该语句注释。
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day


# 获取链接
try:
    with open('prl_link_list.txt', 'r', encoding='UTF-8') as f:  # 如果文件存在
        link_list = f.read().split('\n')   # 历史已经访问过的链接（数组类型）
except:
    with open('prl_link_list.txt', 'w', encoding='UTF-8') as f:  # 如果文件不存在
        link_list = [] 
f = open('prl_link_list.txt', 'a', encoding='UTF-8')  # 打开文件（补充）
f.write('\nLink list obtained on '+str(year)+'.'+str(month).rjust(2,'0')+'.'+str(day).rjust(2,'0')+':\n')
match_href = []  # 在本次运行中满足条件的链接
for loop in range(3):
    if loop == 0:
        start_link = "https://journals.aps.org/prl/recent?page=1"  # 看第一页
    elif loop == 1:
        start_link = "https://journals.aps.org/prl/recent?page=2"  # 看第二页
    elif loop == 2: 
        start_link = "https://journals.aps.org/prl/recent?page=3"  # 看第三页（三页基本上覆盖了当天的所有更新）
    html = urlopen(start_link).read().decode('utf-8')  # 打开网页
    soup = BeautifulSoup(html, features='lxml') # 放入soup中
    all_a_tag = soup.find_all('a', href=True)  # 获取超链接标签
    for a_tag in all_a_tag:
        href = a_tag['href']  # 超链接字符串
        if re.search('/abstract/', href): # 文章的链接
            if re.search('https://journals.aps.org', href)==None:  # 如果链接不是完整的，那么补充完整
                href = 'https://journals.aps.org'+ href
            if href not in match_href and href not in link_list and re.search('\?', href)==None:  # 链接不重复
                match_href.append(href)
                f.write(href+'\n')
f.close()



# 获取摘要
try:
    f = open('prl_all.txt', 'a', encoding='UTF-8')  # 全部记录
except:
    f = open('prl_all.txt', 'w', encoding='UTF-8')  # 如果文件不存在
try:
    f_month = open('prl_'+str(year)+'.'+str(month).rjust(2,'0')+'.txt', 'a', encoding='UTF-8')  # 一个月的记录
except:
    f_month = open('prl_'+str(year)+'.'+str(month).rjust(2,'0')+'.txt', 'w', encoding='UTF-8')  # 如果文件不存在
f.write('\n\n['+str(year)+'.'+str(month).rjust(2,'0')+'.'+str(day).rjust(2,'0')+'][total number='+str(len(match_href))+']\n\n\n')
f_month.write('\n\n['+str(year)+'.'+str(month).rjust(2,'0')+'.'+str(day).rjust(2,'0')+'][total number='+str(len(match_href))+']\n\n\n')
print('total number=', len(match_href))  # 调试的时候显示这个
i00 = 0
for href in match_href: 
    i00 += 1
    print('reading number', i00, '...')  # 调试的时候显示这个
    # time.sleep(random.uniform(10,110))  # 爬虫简单伪装，休息一分钟左右。如果链接个数有60个，那么程序运行时间延长60分钟。调试的时候把该语句注释。
    try:
        html = urlopen(href).read().decode('utf-8')   # 打开文章链接
        soup = BeautifulSoup(html, features='lxml') # 放入soup中
        title = soup.title   # 文章标题
        f.write(str(title.get_text())+'\n\n')   
        f_month.write(str(title.get_text())+'\n\n') 
        f.write(str(href)+'\n\n')   # 文章链接
        f_month.write(str(href)+'\n\n') 
        abstract = re.findall('"yes"><p>.*</p><div', html, re.S)[0][9:-8]  # 文章摘要
        word_list = abstract.split(' ')  # 划分单词
        for word in word_list:
            if re.search('<', word)==None and re.search('>', word)==None:  # 有些内容满足过滤条件，因此信息可能会丢失。
                f.write(word+' ')
                f_month.write(word+' ')
        f.write('\n\n\n')
        f_month.write('\n\n\n')
    except:
        pass
f.close()