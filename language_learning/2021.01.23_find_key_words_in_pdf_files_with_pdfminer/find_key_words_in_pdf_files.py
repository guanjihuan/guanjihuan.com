"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/9129
"""

import os
import re 
import time
import logging 
logging.Logger.propagate = False 
logging.getLogger().setLevel(logging.ERROR)  # 只显示error级别的通知


def main():
    # 参数
    key_word_array = ['photonic', 'Berry phase']
    original_path = 'D:\\文献'
    
    # 查找所有的PDF文件路径
    pdf_file_all = find_files_pdf(original_path)
    print('\n该文件夹下总共有', len(pdf_file_all), '个PDF文件。\n')
    
    f = open('error.txt','w',encoding='utf-8')
    f.close()
    for key_word in key_word_array:
        f = open(str(key_word)+'.txt','w',encoding='utf-8')
        f.write('该文件夹下总共有'+str(len(pdf_file_all))+'个PDF文件。\n')
        f.close()

    # 查找包含关键词的PDF文件
    i0 = 1
    begin = time.time()
    for pdf_file in pdf_file_all:
        print('查找第', i0, '个文件，', end='')
        begin0 = time.time()
        try: 
            content = get_text_from_pdf(pdf_file)
            for key_word in key_word_array:
                if re.search(re.compile(key_word),content):
                    print('发现文件！关键词', key_word, '对应的文件位置在：\n\n', pdf_file, '\n')
                    with open(str(key_word)+'.txt','a',encoding='utf-8') as f:
                        f.write('\n查找第'+str(i0)+'个文件时发现文件！位置在：\n'+pdf_file+'\n')
        except: 
            print('出现异常！位置在：\n\n', pdf_file, '\n')
            with open('error.txt','a',encoding='utf-8') as f:
                f.write('\n解析第'+str(i0)+'个文件时出现异常！位置在：\n'+pdf_file+'\n')
        end0 = time.time()
        print('用时', end0-begin0, '秒')
        i0 += 1
    print('\n全部搜索结束！')
    end = time.time()
    print('\n总共用时：', (end-begin)/60, '分')


def find_files_pdf(path):  # 查找所有PDF文件
    file_all = find_files(path)
    pdf_file_all = []
    for file0 in file_all:
        if re.search(re.compile('^fdp.'),file0[::-1]): # 如果文件是以.pdf结尾
            pdf_file_all.append(file0)
    return pdf_file_all


def find_files(path):  # 查找所有文件
    file_all = []
    path_next_loop = [path]
    for i in range(10000):  # i为文件在文件夹中的深度
        file_all_in_one_loop, path_next_loop = find_files_loop_module(path_next_loop)
        for file_in_one_loop in file_all_in_one_loop:
            file_all.append(file_in_one_loop)
        if path_next_loop == []:
            break
    return file_all


def find_files_loop_module(path_all): # 查找文件的一个循环模块
    file_all_in_one_loop = []
    path_next_loop = []
    for path in path_all:
        filenames = os.listdir(path)
        for filename in filenames:
            filename = os.path.join(path,filename) 
            if os.path.isfile(filename): # 如果是文件
                file_all_in_one_loop.append(filename) 
            else:  # 如果是文件夹
                path_next_loop.append(filename)
    return file_all_in_one_loop, path_next_loop


def get_text_from_pdf(file_path):  # 从PDF中获取文本
    from pdfminer.pdfparser import PDFParser, PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.layout import LAParams, LTTextBox
    from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(open(file_path, 'rb'))
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        content = ''
        for page in doc.get_pages():
            interpreter.process_page(page)                        
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象，里面存放着这个 page 解析出的各种对象
            # 包括 LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等                            
            for x in layout:
                if isinstance(x, LTTextBox):
                    # print(x.get_text().strip())
                    content  = content + x.get_text().strip()
    return content


if __name__ == "__main__":
    main()