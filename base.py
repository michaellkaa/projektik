import pygame
import random
import os
import sys
from pygame.locals import *

pygame.init()
pygame.font.init() 

# SYSTEM
FPS = 60
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# COLORS
RED = (255, 0, 0)
GREEN = (0, 153, 0)
YELLOW = (254, 236, 55)
ORANGE = (255, 128, 0)
PURPLE = (183,104,162)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 51, 153)
GRAY = (100, 100, 100)
DARK_MODE_BG = (30, 30, 30)
LIGHT_MODE_BG = (255, 255, 255)
DARK_GREEN = (26, 26, 25)

BG_COLOR = PURPLE
COIN_COLOR = YELLOW
COIN_SIZE = 30
CASH_COLOR = GREEN

# CHARACTER
CHARACTER_COLOR = BLACK
CHARACTER_SIZE = 100
PLAYER_SPEED = 12
PLAYER_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
HP = 5
POINTS = 0

# MENU
THEMES = [
    {"bg": (162, 178, 159), "text": (248, 237, 227), "button": (121, 135, 119)},  # SVETLO ZELENA
    {"bg": (96, 153, 102), "text": (237, 241, 214), "button": (64, 81, 59)},  # TMAVO ZELENA
    {"bg": (232, 184, 109), "text": (245, 247, 248), "button": (250, 188, 63)},  # SVETLO ZLTA
    {"bg": (96, 139, 193), "text": (243, 243, 224), "button": (19, 62, 135)},  # TMAVO MODRA
    {"bg": (255, 180, 194), "text": (253, 255, 210), "button": (102, 123, 198)} # SVETLO RUZOVA
    ]
theme_index = 0
current_theme = THEMES[theme_index]

# FONT + NOVY FONT
font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)

