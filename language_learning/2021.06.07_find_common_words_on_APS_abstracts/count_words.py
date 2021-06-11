"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/13623
"""

import re  
from collections import Counter


def main():
    file_name = 'prb_all.txt'
    with open(file_name, 'r', encoding='UTF-8') as f:  # 打开文件
        paper_list = f.read().split('\n\n\n')  # 通过三个回车划分不同文章
    word_list = []  
    ignore = ignore_words()  # 过滤常见单词
    for paper in paper_list:
        word_list_in_one_paper = []
        if len(paper)>20:  # 通过字符串长度过滤日期
            content_list = paper.split('\n\n')  # 通过两个回车划分内容
            for content in content_list:
                if re.search('https://', content)==None: # 过滤文章链接
                    words = content.split(' ')  # 通过空格划分单词
                    for word in words:
                        if word not in word_list_in_one_paper:  # 一篇文章的某个单词只统计一次
                            if word not in ignore and len(word)>1:  # 过滤词汇
                                word_list.append(word)
                                word_list_in_one_paper.append(word)       
    num = 300
    most_common_words = Counter(word_list).most_common(num)  # 统计出现最多的num个词汇
    print('\n出现频率最高的前', num, '个词汇：')
    for word in most_common_words:
        print(word)


def ignore_words(): # 可自行增删
    ignore = ['Phys.', 'the', 'to', 'of', 'in', 'under', 'and', 'by', 'The', 'at', 'with', 'up', 'be', 'above', 'below', 'are', 'is', 'for', 'that', 'as', 'we', '<a', 'abstract', 'abstract"','<span', 'which', 'We', 'such', 'has', 'two', 'these', 'it', 'all', 'results', 'result', 'each', 'have', 'between', 'on', 'an', 'can', 'also', 'from', 'Our', 'our', 'using', 'where', 'These', 'out', 'both', 'due', 'less', 'along', 'but', 'In', 'show', 'into', 'study', 'find', 'provide', 'change','not', 'open', 'this', 'show', 'into', 'study', 'find', 'provide', 'change', 'present', 'Using', 'large', 'This', 'However', 'appear', 'studied', 'obtain', 'been', 'Both', 'they', 'effects', 'effect', 'compute', 'more', 'does', 'shown', 'Based', 'reveal', 'highly', 'number', 'However,', 'was', 'near', 'full', 'based', 'several', 'suggest', 'agreement', 'predicted', 'values', 'work', 'emphasize', 'without', 'or', 'work,', 'studies', 'future', 'identify', 'present.', 'predict', 'presence', 'their', 'were', 'From', 'its', 'By', 'how', 'ground', 'observed', 'recent', 'For', 'other', 'Here', 'test', 'further', 'Its', 'similar', 'however,', 'range', 'within', 'value', 'possible', 'may', 'than', 'low', 'us', 'obtained', 'around', 'consider', 'about', 'very', 'will', 'when', 'played', 'consist', 'consists', 'Here,', 'observe', 'gives', 'It', 'over', 'cannot', 'As', 'whose', 'new', 'some', 'only', 'from', 'yields', 'shows', 'data', 'direct', 'related', 'different', 'evidence', 'role', 'function', 'origin', 'specific', 'set', 'confirm', 'give', 'Moreover', 'develop', 'including', 'could', 'used', 'means', 'allows', 'make', 'e.g.,', 'provides', 'system', 'systems', 'field', 'fields', 'model', 'model,', 'state', 'states', 'states.', 'state.', 'band', 'bands', 'method', 'methods', 'nature', 'rate', 'zero', 'single', 'theory', 'first', 'one', 'complex', 'approach', 'schemes', 'terms', 'even', 'case', 'analysis', 'weight', 'volume', 'evolution', 'well', 'external', 'measured', 'introducing', 'dependence', 'properties', 'demonstrate', 'remains', 'through', 'measurements', 'samples', 'findings', 'respect', 'investigate', 'behavior', 'importance', 'considered', 'experimental', 'increase', 'propose', 'follows', 'increase', 'emerged', 'interesting', 'behaviors', 'influenced', 'paramount', 'indicate', 'Rev.', 'concepts', 'induced', 'zone', 'regions', 'exact', 'contribution', 'behavior', 'formation', 'measurements.', 'utilizing', 'constant', 'regime', 'features', 'strength', 'compare', 'determined', 'combination', 'compare', 'determined', 'At', 'inside', 'ambient', 'then', 'important', 'report', 'Moreover,', 'Despite', 'found', 'because', 'process', 'and,', 'significantly', 'realized', 'much', 'natural', 'since', 'grows', 'any', 'compared', 'while', 'forms.', 'appears', 'indicating', 'coefficient', 'suggested', 'time', 'exhibits', 'calculations.', 'developed', 'array', 'discuss', 'field', 'becomes', 'allowing', 'indicates', 'via', 'introduce', 'considering', 'times.', 'constructed', 'explain', 'form', 'owing', 'parameters.', 'parameter', 'operation', 'probe', 'experiments', 'interest', 'strategies', 'seen', 'emerge', 'generic', 'geometry', 'numbers', 'observation', 'avenue', 'theretically', 'three', 'excellent', 'amount', 'notable', 'example', 'being', 'promising', 'latter', 'little', 'imposed', 'put', 'resource', 'together', 'produce', 'successfully','there', 'enhanced', 'this', 'great', 'dirven', 'increasing','should', 'otherwise', 'Further', 'field,', 'known', 'changes', 'still', 'beyond', 'various', 'center', 'previously', 'way', 'peculiar', 'detailed', 'understanding', 'good', 'years', 'where', 'Me', 'origins', 'years.', 'attributed', 'known,', 'them', 'reported', 'no', 'systems', 'agree', 'examined', 'rise', 'calculate', 'those', 'particular', 'relation', 'defined', 'either', 'again', 'current', 'exhibit', 'calculated', 'here', 'made', 'Further', 'consisting', 'constitutes', 'originated', 'if', 'exceed', 'access']
    return ignore


if __name__ == '__main__':
    main()