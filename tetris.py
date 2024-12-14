import pygame
import random

# 初始化
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

# 游戏设置
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

# 方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        
    def new_piece(self):
        # 随机选择一个方块
        shape = random.choice(SHAPES)
        # 方块初始位置
        return {
            'shape': shape,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }
    
    def valid_move(self, piece, x, y):
        for i in range(len(piece['shape'])):
            for j in range(len(piece['shape'][0])):
                if piece['shape'][i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True
    
    def merge_piece(self):
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][i][j]:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = 1
    
    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared * 100
    
    def move(self, dx, dy):
        new_x = self.current_piece['x'] + dx
        new_y = self.current_piece['y'] + dy
        if self.valid_move(self.current_piece, new_x, new_y):
            self.current_piece['x'] = new_x
            self.current_piece['y'] = new_y
            return True
        return False
    
    def rotate(self):
        # 旋转方块
        shape = self.current_piece['shape']
        new_shape = [[shape[j][i] for j in range(len(shape)-1, -1, -1)]
                    for i in range(len(shape[0]))]
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = new_shape
        if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
            self.current_piece['shape'] = old_shape

def draw_game(screen, game):
    screen.fill(BLACK)
    
    # 绘制网格
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if game.grid[i][j]:
                pygame.draw.rect(screen, WHITE,
                               (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE-1, BLOCK_SIZE-1))
    
    # 绘制当前方块
    for i in range(len(game.current_piece['shape'])):
        for j in range(len(game.current_piece['shape'][0])):
            if game.current_piece['shape'][i][j]:
                pygame.draw.rect(screen, CYAN,
                               ((game.current_piece['x'] + j) * BLOCK_SIZE,
                                (game.current_piece['y'] + i) * BLOCK_SIZE,
                                BLOCK_SIZE-1, BLOCK_SIZE-1))
    
    # 显示分数
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {game.score}', True, WHITE)
    screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))
    
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0
    fall_speed = 500  # 下落速度（毫秒）
    
    while not game.game_over:
        fall_time += clock.get_rawtime()
        clock.tick()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    while game.move(0, 1):
                        pass
        
        # 自动下落
        if fall_time >= fall_speed:
            if not game.move(0, 1):
                game.merge_piece()
                game.clear_lines()
                game.current_piece = game.new_piece()
                if not game.valid_move(game.current_piece, game.current_piece['x'], game.current_piece['y']):
                    game.game_over = True
            fall_time = 0
        
        draw_game(screen, game)

    # 游戏结束
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('Game Over!', True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH//3, SCREEN_HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)

if __name__ == '__main__':
    main()
    pygame.quit()