# HUDBA V MENU 
pygame.mixer.music.load("Meow.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)
volume_level = 50  
sound_on = True

# CASH V MENU
money_image = pygame.image.load("cash.png") 
falling_money = [] 

# MINIGAME 1
result = None
TILE_SIZE = 120
BLANK = None
Last_click = False
PRINCESS_PINK = (255, 177, 207)
TILE_COLOR = PRINCESS_PINK
TEXT_COLOR = WHITE
BASIC_FONT_SIZE = 20
MESSAGE_COLOR = WHITE


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.left_sprites = [
            pygame.image.load("player_still_l.png").convert_alpha(),
            pygame.image.load("player_l1.png").convert_alpha(),
            pygame.image.load("player_l2.png").convert_alpha(),
            pygame.image.load("player_l3.png").convert_alpha()]
        self.right_sprites = [
            pygame.image.load("player_still_r.png").convert_alpha(),
            pygame.image.load("player_r1.png").convert_alpha(),
            pygame.image.load("player_r2.png").convert_alpha(),
            pygame.image.load("player_r3.png").convert_alpha()]
        self.left_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.left_sprites]
        self.right_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.right_sprites]
        self.up_sprites = [
            pygame.image.load("player_still_l.png").convert_alpha(),
            pygame.image.load("player_l1.png").convert_alpha(),
            pygame.image.load("player_l2.png").convert_alpha(),
            pygame.image.load("player_l3.png").convert_alpha()]
        self.down_sprites = [
            pygame.image.load("player_d1.png").convert_alpha(),
            pygame.image.load("player_d2.png").convert_alpha(),
            pygame.image.load("player_d1.png").convert_alpha(),
            pygame.image.load("player_d3.png").convert_alpha()]
        self.up_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE)) for img in self.up_sprites]
        self.down_sprites = [pygame.transform.scale(img, (CHARACTER_SIZE-(CHARACTER_SIZE//3), CHARACTER_SIZE)) for img in self.down_sprites]

        self.image = self.right_sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 100
        self.direction = "right"

    def move(self, keys, screen_rect):
        moved = False
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= PLAYER_SPEED
            self.direction = "left"
            moved = True
        elif keys[K_RIGHT] or keys[K_d]:
            self.rect.x += PLAYER_SPEED
            self.direction = "right"
            moved = True
        elif keys[K_UP] or keys[K_w]:
            self.rect.y -= PLAYER_SPEED
            self.direction = "up"
            moved = True
        elif keys[K_DOWN] or keys[K_s]:
            self.rect.y += PLAYER_SPEED
            self.direction = "down"
            moved = True

        self.rect.clamp_ip(screen_rect)
        if moved:
            self.update_animation()

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.animation_speed:
            self.animation_timer = now
            self.frame_index = (self.frame_index + 1) % 4

            if self.direction == "left":
                self.image = self.left_sprites[self.frame_index]
            elif self.direction == "right":
                self.image = self.right_sprites[self.frame_index]
            if self.direction == "up":
                self.image = self.up_sprites[self.frame_index]
            elif self.direction == "down":
                self.image = self.down_sprites[self.frame_index]


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        except pygame.error:
            self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
            self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.special = False

    def toggle_special(self):
        self.special = random.choice([True, False, False])  # Randomly determine if the coin is special
        if self.special == True:
            try:
                self.image = pygame.image.load("cash.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (COIN_SIZE+(COIN_SIZE//2), COIN_SIZE))
            except pygame.error:
                self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
                self.image.fill(COIN_COLOR)
        else:
            try:
                self.image = pygame.image.load("coin.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
            except pygame.error:
                self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
                self.image.fill(COIN_COLOR)


    def update_image(self):
        if self.special:
            self.image.fill(CASH_COLOR)
        else:
            self.image.fill(COIN_COLOR)


'''
SYSTEM FUNC
'''

# MAIN
def main():
    global FPS_CLOCK, SCREEN, BASIC_FONT, POINTS
    FPS_CLOCK = pygame.time.Clock()
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('CAT Your Paycheck!')

    POINTS = 0
    while True:
        run_game()


# END GAME
def end_game():
    pygame.quit()
    sys.exit()

# GAME OVER SCREEN - placeholder
def game_over_screen():
    pass

# TEXT
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# HLAVNE MENU
def main_menu():
    while True:
        global SCREEN
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('CAT Your Paycheck!')
        # FARBA POZADIA
        SCREEN.fill(current_theme["bg"])

        draw_text("!CAT Your Paycheck!", font, YELLOW, SCREEN, SCREEN_WIDTH // 2, 195)

        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 550, 200, 50)

        pygame.draw.rect(SCREEN, DARK_GREEN, start_button)
        pygame.draw.rect(SCREEN, DARK_GREEN, settings_button)
        pygame.draw.rect(SCREEN, DARK_GREEN, exit_button)

        draw_text("Start", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 375)
        draw_text("Settings", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 475)
        draw_text("Exit", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 575)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return True
                if settings_button.collidepoint(event.pos):
                    settings_menu()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()  
                    sys.exit()

        pygame.display.flip()

# NASTAVENIA + START GAME
def start_open():
    os.execlp("python", "python", "game.py")
    
def settings_menu():
    global theme_index, current_theme, sound_on, volume_level
    volume_slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 440, 200, 20)
    volume_slider = pygame.Rect(SCREEN_WIDTH // 2 - 100 + (volume_level * 2), 440, 10, 20)

    while True:
        # FARBA POZADIA
        SCREEN.fill(current_theme["bg"])

        draw_text("SETTINGS", font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 150)

        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 50)
        theme_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        sound_toggle_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)

        pygame.draw.rect(SCREEN, current_theme["button"], back_button)
        pygame.draw.rect(SCREEN, current_theme["button"], theme_button)
        pygame.draw.rect(SCREEN, current_theme["button"], sound_toggle_button)
        pygame.draw.rect(SCREEN, YELLOW, volume_slider_rect)

        draw_text("Back", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 525)
        draw_text("Theme", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 275)
        draw_text("Sound: ON" if sound_on else "Sound: OFF", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 375)


        pygame.draw.rect(SCREEN, WHITE, volume_slider_rect)
        pygame.draw.rect(SCREEN, YELLOW, volume_slider)
        draw_text(f"Volume: {volume_level}%", button_font, current_theme["text"], SCREEN, SCREEN_WIDTH // 2, 475)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                if theme_button.collidepoint(event.pos):
                    theme_index = (theme_index + 1) % len(THEMES)
                    current_theme = THEMES[theme_index]
                if sound_toggle_button.collidepoint(event.pos):
                    sound_on = not sound_on 
                    if not sound_on:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(volume_level / 100)
                        
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and volume_slider_rect.collidepoint(event.pos):
                    volume_level = (event.pos[0] - volume_slider_rect.left) // 2
                    volume_level = max(0, min(volume_level, 100))
                    volume_slider.x = volume_slider_rect.left + (volume_level * 2)
                    pygame.mixer.music.set_volume(volume_level / 100)

        pygame.display.flip()


'''
GAME FUNC
'''

# GENERATE NEW CHARACTER
def get_new_character():
    return Player(PLAYER_POSITION[0], PLAYER_POSITION[1])


# GENERATE RANDOM COIN POSITION
def random_coin_pos():
    return [random.randint(0, SCREEN_WIDTH - COIN_SIZE), random.randint(0, SCREEN_HEIGHT - COIN_SIZE)]


# DRAW HUD
def draw_hud():
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f"HP: {HP}", True, BLACK)
    points_text = font.render(f"Score: {POINTS}", True, WHITE)
    SCREEN.blit(hp_text, (10, 10))
    SCREEN.blit(points_text, (10, 50))

# MINIHRA 1
def scissors_tile(square_x, square_y):
    message = "Scissors"
    pygame.draw.rect(SCREEN, TILE_COLOR, (square_x, square_y, TILE_SIZE, TILE_SIZE))
    text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
    text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
    SCREEN.blit(text_obj, text_rect)


def rock_tile(square_x, square_y):
    square_x = (SCREEN_WIDTH - TILE_SIZE) / 2 - TILE_SIZE - 10
    message = "Rock"
    pygame.draw.rect(SCREEN, TILE_COLOR, (square_x, square_y, TILE_SIZE, TILE_SIZE))
    text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
    text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
    SCREEN.blit(text_obj, text_rect)


def paper_tile(square_x, square_y):
    square_x = (SCREEN_WIDTH - TILE_SIZE) / 2 + TILE_SIZE + 10
    message = "Paper"
    pygame.draw.rect(SCREEN, TILE_COLOR, (square_x, square_y, TILE_SIZE, TILE_SIZE))
    text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
    text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
    SCREEN.blit(text_obj, text_rect)


def game(square_x, square_y):
    scissors_tile(square_x, square_y)
    rock_tile(square_x, square_y)
    paper_tile(square_x, square_y)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def mouse_click(square_x, square_y):
    global Last_click, result
    if pygame.mouse.get_pressed()[0] and Last_click == False:
        pos = pygame.mouse.get_pos()
        pick = check_boxes(pos[0], pos[1], square_x, square_y)
        if pick != None:
            enemy_pick = ["Rock", "Scissors", "Paper"][random.randint(1, 3) - 1]
            SCREEN.fill((0, 0, 0))
            if pick == enemy_pick:
                message = "It's a tie"
                text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                SCREEN.blit(text_obj, text_rect)
                result = "Tie"
                return result
            elif (pick == "Rock" and enemy_pick == "Paper") or (pick == "Paper" and enemy_pick == "Scissors") or (pick == "Scissors" and enemy_pick ==  "Rock"):
                message = "You won"
                text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                SCREEN.blit(text_obj, text_rect)
                result = True
                return result
            elif (pick == "Rock" and enemy_pick == "Scissors") or (pick == "Paper" and enemy_pick == "Rock") or (pick == "Scissors" and enemy_pick ==  "Paper"):
                message = "You lose"
                text_obj = BASIC_FONT.render(message, True, TEXT_COLOR)
                text_rect = text_obj.get_rect(center=(square_x + TILE_SIZE / 2, square_y + TILE_SIZE / 2))
                SCREEN.blit(text_obj, text_rect)
                result = False
                return result
            pygame.display.update()
            pygame.time.delay(1000)
    Last_click = pygame.mouse.get_pressed()[0]


def check_boxes(mouse_x, mouse_y, square_x, square_y):
    global TILE_SIZE
    rock_left = (SCREEN_WIDTH - TILE_SIZE) / 2 - TILE_SIZE - 10
    rock_right = (SCREEN_WIDTH - TILE_SIZE) / 2 - 10
    scissors_left = (SCREEN_WIDTH - TILE_SIZE) / 2
    scissors_right = (SCREEN_WIDTH - TILE_SIZE) / 2 + TILE_SIZE
    paper_left = (SCREEN_WIDTH - TILE_SIZE) / 2 + TILE_SIZE + 10
    paper_right = (SCREEN_WIDTH - TILE_SIZE) / 2 + 2 * TILE_SIZE + 10
    tile_top = (SCREEN_HEIGHT - TILE_SIZE) / 2
    tile_bottom = (SCREEN_HEIGHT - TILE_SIZE) / 2 + TILE_SIZE

    if rock_left <= mouse_x <= rock_right and tile_top <= mouse_y <= tile_bottom:
        return "Rock"
    if scissors_left <= mouse_x <= scissors_right and tile_top <= mouse_y <= tile_bottom:
        return "Scissors"
    if paper_left <= mouse_x <= paper_right and tile_top <= mouse_y <= tile_bottom:
        return "Paper"
    return None


def mini_game_1():
    global SCREEN, BASIC_FONT, result, clock
    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('CAT Your Paycheck!')

    square_x = (SCREEN_WIDTH - TILE_SIZE) / 2
    square_y = (SCREEN_HEIGHT - TILE_SIZE) / 2
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()

        game(square_x, square_y) 
        mouse_click(square_x, square_y)
        if result is not None:
            running = False
        pygame.display.update()
    return result


'''
GAME LOOP
'''

def run_game():
    global POINTS, HP, result
    clock = pygame.time.Clock()
    player = Player(PLAYER_POSITION[0], PLAYER_POSITION[1])
    coin = Coin(*random_coin_pos())

    all_sprites = pygame.sprite.Group(player, coin)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                end_game()
        keys = pygame.key.get_pressed()
        player.move(keys, SCREEN.get_rect())

        if pygame.sprite.collide_rect(player, coin):
            pygame.mixer.music.load("coin_sound.mp3")
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(0.5)
            if coin.special:
                mini_game_1()
                if result == True:
                    POINTS += 5
                elif result == False:
                    HP -= 1
                    if HP == 0:
                        end_game()
                        print("TY CHUJ")
                else:
                    pass
                result = None
            else:
                POINTS += 1
            coin.rect.topleft = random_coin_pos()
            coin.toggle_special()
        background = pygame.image.load("background.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.blit(background, (0, 0))
        draw_hud()
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

    end_game()


if __name__ == "__main__":
    if main_menu():
        main()
