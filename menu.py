import pygame, sys, os, random
pygame.init()
pygame.mixer.init()

# SCREEN
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# ICONA MACICKY + SCREEN
icon = pygame.image.load("icon1.png")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MEOW")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_MODE_BG = (30, 30, 30)
LIGHT_MODE_BG = (255, 255, 255)
DARK_GREEN = (26, 26, 25)
YELLOW = (254, 236, 55)

THEMES = [
    {"bg": (162, 178, 159), "text": (248, 237, 227), "button": (121, 135, 119)},  # SVETLO ZELENA
    {"bg": (96, 153, 102), "text": (237, 241, 214), "button": (64, 81, 59)},  # TMAVO ZELENA
    {"bg": (232, 184, 109), "text": (245, 247, 248), "button": (250, 188, 63)},  # SVETLO ZLTA
    {"bg": (96, 139, 193), "text": (243, 243, 224), "button": (19, 62, 135)},  # TMAVO MODRA
    {"bg": (255, 180, 194), "text": (253, 255, 210), "button": (102, 123, 198)} # SVETLO RUZOVA
    ]

theme_index = 0
current_theme = THEMES[theme_index]


# HUDBA V MENU 
pygame.mixer.music.load("Meow.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

volume_level = 50  
sound_on = True

# TEXT A FONT
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)


# CASH V MENU
money_image = pygame.image.load("cash.png")
money_image = pygame.transform.scale(money_image, (50, 50))

falling_money = []

def spawn_money():
    x_pos = random.randint(0, SCREEN_WIDTH - 50)
    y_pos = -50
    speed = random.randint(1, 2) 
    falling_money.append({"x": x_pos, "y": y_pos, "speed": speed})
def update_money():
    for money in falling_money:
        money["y"] += money["speed"]
    falling_money[:] = [m for m in falling_money if m["y"] < SCREEN_HEIGHT]

# HLAVNE MENU
def main_menu():
    while True:
        # FARBA POZADIA
        screen.fill(current_theme["bg"])

        draw_text("!CAT YOUR PAYCHECK!", font, YELLOW, screen, SCREEN_WIDTH // 2, 195)

        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 550, 200, 50)

        pygame.draw.rect(screen, DARK_GREEN, start_button)
        pygame.draw.rect(screen, DARK_GREEN, settings_button)
        pygame.draw.rect(screen, DARK_GREEN, exit_button)

        draw_text("Start", button_font, current_theme["text"], screen, SCREEN_WIDTH // 2, 375)
        draw_text("Settings", button_font, current_theme["text"], screen, SCREEN_WIDTH // 2, 475)
        draw_text("Exit", button_font, current_theme["text"], screen, SCREEN_WIDTH // 2, 575)

        if pygame.time.get_ticks() % 60 == 0:
            spawn_money()

        update_money()
        for money in falling_money:
            screen.blit(money_image, (money["x"], money["y"]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("Start game!")
                    start_open()
                if settings_button.collidepoint(event.pos):
                    settings_menu()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()  
                    sys.exit()  

        pygame.display.flip()

# NASTAVENIA + START GAME + RIP CAT 
def start_open():
    os.execlp("python", "python", "game.py")

# RIP MACICKY V SETTINGS
rip_image = pygame.image.load("player_rip.png")  
rip_image = pygame.transform.scale(rip_image, (50, 50))  
falling_rip = []

def spawn_rip():
    x_pos = random.randint(0, SCREEN_WIDTH - 50)
    y_pos = -50
    speed = random.randint(1, 2)
    falling_rip.append({"x": x_pos, "y": y_pos, "speed": speed})
def update_rip():
    for rip in falling_rip:
        rip["y"] += rip["speed"]
    falling_rip[:] = [m for m in falling_rip if m["y"] < SCREEN_HEIGHT]
    
def settings_menu():
    global theme_index, current_theme, sound_on, volume_level
    volume_slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 440, 200, 20)
    volume_slider = pygame.Rect(SCREEN_WIDTH // 2 - 100 + (volume_level * 2), 440, 10, 20)
    
    while True:
        screen.fill(current_theme["bg"])

        draw_text("SETTINGS", font, current_theme["text"], screen, SCREEN_WIDTH // 2, 150)

        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 50)
        theme_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        sound_toggle_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)

        pygame.draw.rect(screen, current_theme["button"], back_button)
        pygame.draw.rect(screen, current_theme["button"], theme_button)
        pygame.draw.rect(screen, current_theme["button"], sound_toggle_button)
        pygame.draw.rect(screen, YELLOW, volume_slider_rect)

        draw_text("Back", button_font, current_theme["text"], screen, SCREEN_WIDTH // 2, 525)
        draw_text("Theme", button_font, current_theme["text"], screen, SCREEN_WIDTH // 2, 275)
        draw_text("Sound: ON" if sound_on else "Sound: OFF", button_font, current_theme["text"], screen, SCREEN_WIDTH // 2, 375)
        draw_text(f"Volume: {volume_level}%", button_font, current_theme["text"], screen, SCREEN_WIDTH // 2, 475)

        pygame.draw.rect(screen, WHITE, volume_slider_rect)
        pygame.draw.rect(screen, YELLOW, volume_slider)

        if pygame.time.get_ticks() % 60 == 0:
            spawn_rip()

        update_rip()
        for rip in falling_rip:
            screen.blit(rip_image, (rip["x"], rip["y"]))

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

# SPUSTENIE (FINALLY)
main_menu()
