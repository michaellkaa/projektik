import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
CIRCLE_RADIUS = 60
CROSS_WIDTH = 15

THEMES = [
    {"bg": (162, 178, 159), "text": (248, 237, 227), "button": (121, 135, 119)},  # SVETLO ZELENA
    {"bg": (96, 153, 102), "text": (237, 241, 214), "button": (64, 81, 59)},  # TMAVO ZELENA
    {"bg": (232, 184, 109), "text": (245, 247, 248), "button": (250, 188, 63)},  # SVETLO ZLTA
    {"bg": (96, 139, 193), "text": (243, 243, 224), "button": (19, 62, 135)},  # TMAVO MODRA
    {"bg": (255, 180, 194), "text": (253, 255, 210), "button": (102, 123, 198)} # SVETLO RUZOVA
]

ctheme = THEMES[0]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(ctheme["bg"])

font = pygame.font.Font(None, 74)
message_font = pygame.font.Font(None, 54)

board = [[None] * 3 for _ in range(3)]
current_player = "player"

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, ctheme["button"], (0, HEIGHT // 3 * i), (WIDTH, HEIGHT // 3 * i), LINE_WIDTH)
        pygame.draw.line(screen, ctheme["button"], (WIDTH // 3 * i, 0), (WIDTH // 3 * i, HEIGHT), LINE_WIDTH)

def draw_mark(row, col, player):
    x = col * (WIDTH // 3) + (WIDTH // 6)
    y = row * (HEIGHT // 3) + (HEIGHT // 6)
    if player == "player":  # X
        pygame.draw.line(screen, ctheme["text"], (x - 40, y - 40), (x + 40, y + 40), CROSS_WIDTH)
        pygame.draw.line(screen, ctheme["text"], (x - 40, y + 40), (x + 40, y - 40), CROSS_WIDTH)
    else:  # O
        pygame.draw.circle(screen, ctheme["text"], (x, y), CIRCLE_RADIUS, LINE_WIDTH)

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    if all(cell is not None for row in board for cell in row):  
        return "draw"
    return None

def pc_move():
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = "pc"
                if check_winner() == "pc":
                    return row, col
                board[row][col] = "player"
                if check_winner() == "player":
                    board[row][col] = "pc"
                    return row, col
                board[row][col] = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = "pc"
                return row, col

def display_message(text):
    message = message_font.render(text, True, ctheme["button"])
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

running = True
draw_grid()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN and current_player == "player":
            x, y = event.pos
            row, col = y // (HEIGHT // 3), x // (WIDTH // 3)
            if board[row][col] is None:
                board[row][col] = "player"
                draw_mark(row, col, "player")
                winner = check_winner()
                if winner:
                    if winner == "draw":
                        display_message("Remíza!")
                    elif winner == "player":
                        display_message("Vyhrál jsi!")
                    elif winner == "pc":
                        display_message("Prohrál jsi!")
                    running = False
                else:
                    current_player = "pc"

        if current_player == "pc" and running:
            row, col = pc_move()
            draw_mark(row, col, "pc")
            winner = check_winner()
            if winner:
                if winner == "draw":
                    display_message("Remíza!")
                elif winner == "player":
                    display_message("Vyhrál jsi!")
                elif winner == "pc":
                    display_message("Prohrál jsi!")
                running = False
            else:
                current_player = "player"

    pygame.display.flip()

pygame.quit()
sys.exit()
