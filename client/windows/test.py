# Pygame шаблон - скелет для нового проекта Pygame
import math
import pygame
from utils import get_image
import random

WIDTH = 512
HEIGHT = 512
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        global turn_flag
        global curr_node
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 8
        elif keystate[pygame.K_UP]:
            self.speedy = -8
        elif keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            if math.ceil(curr_node / 50) < 49:
                turn_flag = True
                curr_node += 1
                self.rect.right = 60
            else:
                self.rect.right = WIDTH
        elif self.rect.left < 0:
            if math.ceil(curr_node / 50) > 0:
                turn_flag = True
                curr_node -= 1
                self.rect.left = WIDTH - 60
            else:
                self.rect.left = 0
        elif self.rect.top < 0:
            if math.ceil(curr_node/50) > 0:
                turn_flag = True
                curr_node -= 50
                self.rect.top = HEIGHT - 50
            else:
                self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            if math.ceil(curr_node / 50) < 50:
                turn_flag = True
                curr_node += 50
                self.rect.top = 50
            else:
                self.rect.bottom = HEIGHT


# globals
turn_flag = False
curr_node = 0
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
background = pygame.image.load(get_image(curr_node))

font = pygame.font.Font('freesansbold.ttf', 32)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # Рендеринг
    screen.fill(BLACK)

    if turn_flag:
        background = pygame.image.load(get_image(curr_node))
        turn_flag = False
    screen.blit(background, (0, 0))

    # curr
    text = font.render(f'{curr_node}', True, GREEN, BLUE)
    textRect = text.get_rect()
    textRect.center = (HEIGHT // 2, WIDTH // 2)
    screen.blit(text, textRect)

    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()