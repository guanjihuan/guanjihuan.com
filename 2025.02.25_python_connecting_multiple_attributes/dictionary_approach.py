"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45135
"""

atom_dict_list = []
index = 0
for i0 in range(3):
    for j0 in range(3):
        atom_dict= {
            'name': 'atom',
            'index': index, 
            'x': i0,
            'y': j0,
            'z': 0,
        }
        atom_dict_list.append(atom_dict)
        index += 1

print(atom_dict_list)
for atom_dict in atom_dict_list:
    print([atom_dict['name'], atom_dict['index'], atom_dict['x'], atom_dict['y'], atom_dict['z']])