"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/37730
"""

class Animal:
    age0 = 0  # 类的属性（变量）

    def __init__(self, name): # 如果子类定义了__init__方法，它将覆盖父类的__init__方法
        self.name = name
        print('父类的初始化实例！')

    def make_sound(self): # 方法（函数）
        print(f'Animal {self.name} is making sound.')  # 如果子类中有相同名字的方法，那么会覆盖它


class Dog(Animal):  # 继承Animal类
    def __init__(self, name, age):  # 在创建对象时初始化属性，其中，self也可以用其他名字，但默认用这个，表示内部的一个实例
        self.name = name  # 实例的属性（变量）
        self.age = age  # 实例的属性（变量）
        print('创建一个类的实例！')

    def bark(self): # 方法（函数）
        print(f"Dog {self.name} is barking.")


print(Animal.age0)  # 类的属性
print(Dog.age0)  # 类的属性
print()

an_animal = Animal('零号')   # 创建类的实例
print(an_animal.name) # 访问实例的属性
an_animal.make_sound() # 调用实例的方法
print()

my_dog = Dog(name="一号", age=3) # 创建类的实例
print(f"小狗的名字为：{my_dog.name}") # 访问实例的属性
print(f"小狗年龄为：{my_dog.age} 岁") # 访问实例的属性
my_dog.bark()  # 调用实例的方法
my_dog.make_sound()  # 调用实例的方法
my_dog.age = 4 # 更新属性值
print(f"小狗年龄修改为：{my_dog.age} 岁")
print()

another_dog = Dog(name="二号", age=1)  # 创建另一个实例
print(f"小狗的名字为：{another_dog.name}")  # 访问实例的属性
print(f"小狗年龄为：{another_dog.age} 岁")  # 访问实例的属性
another_dog.bark()  # 调用实例的方法
another_dog.make_sound()  # 调用实例的方法