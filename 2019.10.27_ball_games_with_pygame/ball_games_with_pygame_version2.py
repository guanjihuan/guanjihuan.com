"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/703
"""

import pygame
import random
import math
import sys

# 初始化pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# 游戏设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 1400
WORLD_HEIGHT = 1050
FPS = 60

# 创建窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("球球大作战")
clock = pygame.time.Clock()

# 字体 - 尝试加载系统中文字体
def get_font(size):
    # Windows系统字体路径 - 尝试更多常见字体
    windows_fonts = [
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/msyh.ttc",   # 微软雅黑
        "C:/Windows/Fonts/msyhbd.ttc", # 微软雅黑粗体
        "C:/Windows/Fonts/msyhl.ttc",  # 微软雅黑细体
        "C:/Windows/Fonts/simsun.ttc", # 宋体
        "C:/Windows/Fonts/simkai.ttf", # 楷体
        "C:/Windows/Fonts/arial.ttf",  # Arial
    ]
    # 只文件名尝试
    font_names = [
        "simhei.ttf",
        "msyh.ttc",
        "simsun.ttc",
        "arial.ttf",
    ]
    # 先试完整路径
    for font_path in windows_fonts:
        try:
            return pygame.font.Font(font_path, size)
        except:
            continue
    # 再试文件名
    for font_name in font_names:
        try:
            return pygame.font.Font(font_name, size)
        except:
            continue
    # 如果找不到中文字体，使用默认字体
    print("警告：未找到中文字体")
    return pygame.font.Font(None, size)

font = get_font(36)
small_font = get_font(24)


class Cell:
    """单个球体（细胞）类"""
    def __init__(self, x, y, radius, color, is_player=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.is_player = is_player
        self.mass = math.pi * radius * radius

    def update_mass(self):
        """根据质量更新半径"""
        self.radius = math.sqrt(self.mass / math.pi)

    def add_mass(self, mass):
        """增加质量"""
        self.mass += mass
        self.update_mass()

    def contains(self, other):
        """检查是否包含另一个球（可以吃掉它）
        覆盖约80%就能吃，不需要完全覆盖
        """
        dist = math.hypot(self.x - other.x, self.y - other.y)
        # 80%覆盖判定：dist + 0.8 * other.radius < self.radius
        return dist + 0.8 * other.radius < self.radius and self.mass > other.mass

    def draw(self, surface, camera_x, camera_y, zoom=1):
        """绘制球体
        camera_x, camera_y: 摄像头跟踪的世界坐标中心点
        zoom: 缩放系数，<1 表示缩小显示
        """
        # 计算屏幕坐标：以摄像头为中心缩放
        screen_x = int(SCREEN_WIDTH // 2 + (self.x - camera_x) * zoom)
        screen_y = int(SCREEN_HEIGHT // 2 + (self.y - camera_y) * zoom)
        # 缩放半径
        scaled_radius = int(self.radius * zoom)

        # 只有在屏幕可见范围内才绘制
        if (-scaled_radius < screen_x < SCREEN_WIDTH + scaled_radius and
            -scaled_radius < screen_y < SCREEN_HEIGHT + scaled_radius):
            pygame.draw.circle(surface, self.color, (screen_x, screen_y), scaled_radius)
            # 绘制边框
            pygame.draw.circle(surface, BLACK, (screen_x, screen_y), scaled_radius, 2)

            # 如果是玩家，显示分数
            if self.is_player:
                text = small_font.render(str(int(self.mass)), True, WHITE)
                text_rect = text.get_rect(center=(screen_x, screen_y))
                surface.blit(text, text_rect)


class Food:
    """食物类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 6
        self.mass = 25  # 增大食物的质量值
        self.color = random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, CYAN])

    def draw(self, surface, camera_x, camera_y, zoom=1):
        """绘制食物，支持缩放"""
        screen_x = int(SCREEN_WIDTH // 2 + (self.x - camera_x) * zoom)
        screen_y = int(SCREEN_HEIGHT // 2 + (self.y - camera_y) * zoom)
        scaled_radius = int(self.radius * zoom)
        if (-scaled_radius < screen_x < SCREEN_WIDTH + scaled_radius and
            -scaled_radius < screen_y < SCREEN_HEIGHT + scaled_radius):
            pygame.draw.circle(surface, self.color, (screen_x, screen_y), scaled_radius)


class Game:
    """游戏主类"""
    def __init__(self):
        self.player_cells = []
        self.ai_cells = []
        self.foods = []
        self.score = 0
        self.game_over = False
        self.paused = False
        self.final_mass = 0

        # 初始化玩家
        start_x = WORLD_WIDTH // 2
        start_y = WORLD_HEIGHT // 2
        player = Cell(start_x, start_y, 20, BLUE, is_player=True)
        self.player_cells.append(player)

        # 生成初始食物 - 更多更密
        self.generate_food(200)

        # 生成初始AI球球
        self.generate_ai(5)

    def generate_food(self, count):
        """生成食物"""
        for _ in range(count):
            x = random.randint(10, WORLD_WIDTH - 10)
            y = random.randint(10, WORLD_HEIGHT - 10)
            self.foods.append(Food(x, y))

    def generate_ai(self, count):
        """生成AI球球"""
        for _ in range(count):
            x = random.randint(50, WORLD_WIDTH - 50)
            y = random.randint(50, WORLD_HEIGHT - 50)
            radius = random.randint(15, 30)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            self.ai_cells.append(Cell(x, y, radius, color))

    def update_player(self, mouse_x, mouse_y):
        """更新玩家位置 - 所有玩家的球都跟随鼠标移动"""
        if not self.player_cells:
            return

        # 摄像头位置基于玩家重心（最大的球）
        main_player = self.get_main_player()
        if not main_player:
            return

        # 计算世界坐标中的目标位置
        camera_x = main_player.x - SCREEN_WIDTH // 2
        camera_y = main_player.y - SCREEN_HEIGHT // 2
        world_mouse_x = mouse_x + camera_x
        world_mouse_y = mouse_y + camera_y

        # 是否按住加速键
        mouse_buttons = pygame.mouse.get_pressed()
        boost_active = mouse_buttons[0]  # 左键加速

        # 更新所有玩家球
        for player in self.player_cells:
            # 向鼠标方向移动 - 整体加速，大球也不会太慢
            speed = 28000 / player.mass + 45  # 提高基础速度和整体速度

            # 如果按住鼠标左键，激活加速（4倍速），不消耗质量
            if boost_active:
                speed *= 4

            dx = world_mouse_x - player.x
            dy = world_mouse_y - player.y
            dist = math.hypot(dx, dy)

            if dist > 5:
                dx /= dist
                dy /= dist
                player.x += dx * speed / FPS
                player.y += dy * speed / FPS

            # 边界限制：允许球最多一半超出地图，这样能吃到角落的食物
            player.x = max(-player.radius/2, min(WORLD_WIDTH + player.radius/2, player.x))
            player.y = max(-player.radius/2, min(WORLD_HEIGHT + player.radius/2, player.y))

        # 自动合体：检查所有小球，如果接近主球就合体
        self.merge_cells()

    def merge_cells(self):
        """自动合体 - 分裂的球靠近时会合并回主球"""
        if len(self.player_cells) <= 1:
            return

        main_player = self.get_main_player()
        if not main_player:
            return

        # 检查其他小球
        to_merge = []
        for i, cell in enumerate(self.player_cells):
            if cell is main_player:
                continue

            # 计算距离
            dist = math.hypot(cell.x - main_player.x, cell.y - main_player.y)

            # 80%覆盖就能合体（和吞噬规则一致
            if dist + 0.8 * cell.radius < main_player.radius:
                to_merge.append(i)
                main_player.add_mass(cell.mass)

        # 移除合并的球（倒序删除避免索引问题）
        for i in reversed(to_merge):
            del self.player_cells[i]

    def update_ai(self):
        """更新AI移动"""
        for ai in self.ai_cells:
            # 简单AI：向附近较小的球移动，避开较大的球
            target = None
            closest_dist = float('inf')

            # 寻找最近的较小目标
            for food in self.foods:
                dist = math.hypot(ai.x - food.x, ai.y - food.y)
                if dist < closest_dist:
                    closest_dist = dist
                    target = (food.x, food.y)

            # 检查玩家
            for player in self.player_cells:
                dist = math.hypot(ai.x - player.x, ai.y - player.y)
                if ai.mass > player.mass * 1.2:
                    if dist < closest_dist:
                        closest_dist = dist
                        target = (player.x, player.y)
                elif player.mass > ai.mass * 1.2 and dist < 200:
                    # 逃离大球
                    dx = ai.x - player.x
                    dy = ai.y - player.y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        dx /= dist
                        dy /= dist
                        ai.x += dx * (5 / FPS) * 8
                        ai.y += dy * (5 / FPS) * 8
                    target = None

            # 向目标移动
            if target:
                speed = 18000 / ai.mass + 30  # 提高AI速度，加快游戏节奏
                dx = target[0] - ai.x
                dy = target[1] - ai.y
                dist = math.hypot(dx, dy)
                if dist > 5:
                    dx /= dist
                    dy /= dist
                    ai.x += dx * speed / FPS
                    ai.y += dy * speed / FPS

            # 边界限制：允许球最多一半超出地图
            ai.x = max(-ai.radius/2, min(WORLD_WIDTH + ai.radius/2, ai.x))
            ai.y = max(-ai.radius/2, min(WORLD_HEIGHT + ai.radius/2, ai.y))

    def check_collisions(self):
        """检查碰撞 - 吃东西和互相吞噬"""
        # 玩家吃食物
        for player in self.player_cells:
            to_remove = []
            for i, food in enumerate(self.foods):
                if player.contains(Cell(food.x, food.y, food.radius, None)):
                    player.add_mass(food.mass)
                    to_remove.append(i)
                    self.score += food.mass

            # 移除被吃的食物
            for i in reversed(to_remove):
                del self.foods[i]

            # AI吃食物
            for ai in self.ai_cells:
                to_remove = []
                for i, food in enumerate(self.foods):
                    if ai.contains(Cell(food.x, food.y, food.radius, None)):
                        ai.add_mass(food.mass)
                        to_remove.append(i)
                for i in reversed(to_remove):
                    del self.foods[i]

        # AI吞噬玩家
        for ai in self.ai_cells[:]:
            for player in self.player_cells[:]:
                if ai.contains(player):
                    ai.add_mass(player.mass)
                    # 在移除前保存最终质量
                    if len(self.player_cells) == 1:
                        self.final_mass = player.mass
                    self.player_cells.remove(player)
                elif player.contains(ai):
                    player.add_mass(ai.mass)
                    self.ai_cells.remove(ai)
                    self.score += ai.mass
                    break

        # AI之间互相吞噬
        for ai1 in self.ai_cells[:]:
            for ai2 in self.ai_cells[:]:
                if ai1 != ai2 and ai1.contains(ai2):
                    ai1.add_mass(ai2.mass)
                    self.ai_cells.remove(ai2)
                    break

        # 补充食物 - 更多更密
        if len(self.foods) < 300:
            self.generate_food(20)

        # 动态补充AI：玩家质量越高，生成越多对手
        main_player = self.get_main_player()
        if main_player:
            # 限制最多35个AI，平衡挑战性和流畅性，减少卡顿
            target_ai_count = min(35, 15 + int(main_player.mass / 150))
        else:
            target_ai_count = 12

        # 如果AI数量少于目标，持续补充
        if len(self.ai_cells) < target_ai_count:
            self.generate_ai(1)

        # 质量衰减：所有球按比例减小体积，越大减少越多
        self.mass_decay()

    def get_main_player(self):
        """获取玩家最大的球"""
        if not self.player_cells:
            return None
        return max(self.player_cells, key=lambda c: c.mass)

    def draw(self):
        """绘制游戏，支持自动缩放"""
        # 背景
        screen.fill((240, 240, 240))

        # 获取主玩家
        main_player = self.get_main_player()
        if main_player:
            # 摄像头始终跟随主玩家中心点
            camera_x = main_player.x
            camera_y = main_player.y

            # 自动缩放计算：主球显示直径最大固定为屏幕宽度的一半
            # 达到后，主球显示大小不再增大，实际质量继续增长，其他球跟着缩小
            max_display_radius = SCREEN_WIDTH / 4  # 半径 = 1/4宽度 → 直径 = 1/2宽度，正好是屏幕一半
            if main_player.radius > max_display_radius:
                # 需要缩小整个画面，保持主球显示大小不超
                zoom = max_display_radius / main_player.radius
            else:
                # 还没到最大，正常显示
                zoom = 1.0

            # 最小缩放到0.15，避免缩得太小
            zoom = max(0.15, zoom)
        else:
            camera_x = WORLD_WIDTH // 2
            camera_y = WORLD_HEIGHT // 2
            zoom = 1.0

        # 绘制网格背景（网格也随缩放调整）
        grid_size = int(40 * zoom)
        if grid_size < 5:
            grid_size = 5
        # 计算网格起始位置
        # 因为现在 camera 在中心，所以起始点计算方式改变
        start_x = int((-camera_x * zoom) % grid_size)
        start_y = int((-camera_y * zoom) % grid_size)
        start_x += SCREEN_WIDTH // 2
        start_y += SCREEN_HEIGHT // 2
        for x in range(start_x - grid_size, SCREEN_WIDTH, grid_size):
            pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(start_y - grid_size, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(screen, (220, 220, 220), (0, y), (SCREEN_WIDTH, y), 1)

        # 绘制食物（所有物体都按zoom缩放）
        for food in self.foods:
            food.draw(screen, camera_x, camera_y, zoom)

        # 绘制AI
        for ai in self.ai_cells:
            ai.draw(screen, camera_x, camera_y, zoom)

        # 绘制玩家
        for player in self.player_cells:
            player.draw(screen, camera_x, camera_y, zoom)

        # 绘制UI（UI不缩放，始终固定在屏幕）
        if main_player:
            mass_text = font.render(f"质量: {int(main_player.mass)}", True, BLACK)
            screen.blit(mass_text, (10, 10))

        # 分数显示已禁用
        # score_text = font.render(f"分数: {self.score}", True, BLACK)
        # screen.blit(score_text, (10, 50))

        # 游戏结束
        if not self.player_cells and not self.game_over:
            self.game_over = True
            # 已经在AI吃掉最后一个球时保存了final_mass，如果还有其他球在这里补充
            if self.final_mass == 0:
                self.final_mass = sum(p.mass for p in self.player_cells)

        if self.game_over:
            game_over_text = font.render(f"游戏结束! 最终质量: {int(self.final_mass)}", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)

            restart_text = small_font.render("按R重新开始", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            screen.blit(restart_text, restart_rect)

        if self.paused:
            pause_text = font.render("暂停", True, RED)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(pause_text, text_rect)

        # 操作提示 - 分成两行显示避免超出屏幕，使用普通字符
        hint_text1 = small_font.render(f"鼠标: 移动  左键: 加速(不耗质量)  空格: 分裂({len(self.player_cells)}/16)", True, BLACK)
        hint_text2 = small_font.render("R: 重来  P: 暂停  完全靠近: 合体  大球衰减更多", True, BLACK)
        screen.blit(hint_text1, (10, SCREEN_HEIGHT - 50))
        screen.blit(hint_text2, (10, SCREEN_HEIGHT - 25))

    def split_player(self, mouse_x, mouse_y):
        """玩家分裂 - 最多16个分身"""
        main_player = self.get_main_player()
        if not main_player or main_player.mass < 36:  # 最小分裂质量
            return

        # 限制最多16个分身（4次分裂：1→2→4→8→16）
        if len(self.player_cells) >= 16:
            return

        camera_x = main_player.x - SCREEN_WIDTH // 2
        camera_y = main_player.y - SCREEN_HEIGHT // 2
        world_mouse_x = mouse_x + camera_x
        world_mouse_y = mouse_y + camera_y

        # 计算方向
        dx = world_mouse_x - main_player.x
        dy = world_mouse_y - main_player.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 0.1
            dx = 1
            dy = 0

        dx /= dist
        dy /= dist

        # 创建新球
        new_mass = main_player.mass / 2
        main_player.mass = new_mass
        main_player.update_mass()

        new_x = main_player.x + dx * (main_player.radius + 5)
        new_y = main_player.y + dy * (main_player.radius + 5)

        new_cell = Cell(new_x, new_y, 0, BLUE, is_player=True)
        new_cell.mass = new_mass
        new_cell.update_mass()
        self.player_cells.append(new_cell)

        # 给新细胞一个推力
        new_cell.x += dx * 10
        new_cell.y += dy * 10

    def mass_decay(self):
        """质量衰减：所有球按比例减小体积，越大减少越多，设置最小质量保证不会太小没法吃食物"""
        # 最小质量下限，不会比这个更小
        MIN_MASS = 20
        # 衰减系数，每帧衰减当前质量的比例
        # 纯比例衰减：质量越大衰减越多，小球衰减很少几乎不衰减，符合要求
        decay_rate = 0.0001

        # 玩家球衰减
        for i, player in reversed(list(enumerate(self.player_cells))):
            decay_amount = player.mass * decay_rate
            player.mass -= decay_amount
            # 限制最小质量
            if player.mass < MIN_MASS:
                player.mass = MIN_MASS
            player.update_mass()

        # AI球衰减
        for i, ai in reversed(list(enumerate(self.ai_cells))):
            decay_amount = ai.mass * decay_rate
            ai.mass -= decay_amount
            if ai.mass < MIN_MASS:
                ai.mass = MIN_MASS
            ai.update_mass()

    def restart(self):
        """重新开始游戏"""
        self.player_cells = []
        self.ai_cells = []
        self.foods = []
        self.score = 0
        self.game_over = False
        self.paused = False

        # 初始化玩家
        start_x = WORLD_WIDTH // 2
        start_y = WORLD_HEIGHT // 2
        player = Cell(start_x, start_y, 20, BLUE, is_player=True)
        self.player_cells.append(player)

        # 生成初始食物 - 更多更密
        self.generate_food(200)

        # 生成初始AI球球
        self.generate_ai(5)


def main():
    """主游戏循环"""
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game.game_over and not game.paused:
                    # 左键加速已经在update处理
                    pass
            if event.type == pygame.KEYDOWN:
                # 获取字符，转小写（兼容输入法）
                char = event.unicode.lower() if event.unicode else ''

                # 处理扫描码掩码：某些键盘/SDL会加上0x40000000掩码
                SCANCODE_MASK = 1 << 30  # 1073741824
                key = event.key
                if key & SCANCODE_MASK:
                    key = key & ~SCANCODE_MASK

                # 空格键分裂
                if key == pygame.K_SPACE and not game.game_over and not game.paused:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    game.split_player(mouse_x, mouse_y)

                # R键重启：兼容不同键盘、输入法、大小写
                if (key == pygame.K_r
                    or key == 114
                    or char == 'r'
                    or char == 'R'):
                    game = Game()

                # P键暂停：兼容不同键盘、输入法、大小写
                if (key == pygame.K_p
                    or key == 112
                    or char == 'p'
                    or char == 'P'):
                    game.paused = not game.paused

        if not game.game_over and not game.paused:
            # 获取鼠标位置
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 更新游戏
            game.update_player(mouse_x, mouse_y)
            game.update_ai()
            game.check_collisions()

        # 绘制
        game.draw()

        # 更新显示
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
