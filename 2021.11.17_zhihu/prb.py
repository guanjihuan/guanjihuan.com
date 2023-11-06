from bs4 import BeautifulSoup
from urllib.request import urlopen
import re  
import datetime


year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day


f = open('prb.html', 'w', encoding='UTF-8') 
f.write('<meta charset="utf-8"><style type="text/css">a{text-decoration: none;color: #0a5794;}a:hover {text-decoration: underline;color: red; }</style>')
f.write('<p>'+str(year)+'.'+str(month).rjust(2,'0')+'.'+str(day).rjust(2,'0')+' 已更新</p>')

match_href = []
for loop in range(1):
    if loop == 0:
        start_link = "https://journals.aps.org/prb/recent"  # 看第一页
    # elif loop == 1:
    #     start_link = "https://journals.aps.org/prb/recent?page=2"  # 看第二页
    html = urlopen(start_link).read().decode('utf-8')  # 打开网页
    soup = BeautifulSoup(html, features='lxml') # 放入soup中
    all_article = soup.find_all('div', {"class":"article panel article-result"}) 
    for article in all_article:
        all_a_tag = article.find_all('a', href=True)  # 获取超链接标签
        for a_tag in all_a_tag:
            href = a_tag['href']  # 超链接字符串
            if re.search('/abstract/', href): # 文章的链接
                if re.search('https://journals.aps.org', href)==None:  # 如果链接不是完整的，那么补充完整
                    href = 'https://journals.aps.org'+ href
                if href not in match_href and re.search('\?', href)==None:  # 链接不重复
                    match_href.append(href)
                    f.write('<li><a target=\"_blank\" href=\"')
                    f.write(href)   # 文章链接
                    f.write('\">')
                    f.write(a_tag.get_text())
                    f.write('</a>&nbsp;&nbsp;')
        info = article.find('h6', {"class": "pub-info"}).get_text()
        f.write(re.findall('– Published .*', info, re.S)[0][12:]+'</li>')
f.close()

