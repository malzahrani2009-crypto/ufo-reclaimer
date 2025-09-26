"""
UFO Reclaimer - Polished Prototype
----------------------------------
Controls:
  - Arrow keys / WASD = Move
  - TAB = Transform (UFO <-> Robot)
  - SPACE = Fire laser (UFO mode)
  - M = Fire missile (unlocked later)
  - ESC = Quit
"""

import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UFO Reclaimer")

WHITE, BLACK, RED, GREEN, BLUE, YELLOW = (255,255,255),(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0)

# Load sounds
laser_snd = pygame.mixer.Sound("assets/sfx/laser.wav")
transform_snd = pygame.mixer.Sound("assets/sfx/transform.wav")
explosion_snd = pygame.mixer.Sound("assets/sfx/explosion.wav")
missile_snd = pygame.mixer.Sound("assets/sfx/missile.wav")

music_tracks = [
    "assets/music/desert_loop.wav",
    "assets/music/arctic_loop.wav",
    "assets/music/orbital_loop.wav",
]

class Player:
    def __init__(self):
        self.mode = "ufo"
        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)
        self.cooldown = 0
        self.hp = 100
        self.xp = 0

    def draw(self):
        if self.mode == "ufo":
            pygame.draw.ellipse(WIN, BLUE, self.rect)
        else:
            pygame.draw.rect(WIN, GREEN, self.rect)

    def transform(self):
        self.mode = "robot" if self.mode == "ufo" else "ufo"
        transform_snd.play()

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 30, 30)
    def draw(self):
        pygame.draw.rect(WIN, RED, self.rect)

class Projectile:
    def __init__(self, x, y, dx, dy, color=YELLOW, speed=8, size=6):
        self.rect = pygame.Rect(x, y, size, size)
        self.dx, self.dy, self.color, self.speed = dx, dy, color, speed
    def move(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)

clock = pygame.time.Clock()
player = Player()
enemies = [Enemy() for _ in range(5)]
projectiles = []
running = True

pygame.mixer.music.load(music_tracks[0])
pygame.mixer.music.play(-1)

while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]: player.rect.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player.rect.x += 5
    if keys[pygame.K_UP] or keys[pygame.K_w]: player.rect.y -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: player.rect.y += 5

    if keys[pygame.K_TAB]: player.transform()

    if keys[pygame.K_SPACE] and player.mode == "ufo":
        if player.cooldown <= 0:
            projectiles.append(Projectile(player.rect.centerx, player.rect.centery, 0, -1))
            laser_snd.play()
            player.cooldown = 15

    if player.cooldown > 0: player.cooldown -= 1

    for p in projectiles[:]:
        p.move()
        if not WIN.get_rect().colliderect(p.rect):
            projectiles.remove(p)

    for enemy in enemies[:]:
        for p in projectiles[:]:
            if enemy.rect.colliderect(p.rect):
                enemies.remove(enemy)
                projectiles.remove(p)
                explosion_snd.play()
                player.xp += 10
                break

    if len(enemies) < 5:
        enemies.append(Enemy())

    WIN.fill(BLACK)
    player.draw()
    for e in enemies: e.draw()
    for p in projectiles: p.draw()

    pygame.draw.rect(WIN, RED, (10, 10, player.hp*2, 20))
    pygame.draw.rect(WIN, BLUE, (10, 40, player.xp, 10))
    pygame.display.flip()

pygame.quit()
sys.exit()
