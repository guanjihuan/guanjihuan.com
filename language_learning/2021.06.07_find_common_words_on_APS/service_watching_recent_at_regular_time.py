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

ignore_inner = ['alt="Figure', 'the', '<math', 'to', 'of', 'in', 'under', '<i', 'and', 'by', 'The', 'at', 'with', 'up', 'be', 'above', 'below', 'are', 'is', 'for', 'that', 'as', 'we', '<a', 'abstract', 'abstract"','<span', 'which', 'We', 'such', 'has', 'two', 'these', 'it', 'all', 'results', 'result', 'each', 'have', 'between', 'on', 'an', 'can', 'also', 'from', 'Our', 'our', 'using', 'where', 'These', 'out', 'both', 'due', 'less', 'along', 'but', 'In', 'show', 'into', 'study', 'find', 'provide', 'change', '(<math','not', 'open', 'this', 'show', 'into', 'study', 'find', 'provide', 'change', 'present', 'Using', 'large', 'This', 'However', 'appear', 'studied', 'obtain', 'been', 'Both', 'they', 'effects', 'effect', 'compute', 'more', 'does', 'shown', 'Based', 'reveal', 'highly', 'number', 'However,', 'was', 'near', 'full', 'based', 'several', 'suggest', 'agreement', 'predicted', 'values', 'work', 'emphasize', 'without', 'or', 'work,', 'studies', 'future', 'identify', 'present.', 'predict', 'presence', 'their', 'were', 'From', 'its', 'By', 'how', 'ground', 'observed', 'recent', 'For', 'other', 'Here', 'test', 'further', 'Its', 'similar', 'however,', 'range', 'within', 'value', 'possible', 'may', 'than', 'low', 'us', 'obtained', 'around', 'consider', 'about', 'very', 'will', 'when', 'played', 'consist', 'consists', 'Here,', 'observe', 'gives', 'It', 'over', 'cannot', 'As', 'whose', 'new', 'some', 'only', 'from', 'yields', 'shows', 'data', 'direct', 'related', 'different', 'evidence', 'role', 'function', 'origin', 'specific', 'set', 'confirm', 'give', 'Moreover', 'develop', 'including', 'could', 'used', 'means', 'allows', 'make', 'e.g.,', 'provides', 'system', 'systems', 'field', 'fields', 'model', 'model,', 'state', 'states', 'states.', 'state.', 'band', 'bands', 'method', 'methods', 'nature', 'rate', 'zero', 'single', 'theory', 'first', 'one', 'complex', 'approach', 'schemes', 'terms', 'even', 'case', 'analysis', 'weight', 'volume', 'evolution', 'well', 'external', 'measured', 'introducing', 'dependence', 'properties', 'demonstrate', 'remains', 'through', 'measurements', 'samples', 'findings', 'respect', 'investigate', 'behavior', 'importance', 'considered', 'experimental', 'increase', 'propose', 'follows', 'increase', 'emerged', 'interesting', 'behaviors', 'influenced', 'paramount', 'indicate', 'Rev.', 'concepts', 'induced', 'zone', 'regions', 'exact', 'contribution', 'behavior', 'formation', 'measurements.', 'utilizing', 'constant', 'regime', 'features', 'strength', 'compare', 'determined', 'combination', 'compare', 'determined', 'At', 'inside', 'ambient', 'then', 'important', 'report', 'Moreover,', 'Despite', 'found', 'because', 'process', 'and,', 'significantly', 'realized', 'much', 'natural', 'since', 'grows', 'any', 'compared', 'while', 'forms.', 'appears', 'indicating', 'coefficient', 'suggested', 'time', 'exhibits', 'calculations.', 'developed', 'array', 'discuss', 'field', 'becomes', 'allowing', 'indicates', 'via', 'introduce', 'considering', 'times.', 'constructed', 'explain', 'form', 'owing', 'parameters.', 'parameter', 'operation', 'probe', 'experiments', 'interest', 'strategies', 'seen', 'emerge', 'generic', 'geometry', 'numbers', 'observation', 'avenue', 'theretically', 'three', 'excellent', 'amount', 'notable', 'example', 'being', 'promising', 'latter', 'little', 'imposed', 'put', 'resource', 'together', 'produce', 'successfully','there', 'enhanced', 'this', 'great', 'dirven', 'increasing','should', 'otherwise', 'Further', 'field,', 'known', 'changes', 'still', 'beyond', 'various', 'center', 'previously', 'way', 'peculiar', 'detailed', 'understanding', 'good', 'years', 'where', 'Me', 'origins', 'years.', 'attributed', 'known,', 'them', 'reported', 'no', 'systems', 'agree', 'examined', 'rise', 'calculate', 'those', 'particular', 'relation', 'defined', 'either', 'again', 'current', 'exhibit', 'calculated', 'here', 'made', 'Further', 'consisting', 'constitutes', 'originated', 'if', 'exceed', 'access']
num = 50
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day
for loop in range(2):
    if loop == 0:
        visit_link = "https://journals.aps.org/prb/recent"
        with open('prb_recent_most_common_words.txt', 'r', encoding='UTF-8') as f0:
            content_before = f0.read()
        f = open('prb_recent_most_common_words.txt', 'w', encoding='UTF-8') 
    elif loop == 1:
        visit_link = "https://journals.aps.org/prl/recent"
        with open('prl_recent_most_common_words.txt', 'r', encoding='UTF-8') as f0:
            content_before = f0.read()
        f = open('prl_recent_most_common_words.txt', 'w', encoding='UTF-8') 
    html = urlopen(visit_link).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    all_a_tag = soup.find_all('a', href=True)
    match_href = []
    for a_tag in all_a_tag:
        href = a_tag['href']
        if re.search('https://journals.aps.org/.*/abstract', href) or re.search('.*/abstract/', href):
            if href not in match_href  and re.search('\?', href)==None:
                if re.search('https://journals.aps.org', href)==None:
                    href = 'https://journals.aps.org'+ href
                match_href.append(href)
    all_word_list = []
    for href in match_href: 
        time.sleep(random.uniform(0,2))  # 爬虫休息一秒左右，简单伪装
        html = urlopen(href).read().decode('utf-8')
        abstract = re.findall('<a name="abstract">.*<li>Received', html, re.S)[0]
        word_list = abstract.split(' ')
        word_list_for_one_href = []
        for word in word_list:
            if 1<len(word)<35 and word not in ignore_inner and re.search('class=', word)==None and re.search('data-', word)==None and re.search('<', word)==None and re.search('>', word)==None and re.search('href', word)==None:
                if word not in word_list_for_one_href:
                    word_list_for_one_href.append(word)
                    all_word_list.append(word)
    most_common_words = Counter(all_word_list).most_common(num)
    f.write(str(year)+'.'+str(month).rjust(2,'0')+'.'+str(day).rjust(2,'0')+'|number_of_papers='+str(len(match_href)))
    for word in most_common_words:
        f.write('|'+str(word))
    f.write('\n\n')
    f.write(content_before)
    f.close()