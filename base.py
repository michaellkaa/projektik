import pygame, random, sys
from pygame.locals import *
from sys import exit

# SYSTEM
FPS = 60
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
COIN_SIZE = 25

# COLORS
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 153, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 51, 153)

BG_COLOR = ORANGE
COIN_COLOR = YELLOW
CASH_COLOR = GREEN

# CHARACTER
CHARACTER_COLOR = BLACK
CHARACTER_SIZE = 50
PLAYER_SPEED = 12
PLAYER_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
HP = 3
POINTS = 0

# MINI GAMES - changeable
MINIGAME_TIME_LIMIT = 20  # 20 SEKUND
MINIGAME_ACTIVE = False


class Player:

    def __init__(self, position: list, status: str):
        self.pos = position
        self.status = status

    def __str__(self):
        return str(self.pos)
    
    def move(self, direction):
        if direction == 'up' and self.pos[1] > 0:
            self.pos[1] -= PLAYER_SPEED
        elif direction == 'down' and self.pos[1] < SCREEN_HEIGHT - CHARACTER_SIZE:
            self.pos[1] += PLAYER_SPEED
        elif direction == 'left' and self.pos[0] > 0:
            self.pos[0] -= PLAYER_SPEED
        elif direction == 'right' and self.pos[0] < SCREEN_WIDTH - CHARACTER_SIZE:
            self.pos[0] += PLAYER_SPEED


class Coin:

    def __init__(self, color, position):
        self.color = color
        self.position = position

    def toggle_special(self):
        if random.choice([True, False, False]) == True:
            self.color = CASH_COLOR
        else:
            self.color = COIN_COLOR


'''
SYSTEM FUNC
'''

# MAIN
def main():
    global FPS_CLOCK, SCREEN, BASIC_FONT, POINTS
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Catch Your Paycheck!')

    POINTS = 0
    while True:
        run_game()
        game_over_screen()

# UKONCENIE HRY
def end_game():
    pygame.quit()
    sys.exit()

# GAME OVER SCREEN - hra sa zastavi, okienko s "game over" a hracovym score (+ mozno highscore), try again button, return to menu button
def game_over_screen():
    pass


'''
GAME FUNC
'''

# GENEROVANIE HRACA NA ZACIATKU
def get_new_character():
<<<<<<< Updated upstream
=======
    # TO DO
>>>>>>> Stashed changes
    return Player(PLAYER_POSITION, "")


# GENEROVANIE NAHODNEJ POZICIE COINU
def random_coin_pos():
    return [random.randint(0, SCREEN_WIDTH - COIN_SIZE), random.randint(0, SCREEN_HEIGHT - COIN_SIZE)]

# ZOBRAZENIE STAVU HRACA - HP, POINTS
def draw_hud():
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f"HP: {HP}", True, BLACK)
    points_text = font.render(f"Score: {POINTS}", True, WHITE)
    SCREEN.blit(hp_text, (10, 10))
    SCREEN.blit(points_text, (10, 50))


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
    global POINTS
    player = get_new_character()
    coin_position = random_coin_pos()
    coin = Coin(COIN_COLOR, coin_position)
    direction = ""
    coin_count = 0
    
    while True:
        SCREEN.fill(BG_COLOR)
        EVENTS = pygame.event.get()
        for event in EVENTS:  # EVENTS
            if event.type == QUIT:
                end_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    end_game()

        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            player.move('up')
        elif keys[K_DOWN] or keys[K_s]:
            player.move('down')
        elif keys[K_LEFT] or keys[K_a]:
            player.move('left')
        elif keys[K_RIGHT] or keys[K_d]:
            player.move('right')

        pygame.draw.rect(SCREEN, RED, (player.pos[0]+20, player.pos[1]+5, CHARACTER_SIZE, CHARACTER_SIZE+20))
        pygame.draw.rect(SCREEN, CHARACTER_COLOR, (player.pos[0], player.pos[1], CHARACTER_SIZE, CHARACTER_SIZE+20))
        pygame.draw.rect(SCREEN, coin.color, (coin.position[0], coin.position[1], COIN_SIZE, COIN_SIZE))

        player_rect = pygame.Rect(player.pos[0], player.pos[1], CHARACTER_SIZE, CHARACTER_SIZE+20)
        coin_rect = pygame.Rect(coin.position[0], coin.position[1], COIN_SIZE, COIN_SIZE)
        if player_rect.colliderect(coin_rect):
            if coin.color == CASH_COLOR:
                POINTS += 5
            else:
                POINTS += 1
            coin_count += 1
            coin.position = random_coin_pos()
            coin.toggle_special()

        draw_hud()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
