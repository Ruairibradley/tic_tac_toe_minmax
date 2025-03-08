"""
Tic-Tac-Toe AI using Pygame and Minimax Algorithm

This program allows a human player to play Tic-Tac-Toe against an AI opponent.
The AI can play at three difficulty levels:
- Easy: Random moves
- Medium: Minimax with limited depth
- Hard: Full Minimax (perfect play)

Author: Your Name
Date: March 2025
"""

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
difficulty = "Hard"  # Set AI difficulty level (Easy, Medium, Hard)

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe AI')
screen.fill(BG_COLOR)


def draw_grid():
    """Draws the Tic-Tac-Toe grid on the screen."""
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    """Draws X and O on the board based on the current game state."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                           row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)


def is_winner(player):
    """Checks if a given player ('X' or 'O') has won the game."""
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_draw():
    """Checks if the game is a draw (no empty spaces left)."""
    return all(board[row][col] != ' ' for row in range(3) for col in range(3))


def minimax(board, depth, is_maximizing):
    """Minimax algorithm to determine the best move for the AI."""
    if is_winner(ai):
        return 1  # AI wins
    if is_winner(player):
        return -1  # Player wins
    if is_draw():
        return 0  # Draw

    if difficulty == "Medium" and depth >= 2:  # Limit depth for medium difficulty
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '  # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '  # Undo move
                    best_score = min(score, best_score)
        return best_score


def best_move():
    """AI determines the best move based on the chosen difficulty."""
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
                board[i][j] = ' '  # Undo move
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def reset_board():
    """Resets the game board and redraws the grid."""
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    screen.fill(BG_COLOR)
    draw_grid()


# Draw initial grid
draw_grid()
running = True
game_over = False

# Main game loop
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

        # Reset game when clicking after game over
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            reset_board()
            game_over = False

    # Update game visuals
    screen.fill(BG_COLOR)
    draw_grid()
    draw_figures()
    pygame.display.update()

pygame.quit()
