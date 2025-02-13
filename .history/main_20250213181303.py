from flask import Flask, render_template_string, send_from_directory
import threading
import time
import random
import os

# Flask uygulamasını başlat
app = Flask(__name__)

# Oyun alanı boyutları
WIDTH = 10
HEIGHT = 20

# Tetromino şekilleri
TETROMINOS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 0, 1]],  # L
    [[1, 1, 1], [1, 0, 0]]   # J
]

# Rastgele tetromino seçimi
def get_random_tetromino():
    return random.choice(TETROMINOS)

# Oyun durumu
board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
current_tetromino = get_random_tetromino()
x, y = WIDTH // 2, 0

# Oyun döngüsünü başlat
def game_loop():
    global y, current_tetromino
    while True:
        time.sleep(0.5)  # Her 0.5 saniyede bir tetrominoyu bir satır aşağı taşı
        y += 1
        if y + len(current_tetromino) >= HEIGHT:  # Eğer alan doluysa yeni bir tetromino oluştur
            current_tetromino = get_random_tetromino()
            x, y = WIDTH // 2, 0

# Favicon sunma
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Ana sayfa
@app.route('/')
def index():
    global board
    board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]  # Board'u temizle
    for dy, row in enumerate(current_tetromino):  # Mevcut tetrominoyu board'a ekle
        for dx, cell in enumerate(row):
            if cell:
                if 0 <= y + dy < HEIGHT and 0 <= x + dx < WIDTH:
                    board[y + dy][x + dx] = 1
    board_str = "\n".join("".join("#" if cell else " " for cell in row) for row in board)
    return render_template_string(HTML_TEMPLATE, board=board_str)

# HTML şablonu
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Tetris</title>
</head>
<body>
    <pre>{{ board|safe }}</pre>
</body>
</html>
"""

if __name__ == '__main__':
    threading.Thread(target=game_loop, daemon=True).start()  # Oyun döngüsünü başlatabilmek için ayrı bir thread kullan
    app.run(host='0.0.0.0', port=8000)  # Flask uygulamasını çalıştır