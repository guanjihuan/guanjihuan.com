"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/703
"""

import pygame
import random
import math
import numpy as np

# 参数
screen_width = 1500  # 屏幕宽度
screen_height = 900  # 屏幕高度
map_width = screen_width*4  # 地图的大小
map_height = screen_height*4  # 地图的大小
number_enemy = map_width*map_height/500000  # 敌人的数量
number_dots = map_width * map_height / 50  # 点点的数量
max_show_size = 100  # 球显示的最大半径（屏幕有限，球再增大时，改变的地图比例尺寸）

my_value = 1000  # 我的初始值
enemy_value_low = 500  # 敌人的初始值（最低）
enemy_value_high = 1500  # 敌人的初始值（最高）
dot_value = 30  # 点点的值（地上的豆豆/食物值）
my_speed = 10  # 我的球运动的速度
speed_up = 20  # 按下鼠标时加速
speed_enemy = 10  # 敌人球正常运动速度
speed_enemy_anomaly = 20  # 敌人突然加速时的速度（速度异常时的速度）
anomaly_pro = 0.5  # 敌人加速的概率
change_pro = 0.05  # 敌人移动路径变化的概率，也就是1/change_pro左右会变化一次
eat_percent = 0.9  # 吃掉敌人的球，按多少比例并入自己的体积，1对应的是100%
loss = 0.001  # 按比例减小体重（此外越重的减少越多，10万体积损失值为loss的一倍）
enemy_bigger_pro = 0.0005  # 敌人的值增加了我的球的值的enemy_bigger_rate倍的几率
enemy_bigger_rate = 0.1  # 增加我的球的体积的enemy_bigger_rate倍


class Color(object):  # 定义颜色的类
    @classmethod  # 加了这个可以不需要把实例化，能直接调用类的方法
    def random_color(cls):  # cls, 即class，表示可以通过类名直接调用
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return red, green, blue


class Ball(object):  # 定义球
    def __init__(self, x, y, sx, sy, color, value):  # 初始化
        self.x = x  # 球的地图位置参数
        self.y = y
        self.sx = sx  # 速度参数
        self.sy = sy
        self.color = color  # 颜色
        self.value = value  # 球的值，也就是球的大小（不是显示的大小）
        self.is_alive = True  # 球默认是存活状态


class My_Ball(Ball):  # 定义我的球，继承了Ball类的方法
    def __init__(self, x, y, sx, sy, color, value):
        # 注意：如果重写了__init__() 时，实例化子类，就不会调用父类已经定义的__init__()
        # 如果子类不重写__init__()方法，实例化子类后，会自动调用父类的__init__()的方法
        # 如果子类重写__init__()方法又需要调用父类的方法，则要使用super关键词。
        super().__init__(x, y, sx, sy, color, value)  # 调用父类Ball的初始化方法__init__()
        self.radius = int(self.value**0.5)  # 我的球的半径（不考虑系数pi）
        if self.radius >= max_show_size:  # 如果半径比规定的最大半径还大，则显示最大半径
            self.show_radius = max_show_size  # 我的球显示的半径
        else:
            self.show_radius = self.radius  # 如果半径没有超过规定最大的半径，则显示原来实际大小的半径
        self.position_x = int(screen_width/2)   # 把我的球固定在屏幕中间position_x，是屏幕显示的位置
        self.position_y = int(screen_height/2)  # 把我的球固定在屏幕中间position_y，是屏幕显示的位置

    def draw(self, window):  # 把我的球画出来
        self.radius = int(self.value ** 0.5)   # 这里重复上面的，因为除了初始化之后，还要更新
        if self.radius >= max_show_size:
            self.show_radius = max_show_size
        else:
            self.show_radius = self.radius
        self.position_x = int(screen_width / 2)
        self.position_y = int(screen_height / 2)
        pygame.draw.circle(window, self.color, (self.position_x , self.position_y), self.show_radius)

    def eat_ball(self, other):  # 吃别的球（包括小点点和敌人）
        if self != other and self.is_alive and other.is_alive:  # 如果other不是自身，自身和对方也都是存活状态，则执行下面动作
            distance = ((self.position_x - other.position_x) ** 2 + (self.position_y - other.position_y) ** 2) ** 0.5   # 两个球之间的距离
            if distance < self.show_radius and (self.show_radius > other.show_radius or (self.show_radius == other.show_radius and self.value > other.value)):  # 如果自身半径比别人大，而且两者距离小于自身半径，那么可以吃掉。
                other.is_alive = False  # 吃球（敌方已死）
                self.value += other.value*eat_percent   # 自己的值增大（体量增大）
                self.radius = int(self.value ** 0.5)  # 计算出半径
                if self.radius >= max_show_size:  # 我的球的显示半径
                    self.show_radius = max_show_size
                else:
                    self.show_radius = self.radius

    def move(self):  # 移动规则
        self.x += self.sx  # 地图位置加上速度
        self.y += self.sy
        # 横向出界
        if self.x < 0:  # 离开了地图左边
            self.x = 0
        if self.x > map_width:  # 离开了地图右边
            self.x = map_width
        # 纵向出界
        if self.y <= 0:  # 离开了地图下边
            self.y = 0
        if self.y >= map_height:  # 离开了地图上边
            self.y = map_height


class Enemy_Ball(Ball):  # 定义敌人的球，继承了Ball类的方法
    def __init__(self, x, y, sx, sy, color, value, host_ball):  # 初始化带上host_ball，也就是我的球
        super().__init__(x, y, sx, sy, color, value)
        self.host_ball = host_ball
        self.radius = int(self.value**0.5)
        if self.host_ball.radius >= max_show_size:  # 如果我的球比规定的最大尺寸还大，则敌人的球显示的比例要减小
            self.show_radius = max(10, int(self.radius/(self.host_ball.radius/max_show_size)))  # 敌人的球也不能太小，最小半径为10
            self.position_x = int((self.x - self.host_ball.x) / (self.host_ball.radius / max_show_size)) + int(
                screen_width / 2)  # 计算出敌人的球和我的球的相对位置，并且按比例减小
            self.position_y = int((self.y - self.host_ball.y) / (self.host_ball.radius / max_show_size)) + int(
                screen_height / 2)  # 计算出敌人的球和我的球的相对位置，并且按比例减小
        else:
            self.show_radius = self.radius  # 正常显示
            self.position_x = (self.x - self.host_ball.x) + int(screen_width / 2)  # 敌人和我的球的相对位置
            self.position_y = (self.y - self.host_ball.y) + int(screen_height / 2)  # 敌人和我的球的相对位置

    # 画出球
    def draw(self, window):
        self.radius = int(self.value ** 0.5)
        if self.host_ball.radius >= max_show_size:  # 这边把初始化的内容再写一遍，因为敌人的球初始化之后还要根据我的球而动态改变
            self.show_radius = max(10, int(self.radius/(self.host_ball.radius/max_show_size)))
            self.position_x = int((self.x - self.host_ball.x) / (self.host_ball.radius / max_show_size)) + int(
                screen_width / 2)
            self.position_y = int((self.y - self.host_ball.y) / (self.host_ball.radius / max_show_size)) + int(
                screen_height / 2)
        else:
            self.show_radius = self.radius
            self.position_x = (self.x - self.host_ball.x) + int(screen_width / 2)
            self.position_y = (self.y - self.host_ball.y) + int(screen_height / 2)
        pygame.draw.circle(window, self.color, (self.position_x, self.position_y), self.show_radius)

    def eat_ball(self, other):
        if self != other and self.is_alive and other.is_alive:
            distance = ((self.position_x - other.position_x) ** 2 + (self.position_y - other.position_y) ** 2) ** 0.5
            if distance < self.show_radius and (self.show_radius > other.show_radius or (self.show_radius == other.show_radius and self.value > other.value)):
                other.is_alive = False  # 吃球
                self.value += other.value*eat_percent
                self.radius = int(self.value ** 0.5)

    def move(self):  # 移动规则
        self.x += self.sx  # 地图位置加上速度
        self.y += self.sy
        # 横向出界
        if self.x < 0:  # 离开了地图左边
            self.sx = -self.sx
            self.x = 0
        if self.x > map_width:  # 离开了地图右边
            self.sx = -self.sx
            self.x = map_width
        # 纵向出界
        if self.y <= 0:  # 离开了地图下边
            self.sy = -self.sy
            self.y = 0
        if self.y >= map_height:  # 离开了地图上边
            self.sy = -self.sy
            self.y = map_height


class Dot_Ball(Ball):  # 定义地上的小点点，供自己的球和敌人的球吃，继承了Ball类的方法
    def __init__(self, x, y,  sx, sy, color, value, host_ball):
        super().__init__(x, y, sx, sy, color, value)
        self.host_ball = host_ball
        self.radius = 8  # 初始小点点大小
        if self.host_ball.radius >= max_show_size:
            self.show_radius = max(3, int(self.radius/(self.host_ball.radius/max_show_size)))  # 小点点显示也不能太小，最小显示半径为3
            self.position_x = int((self.x - self.host_ball.x) / (self.host_ball.radius / max_show_size)) + int(
                screen_width / 2)
            self.position_y = int((self.y - self.host_ball.y) / (self.host_ball.radius / max_show_size)) + int(
                screen_height / 2)
        else:
            self.show_radius = self.radius
            self.position_x = (self.x - self.host_ball.x) + int(screen_width / 2)
            self.position_y = (self.y - self.host_ball.y) + int(screen_height / 2)

    # 画出球
    def draw(self, window):
        if self.host_ball.radius >= max_show_size:  # 这边把初始化的内容再写一遍，因为小点点初始化之后还要根据我的球而动态改变
            self.show_radius = max(3, int(self.radius/(self.host_ball.radius/max_show_size)))
            self.position_x = int((self.x - self.host_ball.x) / (self.host_ball.radius / max_show_size)) + int(
                screen_width / 2)
            self.position_y = int((self.y - self.host_ball.y) / (self.host_ball.radius / max_show_size)) + int(
                screen_height / 2)
        else:
            self.show_radius = self.radius
            self.position_x = (self.x - self.host_ball.x) + int(screen_width / 2)
            self.position_y = (self.y - self.host_ball.y) + int(screen_height / 2)
        pygame.draw.circle(window, self.color, (self.position_x, self.position_y) , self.show_radius)


def creat_my_ball():  # 产生我的球
    x = random.randint(0, map_width)  # 我的球在地图中的位置，随机生成
    y = random.randint(0, map_height)
    value = my_value  # 我的球的初始值
    color = 255, 255, 255  # 我的球的颜色
    sx = 0  # 速度默认为0
    sy = 0
    host_ball = My_Ball(x, y, sx, sy, color, value)  # 调用My_Ball类
    return host_ball  # 返回我的球


def auto_creat_ball(balls, host_ball):  # 自动产生敌人的球
    if len(balls) <= number_enemy:  # 控制敌人的数量，如果个数够了，就不再生成
        x = random.randint(0, map_width)  # 敌人球在地图中的位置，随机生成
        y = random.randint(0, map_height)
        value = random.randint(enemy_value_low, enemy_value_high)  # 敌人的球初始值
        sx = random.randint(-speed_enemy, speed_enemy)  # 敌人的球移动速度
        i2 = random.randint(0, 1)  # y的移动方向
        if i2 == 0:
            sy = int((speed_enemy**2 - sx**2) ** 0.5)
        else:
            sy = -int((speed_enemy ** 2 - sx ** 2) ** 0.5)
        color = Color.random_color()  # 敌人的颜色随机生成
        enemy = Enemy_Ball(x, y, sx, sy, color, value, host_ball)
        balls.append(enemy)


def auto_creat_dots(dots, host_ball):  # 自动生成点点
    if len(dots) <= number_dots:  # 控制点点的数量
        x = random.randint(0, map_width)  # 随机生成点点的位置
        y = random.randint(0, map_height)
        value = dot_value  # 点点的值
        sx = 0  # 点点速度为0
        sy = 0
        color = Color.random_color()  # 颜色
        dot = Dot_Ball(x, y, sx, sy, color, value, host_ball)
        dots.append(dot)


def control_my_ball(host_ball):  # 控制我的球
    host_ball.move()
    host_ball.value = host_ball.value*(1-loss*host_ball.value/100000)
    for event in pygame.event.get():  # 监控事件（鼠标移动）
        # print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            speed = speed_up
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            if event.buttons[0] == 1:
                speed = speed_up
            if event.buttons[0] == 0:
                speed = my_speed
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            speed = my_speed
        else:
            pos = [screen_width/2, screen_height/2]
            speed = my_speed
        if abs(pos[0] - screen_width/2) < 30 and abs(pos[1] - screen_height/2) < 30:
            host_ball.sx = 0
            host_ball.sy = 0
        elif pos[0] > screen_width/2 and pos[1] >= screen_height/2:
            angle = abs(math.atan((pos[1] - screen_height/2) / (pos[0] - screen_width/2)))
            host_ball.sx = int(speed * math.cos(angle))
            host_ball.sy = int(speed * math.sin(angle))
        elif pos[0] > screen_width/2 and pos[1] < screen_height/2:
            angle = abs(math.atan((pos[1] - screen_height/2) / (pos[0] - screen_width/2)))
            host_ball.sx = int(speed * math.cos(angle))
            host_ball.sy = -int(speed * math.sin(angle))
        elif pos[0] < screen_width/2 and pos[1] >= screen_height/2:
            angle = abs(math.atan((pos[1] - screen_height/2) / (pos[0] - screen_width/2)))
            host_ball.sx = -int(speed * math.cos(angle))
            host_ball.sy = int(speed * math.sin(angle))
        elif pos[0] < screen_width/2 and pos[1] < screen_height/2:
            angle = abs(math.atan((pos[1] - screen_height/2) / (pos[0] - screen_width/2)))
            host_ball.sx = -int(speed * math.cos(angle))
            host_ball.sy = -int(speed * math.sin(angle))
        elif pos[0] == screen_width/2:
            host_ball.sx = 0
            if pos[1] >= 0:
                host_ball.sy = speed
            else:
                host.ball.sy = -speed


def enemy_move(balls, host_ball):  # 敌人移动
    for enemy in balls:
        enemy.move()  # 移动
        enemy.value = enemy.value*(1-loss*enemy.value/100000)
        if random.randint(1, int(1/enemy_bigger_pro)) == 1:
            enemy.value += host_ball.value*enemy_bigger_rate
        if random.randint(1, int(1/anomaly_pro)) == 1:
            speed_enemy0 = speed_enemy_anomaly  # 敌人异常速度
        else:
            speed_enemy0 = speed_enemy  # 敌人正常速度
        i = random.randint(1, int(1/change_pro))  # 一定的概率改变轨迹
        if i == 1:
            enemy.sx = random.randint(-speed_enemy0, speed_enemy0)
            i2 = random.randint(0, 1)
            if i2 == 0:
                enemy.sy = int((speed_enemy0 ** 2 - enemy.sx ** 2) ** 0.5)
            else:
                enemy.sy = -int((speed_enemy0 ** 2 - enemy.sx ** 2) ** 0.5)


def eat_each_other(host_ball, balls, dots):  # 吃球
    for enemy in balls:
        for enemy2 in balls:
            enemy.eat_ball(enemy2)  # 敌人互吃
        for food in dots:
            enemy.eat_ball(food)  # 敌人吃点点
    for enemy in balls:
        host_ball.eat_ball(enemy)  # 我吃敌人
        enemy.eat_ball(host_ball)  # 敌人吃我
    for food in dots:
        host_ball.eat_ball(food)  # 我吃点点


def paint(host_ball, balls, dots, screen):
    screen.fill((0, 0, 0))  # 刷漆
    if host_ball.is_alive:
        host_ball.draw(screen)
    for enemy in balls:  # 遍历容器
        if enemy.is_alive:
            enemy.draw(screen)
        else:
            balls.remove(enemy)
    for food in dots:  # 遍历容器
        if food.is_alive:
            food.draw(screen)
        else:
            dots.remove(food)


def main():
    pygame.init()  # 初始化
    screen = pygame.display.set_mode((screen_width, screen_height))  # 设置屏幕
    pygame.display.set_caption("球球大作战")  # 设置屏幕标题
    balls = []  # 定义一容器  存放所有的敌方球
    dots = []  # 定义一容器 存放所有的点点
    is_running = True  # 默认运行状态
    host_ball = creat_my_ball()  # 产生我的球
    i00 = 0  # 一个参数
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        auto_creat_dots(dots, host_ball)  # 自动生成点点
        auto_creat_ball(balls, host_ball)  # 自动生成敌人
        paint(host_ball, balls, dots, screen)  # 把所有的都画出来 调用draw方法
        pygame.display.flip()  # 渲染
        pygame.time.delay(30)  # 设置动画的时间延迟

        control_my_ball(host_ball)  # 移动我的球
        enemy_move(balls, host_ball)  # 敌人的球随机运动
        eat_each_other(host_ball, balls, dots)  # 吃球 调用eat_ball方法
        i00 += 1
        if np.mod(i00, 50) == 0:
            print(host_ball.value)


if __name__ == '__main__':
    main()
