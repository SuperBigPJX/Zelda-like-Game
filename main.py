import pygame
import random
import os

# 游戏窗口尺寸
WIDTH = 800
HEIGHT = 600

# 迷宫参数
CELL_SIZE = 40
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 角色相关参数
player_size = CELL_SIZE
player_pos = [0, 0]

# 当前路径
current_path = os.path.dirname(__file__)
images_path = os.path.join(current_path, 'images')

# draw character
player_img = pygame.image.load("link.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))

# 宝藏相关参数
treasure_size = CELL_SIZE
treasure_pos = [COLS - 1, ROWS - 1]

# draw box
treasure_img = pygame.image.load("box.png")
treasure_img = pygame.transform.scale(treasure_img, (treasure_size, treasure_size))

# 怪物相关参数
monster_size = CELL_SIZE
monster_pos = []  # 存储怪物的位置列表
k = 0.5  # 控制怪物数量增加的系数

# draw monster
monster_img = pygame.image.load("monster.png")
monster_img = pygame.transform.scale(monster_img, (monster_size, monster_size))


def draw_ui(screen, health):
    # 绘制血量条背景
    pygame.draw.rect(screen, BLACK, (20, 20, 200, 30))

    # 计算血量条长度
    health_width = health * 2

    # 绘制血量条
    pygame.draw.rect(screen, RED, (20, 20, health_width, 30))


# 迷宫生成函数
def generate_maze():
    global monster_pos  # 声明为全局变量
    while True:
        # 初始化迷宫
        maze = [[0] * COLS for _ in range(ROWS)]

        # 随机选择一个起始点
        start_row = random.randint(1, ROWS - 1)
        start_col = random.randint(1, COLS - 1)
        stack = [(start_row, start_col)]
        monster_pos = []

        while stack:
            current_row, current_col = stack.pop()
            maze[current_row][current_col] = 1

            # 获取当前位置的邻居
            neighbors = [
                (current_row - 2, current_col),  # 上方
                (current_row, current_col + 2),  # 右方
                (current_row + 2, current_col),  # 下方
                (current_row, current_col - 2)  # 左方
            ]

            random.shuffle(neighbors)

            for neighbor_row, neighbor_col in neighbors:
                if (0 <= neighbor_row < ROWS) and (0 <= neighbor_col < COLS) and (
                        maze[neighbor_row][neighbor_col] == 0):
                    # 将当前位置与邻居之间的墙打通
                    maze[neighbor_row][neighbor_col] = 1
                    maze[current_row + (neighbor_row - current_row) // 2][
                        current_col + (neighbor_col - current_col) // 2] = 1
                    stack.append((neighbor_row, neighbor_col))

        if maze[1][0] == 1 and maze[0][1] == 1:
            break  # 迷宫满足条件，跳出循环

    # 在路径上随机生成怪物位置
    for row in range(1, ROWS - 1):
        for col in range(1, COLS - 1):
            if maze[row][col] == 1:
                if random.random() < 0.1:  # 10%的概率生成怪物
                    monster_pos.append([col, row])

    return maze


def show_main_menu(screen):
    background_img = pygame.image.load("background.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    font = pygame.font.Font(None, 48)
    title_text = font.render("Zelda-like Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))

    start_text = font.render("Press any key to start", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def show_main_menu(screen):
    background_img = pygame.image.load("background.png")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    font = pygame.font.Font(None, 48)
    title_text = font.render("This is a tribute", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))

    start_text = font.render("Press any key to start", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def play_game():
    global player_pos  # 声明为全局变量
    global player_img

    # 初始化Pygame
    pygame.init()

    # 创建游戏窗口
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zelda-like Game")

    show_main_menu(screen)
    # 生成迷宫
    maze = generate_maze()

    # 游戏关卡计数器
    level = 1

    # 得分数，通过一关得一分
    passed_levels = 1

    # 游戏循环之前定义计时器变量
    monster_timer = 0
    monster_interval = 1/passed_levels * 10000 # 怪物移动的时间间隔，单位为毫秒

    # 游戏开始前设置人物血量
    player_health = 100  # 初始血量为100

    # 游戏循环
    game_over = False
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                x = player_pos[0]
                y = player_pos[1]
                if event.key == pygame.K_LEFT:
                    if x > 0 and maze[y][x - 1] == 1:
                        x -= 1
                elif event.key == pygame.K_RIGHT:
                    if x < COLS - 1 and maze[y][x + 1] == 1:
                        x += 1
                elif event.key == pygame.K_UP:
                    if y > 0 and maze[y - 1][x] == 1:
                        y -= 1
                elif event.key == pygame.K_DOWN:
                    if y < ROWS - 1 and maze[y + 1][x] == 1:
                        y += 1

                elif event.key == pygame.K_SPACE:  # 玩家按下SPACE键
                    for monster in monster_pos:
                        if abs(x - monster[0]) + abs(y - monster[1]) <= 1:
                            monster_pos.remove(monster)  # 怪物消失

                player_pos = [x, y]

        screen.fill(BLACK)

        wall_image = pygame.image.load(os.path.join(images_path, f"stone{level}.png")).convert_alpha()
        road_image = pygame.image.load(os.path.join(images_path, f"road{level}.png")).convert_alpha()

        for row in range(ROWS):
            for col in range(COLS):
                if maze[row][col] == 0:
                    screen.blit(wall_image, (col * CELL_SIZE, row * CELL_SIZE))
                elif maze[row][col] == 1:
                    screen.blit(road_image, (col * CELL_SIZE, row * CELL_SIZE))

        screen.blit(player_img, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE))
        screen.blit(treasure_img, (treasure_pos[0] * CELL_SIZE, treasure_pos[1] * CELL_SIZE))

        # 绘制怪物
        for monster in monster_pos:
            screen.blit(monster_img, (monster[0] * CELL_SIZE, monster[1] * CELL_SIZE))
            # 更新计时器
            monster_timer += clock.get_time()

            # 当计时器达到时间间隔时，移动怪物
            if monster_timer >= monster_interval:
                for monster in monster_pos:
                    # 生成随机移动方向
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])

                    # 更新怪物的位置
                    monster[0] += dx
                    monster[1] += dy

                    # 确保怪物的位置在迷宫范围内
                    monster[0] = max(0, min(monster[0], COLS - 1))
                    monster[1] = max(0, min(monster[1], ROWS - 1))

                # 重置计时器
                monster_timer = 0

        # 碰撞检测的部分
        for monster in monster_pos:
            if abs(player_pos[0] - monster[0]) + abs(player_pos[1] - monster[1]) <= 0:
                player_health -= 1  # 减少人物血量
                print(player_health)
                if player_health < 0:
                    print("Game over!")
                    game_over = True
                    break  # 退出游戏循环

        # 绘制UI
        draw_ui(screen, player_health)

        # 绘制通过的关卡数
        font = pygame.font.Font(None, 36)
        text = font.render("Passed Levels: " + str(passed_levels), True, WHITE)
        screen.blit(text, (20, 60))

        # 计算玩家与宝箱的距离
        distance = abs(player_pos[0] - treasure_pos[0]) + abs(player_pos[1] - treasure_pos[1])
        if distance <= 2:
            print("You win!")
            passed_levels += 1  # 增加通过的关卡数
            level += 1
            if level > 4:
                level = 1
            player_pos = [0, 0]
            maze = generate_maze()  # 重新生成迷宫

        pygame.display.update()
        clock.tick(30)

    pygame.quit()


# 开始游戏
if __name__ == "__main__":
    play_game()
