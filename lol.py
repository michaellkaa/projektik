import pygame
from pygame.locals import *
import sys
import random

TILE_SIZE = 120
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30
BLANK = None

Last_click = False


WHITE = (255, 255, 255)
PRINCESS_PINK = (255, 177, 207)

TILE_COLOR = PRINCESS_PINK
TEXT_COLOR = WHITE
BASIC_FONT_SIZE = 20

MESSAGE_COLOR = WHITE

FPS_CLOCK = None
DISPLAY_SURFACE = None
BASIC_FONT = None

# VYKRESLENIE CHUJOVIN
def scissors_tile(square_x, square_y):
    message = "Scissors"
    pygame.draw.rect(DISPLAY_SURFACE, TILE_COLOR, (square_x, square_y, TILE_SIZE, TILE_SIZE))
    text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
    text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
    DISPLAY_SURFACE.blit(text_obj, text_rect)

def rock_tile(square_x, square_y):
    square_x = (WINDOW_WIDTH - TILE_SIZE) / 2 - TILE_SIZE - 10
    message = "Rock"
    pygame.draw.rect(DISPLAY_SURFACE, TILE_COLOR, (square_x, square_y, TILE_SIZE, TILE_SIZE))
    text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
    text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
    DISPLAY_SURFACE.blit(text_obj, text_rect)

def paper_tile(square_x, square_y):
    square_x = (WINDOW_WIDTH - TILE_SIZE) / 2 + TILE_SIZE + 10
    message = "Paper"
    pygame.draw.rect(DISPLAY_SURFACE, TILE_COLOR, (square_x, square_y, TILE_SIZE, TILE_SIZE))
    text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
    text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
    DISPLAY_SURFACE.blit(text_obj, text_rect)

def game(square_x, square_y):
    scissors_tile(square_x, square_y)
    rock_tile(square_x, square_y)
    paper_tile(square_x, square_y)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def terminate():
    pygame.quit()
    sys.exit()

def mouse_click(square_x, square_y):
    global Last_click
    if pygame.mouse.get_pressed()[0] and Last_click == False:
        pos = pygame.mouse.get_pos()
        pick = check_boxes(pos[0], pos[1], square_x, square_y)
        if pick != None:
            enemy_pick = ["Rock", "Scissors", "Paper"][random.randint(1, 3) - 1]
            DISPLAY_SURFACE.fill((0, 0, 0))
            if pick == enemy_pick:
                message = "It's a tie"
                text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                DISPLAY_SURFACE.blit(text_obj, text_rect)
            elif (pick == "Rock" and enemy_pick == "Paper") or (pick == "Paper" and enemy_pick == "Scissors") or (pick == "Scissors" and enemy_pick ==  "Rock"):
                message = "You won"
                text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                DISPLAY_SURFACE.blit(text_obj, text_rect)
            elif (pick == "Rock" and enemy_pick == "Scissors") or (pick == "Paper" and enemy_pick == "Rock") or (pick == "Scissors" and enemy_pick ==  "Paper"):
                message = "You lose"
                text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                DISPLAY_SURFACE.blit(text_obj, text_rect)
            pygame.display.update()
            pygame.time.delay(1000)

    Last_click = pygame.mouse.get_pressed()[0]

def check_boxes(mouse_x, mouse_y, square_x, square_y):
    global TILE_SIZE
    rock_left = (WINDOW_WIDTH - TILE_SIZE) / 2 - TILE_SIZE - 10
    rock_right = (WINDOW_WIDTH - TILE_SIZE) / 2 - 10
    scissors_left = (WINDOW_WIDTH - TILE_SIZE) / 2
    scissors_right = (WINDOW_WIDTH - TILE_SIZE) / 2 + TILE_SIZE
    paper_left = (WINDOW_WIDTH - TILE_SIZE) / 2 + TILE_SIZE + 10
    paper_right = (WINDOW_WIDTH - TILE_SIZE) / 2 + 2 * TILE_SIZE + 10
    tile_top = (WINDOW_HEIGHT - TILE_SIZE) / 2
    tile_bottom = (WINDOW_HEIGHT - TILE_SIZE) / 2 + TILE_SIZE

    if rock_left <= mouse_x <= rock_right and tile_top <= mouse_y <= tile_bottom:
        return "Rock"
    if scissors_left <= mouse_x <= scissors_right and tile_top <= mouse_y <= tile_bottom:
        return "Scissors"
    if paper_left <= mouse_x <= paper_right and tile_top <= mouse_y <= tile_bottom:
        return "Paper"
    return None


def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Rock, paper, scissors')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
    pygame.display.update()
    FPS_CLOCK.tick(FPS)

    square_x = (WINDOW_WIDTH - TILE_SIZE) / 2
    square_y = (WINDOW_HEIGHT - TILE_SIZE) / 2

    while True:
        FPS_CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        game(square_x, square_y) 
        mouse_click(square_x, square_y) 

        pygame.display.update()
        FPS_CLOCK.tick(FPS)




if __name__ == '__main__':
    main()