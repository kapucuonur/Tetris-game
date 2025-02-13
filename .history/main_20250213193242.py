from flask import Flask, render_template_string
import threading
import pygame
import random
import os
import time

app = Flask(__name__)

# Pygame initialize
pygame.init()
pygame.mixer.quit()  # Ses modülünü devre dışı bırak

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

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
    return f'<rect x="{x * BLOCK_SIZE}" y="{y * BLOCK_SIZE}" width="{BLOCK_SIZE}" height="{BLOCK_SIZE}" fill="{color}" stroke="white" />'

# Draw the entire grid
def draw_grid():
    svg_elements = []
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                svg_elements.append(draw_block(x, y, val))
    return ''.join(svg_elements)

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
                    print(f"Block added at ({nx}, {ny}) with color {color}")  # Debug için

# Clear full lines
def clear_lines():
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_lines)

# Game state
current_piece, current_color = random.choice(TETROMINOS)
next_piece, next_color = random.choice(TETROMINOS)
piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
piece_y = 0
piece_rotation = 0
score = 0
game_over = False  # Oyunun bitip bitmediğini kontrol etmek için

# Game loop
def game_loop():
    global piece_x, piece_y, piece_rotation, score, current_piece, current_color, next_piece, next_color, game_over

    while not game_over:
        time.sleep(0.5)  # Her 0.5 saniyede bir tetrominoyu bir satır aşağı taşı
        if not is_valid_move(current_piece, piece_x, piece_y + 1, piece_rotation):  # current_piece[0] yerine current_piece
            add_to_grid(current_piece, piece_x, piece_y, piece_rotation, current_color)
            cleared_lines = clear_lines()
            score += cleared_lines * 100

            # Yeni tetromino oluştur
            current_piece, current_color = next_piece, next_color
            next_piece, next_color = random.choice(TETROMINOS)
            piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
            piece_y = 0
            piece_rotation = 0

            # Yeni tetromino geçerli bir pozisyonda değilse, oyunu bitir
            if not is_valid_move(current_piece, piece_x, piece_y, piece_rotation):
                game_over = True
                print("Game Over! Final Score:", score)
        else:
            piece_y += 1

@app.route('/')
def index():
    global grid, game_over, score
    svg_content = f'''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SCREEN_WIDTH} {SCREEN_HEIGHT}" style="background-color: black;">
        {draw_grid()}
    </svg>
    '''
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tetris</title>
        <meta http-equiv="refresh" content="0.5">
    </head>
    <body>
        <h1>Score: {score}</h1>
        <div>{svg_content}</div>
        {"<h2>Game Over!</h2>" if game_over else ""}
    </body>
    </html>
    '''

if __name__ == '__main__':
    threading.Thread(target=game_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))