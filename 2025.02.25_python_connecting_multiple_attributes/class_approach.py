"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/45135
"""

class Atom:
    def __init__(self, name='atom', index=0, x=0, y=0, z=0):
        self.name = name
        self.index = index
        self.x = x
        self.y = y
        self.z = z

atom_object_list = []
index = 0
for i0 in range(3):
    for j0 in range(3):
        atom = Atom(index=index, x=i0, y=j0)
        atom_object_list.append(atom)
        index += 1

print(atom_object_list)
for atom_object in atom_object_list:
    print([atom_object.name, atom_object.index, atom_object.x, atom_object.y, atom_object.z])