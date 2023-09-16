# Игра Shmup - 1 часть
# Cпрайт игрока и управление
import pygame
import random
import os

WIDTH = 1200
HEIGHT = 720
FPS = 60
SPEED = 1

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
player_img = pygame.image.load(os.path.join(img_folder, 'sprites/mario_thumb.png')).convert()
background = pygame.image.load(
    os.path.join(img_folder, "map_directory/g30_w25_m25_s(10, 10)_t1694640220/map_1694640219.jpeg")).convert()

# TODO: активно в окне сделать показ только одного биома

class Camera:
    def __init__(self, x, y):
        self.image = player_img
        self.rect = pygame.Rect(x, y, 500, 500)

    def move(self, vector_list):
        # left
        if vector_list[0] < 0:
            temp = self.rect[0] + (vector_list[0] - 40)
            if temp >= -230:
                self.rect[0] = temp
            else:
                self.rect[0] -= vector_list[0] * 2
        if vector_list[0] > 0:
            temp = self.rect[0] + (vector_list[0] + 40)
            if temp >= -230:
                self.rect[0] = temp
            else:
                self.rect[0] -= vector_list[0] * 2
        # top
        if vector_list[1] < 0:
            temp = self.rect[1] + (vector_list[1] - 40)
            if temp >= -230:
                self.rect[1] = temp
            else:
                self.rect[1] -= vector_list[1] * 2
        if vector_list[1] > 0:
            temp = self.rect[1] + (vector_list[1] + 40)
            if temp >= -230:
                self.rect[1] = temp
            else:
                self.rect[1] -= vector_list[1] * 2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # self.rect.centerx = 0
        # self.rect.bottom = 0

    def get_rect_x(self) -> int:
        return self.rect.x

    def get_rect_y(self) -> int:
        return self.rect.y

    def move(self, vector_list: list):
        self.rect.x += vector_list[0]
        if self.rect.y >= -230:
            self.rect.y += vector_list[1]
        else:
            self.rect.y -= vector_list[1] * 2
    #
    # def draw(self):
    #     # Игрок на самом окне не двигается, двигается мир вокруг него
    #     pygame.draw.rect(screen, (150, 0, 0), (240, 240, 10, 10))


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
camera = Camera(0, 0)

# Цикл игры
running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    vector = [0, 0]
    keystate = pygame.key.get_pressed()
    mousestate = pygame.mouse.get_pressed()
    if mousestate[0]:
        x, y = pygame.mouse.get_pos()
        vector[0] = int((x - player.get_rect_x()) / (SPEED * 64))
        vector[1] = int((y - player.get_rect_y()) / (SPEED * 64))
    if mousestate[1]:
        print("property1")
    if mousestate[2]:
        # fast move
        x, y = pygame.mouse.get_pos()
        vector[0] = int((x - player.get_rect_x()) / (SPEED * 32))
        vector[1] = int((y - player.get_rect_y()) / (SPEED * 32))
    if keystate[pygame.K_LEFT]:
        vector[0] = -SPEED
    if keystate[pygame.K_RIGHT]:
        vector[0] = SPEED
    if keystate[pygame.K_DOWN]:
        vector[1] = SPEED
    if keystate[pygame.K_UP]:
        vector[1] = -SPEED

    # Обновление
    if vector != [0, 0]:
        sprite = all_sprites.sprites()
        if sprite:
            all_sprites.remove_internal(sprite[0])
            sprite[0].move(vector)
            all_sprites.add(sprite[0])
        camera.move(vector)

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, (-camera.rect[0], -camera.rect[1]))
    all_sprites.draw(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
