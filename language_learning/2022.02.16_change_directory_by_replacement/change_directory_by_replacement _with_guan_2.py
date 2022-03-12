import guan
guan.change_directory_by_replacement(current_key_word='cloud/codes', new_key_word='local/data')
with open('data.txt', 'w') as f: # 保存数据
    f.write('Hello world') 