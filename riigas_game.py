import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rīga Nākotnē")
icon = pygame.image.load('pygame/logo.png')
pygame.display.set_icon(icon)
# Load music
pygame.mixer.music.load("pygame/music.mp3")
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Player options
player_options = ["pygame/meitene.png", "pygme/men.png"]
selected_player = 0

# Player
player_img = pygame.image.load(player_options[selected_player])
player_rect = player_img.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 10
player_speed = 5

# Coin
coin_img = pygame.image.load("pygame/coin.png")
coin_rect = coin_img.get_rect()
coin_rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
coin_collected = False

# Homes
homes = [
    {"cost": 15, "img": pygame.image.load("pygame/daudzstāvene.png"), "rect": pygame.Rect(50, 50, 100, 100)},
    {"cost": 20, "img": pygame.image.load("pygame/māja.png"), "rect": pygame.Rect(200, 200, 100, 100)},
    {"cost": 30, "img": pygame.image.load("pygame/banka.png"), "rect": pygame.Rect(400, 100, 100, 100)},
    {"cost": 10, "img": pygame.image.load("pygame/garāža.png"), "rect": pygame.Rect(50, 50, 100, 100)},
    {"cost": 25, "img": pygame.image.load("pygame/maiznīca.png"), "rect": pygame.Rect(50, 50, 100, 100)},
    {"cost": 20, "img": pygame.image.load("pygame/panorāmas_rats.png"), "rect": pygame.Rect(400, 100, 100, 100)},
    {"cost": 10, "img": pygame.image.load("pygame/parks.png"), "rect": pygame.Rect(50, 50, 100, 100)},
    {"cost": 20, "img": pygame.image.load("pygame/skola.png"), "rect": pygame.Rect(200, 200, 100, 100)},
    {"cost": 20, "img": pygame.image.load("pygame/slimnīca.png"), "rect": pygame.Rect(200, 200, 100, 100)}
]
current_home = None

# Function to save game progress
def save_progress():
    progress = {
        "player_rect": {"x": player_rect.x, "y": player_rect.y},
        "coin_collected": coin_collected,
        "selected_player": selected_player
    }
    with open("progress.json", "w") as f:
        json.dump(progress, f)

# Function to load game progress
def load_progress():
    try:
        with open("progress.json", "r") as f:
            progress = json.load(f)
        return (
            pygame.Rect(progress["player_rect"]["x"], progress["player_rect"]["y"], 50, 50),
            progress["coin_collected"],
            progress["selected_player"]
        )
    except FileNotFoundError:
        return None, False, 0

# Load progress at the beginning
player_rect, coin_collected, selected_player = load_progress()

# Main loop
running = True
menu = True
while running:
    if menu:
        # Code for the menu...
        pass
    else:
        screen.fill(WHITE)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_progress()

        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # Check if player collects the coin
        if player_rect.colliderect(coin_rect):
            coin_collected = True
            coin_rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

        # Draw coin
        screen.blit(coin_img, coin_rect)

        # Draw player
        screen.blit(player_img, player_rect)

        # Draw homes and check if player can buy
        for home in homes:
            screen.blit(home["img"], home["rect"])
            if player_rect.colliderect(home["rect"]) and coin_collected:
                current_home = home
                break

        # Display current home info
        if current_home:
            text_surface = font.render(f"Press 'B' to buy for {current_home['cost']} coins", True, BLUE)
            screen.blit(text_surface, (10, 10))

            if keys[pygame.K_b]:
                # Implement buying logic here
                coin_collected = False
                current_home = None

        pygame.display.flip()

pygame.quit()