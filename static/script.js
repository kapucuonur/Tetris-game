const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
const nextCanvas = document.getElementById('next-piece');
const nextContext = nextCanvas.getContext('2d');

const ROWS = 20;
const COLS = 10;
const BLOCK_SIZE = 30;
const SHAPES = [
    [[1, 1, 1, 1]], // I
    [[1, 1], [1, 1]], // O
    [[1, 1, 0], [0, 1, 1]], // Z
    [[0, 1, 1], [1, 1, 0]], // S
    [[1, 1, 1], [0, 1, 0]], // T
    [[1, 1, 1], [1, 0, 0]], // L
    [[1, 1, 1], [0, 0, 1]]  // J
];

const COLORS = [
    '#00FFFF', // Cyan
    '#FFFF00', // Yellow
    '#FFA500', // Orange
    '#0000FF', // Blue
    '#00FF00', // Green
    '#FF0000', // Red
    '#800080'  // Purple
];

let grid = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
let currentPiece = createPiece();
let nextPiece = createPiece();
let score = 0;
let level = 1;
let gameOver = false;

function createPiece() {
    const shape = SHAPES[Math.floor(Math.random() * SHAPES.length)];
    return {
        shape,
        color: COLORS[Math.floor(Math.random() * COLORS.length)],
        x: Math.floor(COLS / 2) - Math.floor(shape[0].length / 2),
        y: 0
    };
}

function drawPiece(piece, context) {
    piece.shape.forEach((row, i) => {
        row.forEach((cell, j) => {
            if (cell) {
                context.fillStyle = piece.color;
                context.fillRect((piece.x + j) * BLOCK_SIZE, (piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                context.strokeStyle = '#34495e';
                context.strokeRect((piece.x + j) * BLOCK_SIZE, (piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        });
    });
}

function drawGrid() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    grid.forEach((row, i) => {
        row.forEach((cell, j) => {
            if (cell) {
                context.fillStyle = cell;
                context.fillRect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                context.strokeStyle = '#34495e';
                context.strokeRect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        });
    });
}

function update() {
    if (!gameOver) {
        if (validMove(currentPiece, currentPiece.x, currentPiece.y + 1)) {
            currentPiece.y++;
        } else {
            placePiece();
            currentPiece = nextPiece;
            nextPiece = createPiece();
            if (!validMove(currentPiece, currentPiece.x, currentPiece.y)) {
                gameOver = true;
                alert(`Game Over! Your Score: ${score}`);
            }
        }
        draw();
    }
}

function draw() {
    drawGrid();
    drawPiece(currentPiece, context);
    nextContext.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
    drawPiece({ ...nextPiece, x: 1, y: 1 }, nextContext); // Draw next piece in the info panel
    document.getElementById('score').innerText = score;
    document.getElementById('level').innerText = level;
}

function placePiece() {
    currentPiece.shape.forEach((row, i) => {
        row.forEach((cell, j) => {
            if (cell) {
                grid[currentPiece.y + i][currentPiece.x + j] = currentPiece.color;
            }
        });
    });
    clearLines();
}

function clearLines() {
    let linesCleared = 0;
    grid = grid.filter(row => !row.every(cell => cell));
    while (grid.length < ROWS) {
        grid.unshift(Array(COLS).fill(0));
        linesCleared++;
    }
    score += linesCleared * 100;
    level = 1 + Math.floor(score / 1000);
}

function validMove(piece, x, y) {
    return piece.shape.every((row, i) =>
        row.every((cell, j) =>
            !cell || (grid[y + i] && grid[y + i][x + j] === 0)
        )
    );
}

document.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') {
        if (validMove(currentPiece, currentPiece.x - 1, currentPiece.y)) {
            currentPiece.x--;
        }
    } else if (event.key === 'ArrowRight') {
        if (validMove(currentPiece, currentPiece.x + 1, currentPiece.y)) {
            currentPiece.x++;
        }
    } else if (event.key === 'ArrowDown') {
        if (validMove(currentPiece, currentPiece.x, currentPiece.y + 1)) {
            currentPiece.y++;
        }
    } else if (event.key === 'ArrowUp') {
        const rotated = rotatePiece(currentPiece);
        if (validMove(rotated, currentPiece.x, currentPiece.y)) {
            currentPiece.shape = rotated.shape;
        }
    }
    draw();
});

// Dokunmatik Kontroller
document.getElementById('left').addEventListener('click', () => {
    if (validMove(currentPiece, currentPiece.x - 1, currentPiece.y)) {
        currentPiece.x--;
    }
    draw();
});

document.getElementById('right').addEventListener('click', () => {
    if (validMove(currentPiece, currentPiece.x + 1, currentPiece.y)) {
        currentPiece.x++;
    }
    draw();
});

document.getElementById('rotate').addEventListener('click', () => {
    const rotated = rotatePiece(currentPiece);
    if (validMove(rotated, currentPiece.x, currentPiece.y)) {
        currentPiece.shape = rotated.shape;
    }
    draw();
});

document.getElementById('down').addEventListener('click', () => {
    if (validMove(currentPiece, currentPiece.x, currentPiece.y + 1)) {
        currentPiece.y++;
    }
    draw();
});
document.getElementById('fullscreen').addEventListener('click', () => {
    if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen();
    }
});
function rotatePiece(piece) {
    const rotated = piece.shape[0].map((_, i) =>
        piece.shape.map(row => row[i]).reverse()
    );
    return { ...piece, shape: rotated };
}

setInterval(update, 1000 / level);