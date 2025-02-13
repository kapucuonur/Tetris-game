import pygame
import random

# Ses modülünü devre dışı bırak
pygame.mixer.quit()

# Pygame initialize
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

COLORS = [CYAN, YELLOW, ORANGE, BLUE, GREEN, PURPLE, RED]

# Tetromino shapes and colors
TETROMINOS = [
    ([[1, 1, 1, 1]], CYAN),  # I
    ([[1, 1], [1, 1]], YELLOW),  # O
    ([[0, 1, 0], [1, 1, 1]], PURPLE),  # T
    ([[1, 1, 0], [0, 1, 1]], GREEN),  # Z
    ([[0, 1, 1], [1, 1, 0]], RED),  # S
    ([[1, 1, 1], [0, 0, 1]], ORANGE),  # L
    ([[1, 1, 1], [1, 0, 0]], BLUE)  # J
]

# Game grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Draw a single block
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Draw the entire grid
def draw_grid():
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                draw_block(x, y, val)

# Check if a position is valid
def is_valid_move(piece, x, y, rotation):
    rotated_piece = rotate_tetromino(piece, rotation)
    for dy, row in enumerate(rotated_piece):
        for dx, cell in enumerate(row):
            if cell:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT or (ny >= 0 and grid[ny][nx]):
                    return False
    return True

# Rotate a tetromino
def rotate_tetromino(piece, rotation):
    return [list(reversed(col)) for col in zip(*piece)] if rotation % 4 != 0 else piece

# Add piece to grid
def add_to_grid(piece, x, y, rotation, color):
    rotated_piece = rotate_tetromino(piece, rotation)
    for dy, row in enumerate(rotated_piece):
        for dx, cell in enumerate(row):
            if cell:
                nx, ny = x + dx, y + dy
                if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                    grid[ny][nx] = color

# Clear full lines
def clear_lines():
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_lines)

# Main game loop
def main():
    current_piece, current_color = random.choice(TETROMINOS)
    next_piece, next_color = random.choice(TETROMINOS)
    piece_x, piece_y, piece_rotation = GRID_WIDTH // 2 - len(current_piece[0]) // 2, 0, 0
    score = 0
    fall_time = 0
    fall_speed = 500  # ms

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if is_valid_move(current_piece, piece_x - 1, piece_y, piece_rotation):
                        piece_x -= 1
                if event.key == pygame.K_RIGHT:
                    if is_valid_move(current_piece, piece_x + 1, piece_y, piece_rotation):
                        piece_x += 1
                if event.key == pygame.K_DOWN:
                    if is_valid_move(current_piece, piece_x, piece_y + 1, piece_rotation):
                        piece_y += 1
                if event.key == pygame.K_UP:
                    if is_valid_move(current_piece, piece_x, piece_y, piece_rotation + 1):
                        piece_rotation += 1

        # Fall the piece
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time > fall_speed:
            fall_time = 0
            if is_valid_move(current_piece, piece_x, piece_y + 1, piece_rotation):
                piece_y += 1
            else:
                add_to_grid(current_piece, piece_x, piece_y, piece_rotation, current_color)
                cleared_lines = clear_lines()
                score += cleared_lines * 100
                current_piece, current_color = next_piece, next_color
                next_piece, next_color = random.choice(TETROMINOS)
                piece_x, piece_y, piece_rotation = GRID_WIDTH // 2 - len(current_piece[0]) // 2, 0, 0
                if not is_valid_move(current_piece, piece_x, piece_y, piece_rotation):
                    running = False

        # Draw everything
        draw_grid()
        rotated_current_piece = rotate_tetromino(current_piece, piece_rotation)
        for dy, row in enumerate(rotated_current_piece):
            for dx, cell in enumerate(row):
                if cell:
                    nx, ny = piece_x + dx, piece_y + dy
                    if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                        draw_block(nx, ny, current_color)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()