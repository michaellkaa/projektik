import pygame
import random
import sys
from pygame.locals import *

# SYSTEM
FPS = 60
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# COLORS
RED = (255, 0, 0)
GREEN = (0, 153, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (183,104,162)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 51, 153)

BG_COLOR = PURPLE
COIN_COLOR = YELLOW
COIN_SIZE = 30
CASH_COLOR = GREEN

# CHARACTER
CHARACTER_COLOR = BLACK
CHARACTER_SIZE = 100
PLAYER_SPEED = 12
PLAYER_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
HP = 3
POINTS = 0


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
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('CAT Your Paycheck!')

    POINTS = 0
    while True:
        run_game()
        game_over_screen()


# END GAME
def end_game():
    pygame.quit()
    sys.exit()


# GAME OVER SCREEN - placeholder
def game_over_screen():
    pass


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


'''
GAME LOOP
'''

def run_game():
    global POINTS
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
            POINTS += 5 if coin.special else 1
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
    main()
