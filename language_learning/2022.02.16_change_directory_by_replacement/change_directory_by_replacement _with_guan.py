import guan
guan.change_directory_by_replacement(current_key_word='codes', new_key_word='data')
with open('data.txt', 'w') as f: # 保存数据
    f.write('Hello world') 