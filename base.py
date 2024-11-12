import pygame, random, sys
from pygame.locals import *
from sys import exit

# SYSTEM
FPS = 30
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
COIN_SIZE = 20
COIN_SPAWNRATE = 3

# COLORS
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

BG_COLOR = ORANGE
COIN_COLOR = YELLOW
CASH_COLOR = GREEN

# CHARACTER
CHARACTER_COLOR = RED
CHARACTER_SIZE = 50
PLAYER_SPEED = 10
PLAYER_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
HP = 3
POINTS = 0


class Player:

    def __init__(self, position: list, speed: int, hp: int, points: int):
        self.pos = position
        self.speed = speed
        self.hp = hp
        self.points = points

    def __str__(self):
        return str(f"HP: {self.hp}, POINTS: {self.points}")


class Coin:

    def __init__(self, color):
        self.color = color


'''
SYSTEM FUNC
'''

# MAIN
def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Catch Your Paycheck!')

    start_screen()
    while True:
        run_game()
        game_over_screen()

# UKONCENIE HRY
def end_game():
    pygame.quit()
    sys.exit()

# V PODSTATE MENU S TLACITKOM START A SETTINGS
def start_screen():
    pass

# NASTAVENIA - turn on/off bg_music, volume, theme (dark abyss, eternal light, hot pink), return to menu button
def settings():
    pass

# GAME OVER SCREEN - hra sa zastavi, okienko s "game over" a hracovym score (+ mozno highscore), try again button, return to menu button
def game_over_screen():
    pass


'''
GAME FUNC
'''

# GENEROVANIE HRACA NA ZACIATKU
def get_new_character():
    # TO DO
    return Player(PLAYER_POSITION, PLAYER_SPEED, HP, POINTS)

# GENEROVANIE NAHODNEJ POZICIE COINU
def random_coin_pos():
    # TO DO
    return [random.randint(0, SCREEN_WIDTH - COIN_SIZE), random.randint(0, SCREEN_HEIGHT - COIN_SIZE)]

# ZOBRAZENIE STAVU HRACA - HP, POINTS
def draw_hud():
    pass


'''
MINIGAMES
'''

# MINIHRA 1 - 
def mini_game_1():
    pass

# MINIHRA 2 - 
def mini_game_2():
    pass


'''
GAME LOOP
'''

def run_game():
    player = get_new_character()
    coin = random_coin_pos()
    direction = " "

    while True: # MAIN GAME LOOP
        DISPLAY_SURF.fill(BG_COLOR)
        EVENTS = pygame.event.get()
        for event in EVENTS: # EVENTY
            if event.type == QUIT:
                end_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    end_game()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
