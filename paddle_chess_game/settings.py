# settings.py

# Board dimensions
BOARD_COLS = 8  # Number of columns (files)
BOARD_ROWS = 13  # Number of rows (ranks) - reduced to fit navbar
NAVBAR_HEIGHT = 60

# Screen dimensions - calculated to have perfect squares with no margins
CELL_SIZE = 70  # Size of each square cell in pixels (adjust this to change overall size)
SCREEN_WIDTH = BOARD_COLS * CELL_SIZE  # 8 * 60 = 480
SCREEN_HEIGHT = BOARD_ROWS * CELL_SIZE + NAVBAR_HEIGHT
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (66, 135, 245)
GREEN = (60, 179, 113)
YELLOW = (255, 215, 0)
GREY = (200, 200, 200)
BEIGE = (245, 245, 220)
BROWN = (139, 69, 19)

# Paddle (now horizontal to protect chess pieces from top/bottom)
PADDLE_WIDTH = 100  # Wide horizontal paddle
PADDLE_HEIGHT = 16  # Thin height
PADDLE_SPEED = 7

# Ball
BALL_RADIUS = 10
BALL_SPEED_X = 3
BALL_SPEED_Y = 2
BALL_DAMAGE = 1

# Chess Pieces lives by type
CHESS_PIECES_LIVES = {
    "roi": 3,
    "reine": 2,
    "fou": 2,
    "tour": 2,
    "chevalier": 2,
    "pion": 1,
}

# Score values
PIECE_VALUES = {
    "pion": 10,
    "chevalier": 30,
    "fou": 30,
    "tour": 30,
    "reine": 50,
    "roi": 100
}

# Chess pieces geometry
PIECE_WIDTH = 36
PIECE_HEIGHT = 36
PIECE_SPACING_X = 8
PIECE_SPACING_Y = 8

# UI / Fonts
TITLE = "Paddle + Chess"
WIN_TEXT = "Victoire , felicitations ! Le roi adverse est K.O."
RESET_HINT = "Appuie sur R pour rejouer, ESC pour quitter"
