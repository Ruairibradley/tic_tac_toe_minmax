import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 10
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Game variables
board = [[' ' for _ in range(3)] for _ in range(3)]
player = 'X'
ai = 'O'
difficulty = "Medium"  # Set AI difficulty

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)


# Draw grid lines
def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


# Draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                           row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)


# Check for winner
def is_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


# Check for draw
def is_draw():
    return all(board[row][col] != ' ' for row in range(3) for col in range(3))


# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if is_winner(ai):
        return 1
    if is_winner(player):
        return -1
    if is_draw():
        return 0

    if difficulty == "Medium" and depth >= 2:  # Limit depth for medium difficulty
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score


# AI chooses best move
def best_move():
    if difficulty == "Easy":
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        return random.choice(empty_cells) if empty_cells else None

    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


# Reset the board
def reset_board():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    screen.fill(BG_COLOR)
    draw_grid()


# Game loop
draw_grid()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

            if board[row][col] == ' ':
                board[row][col] = player
                if is_winner(player):
                    print("You win!")
                    game_over = True
                elif is_draw():
                    print("It's a draw!")
                    game_over = True
                else:
                    move = best_move()
                    if move:
                        board[move[0]][move[1]] = ai
                        if is_winner(ai):
                            print("AI wins!")
                            game_over = True

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            reset_board()
            game_over = False

    screen.fill(BG_COLOR)
    draw_grid()
    draw_figures()
    pygame.display.update()

pygame.quit()
