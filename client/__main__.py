# Pygame шаблон - скелет для нового проекта Pygame
import os
import math
from typing import List

import pygame
from client.class_logic.logic import Logic
from client.settings import (
    images_dir,
    WIDTH,
    HEIGHT,
    FPS,
    BLACK,
    GREEN,
    BLUE,
    curr_node,
    turn_flag
)
from client.class_user.user import User
from client.class_resourse.resource import Resources

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = User()
all_sprites.add(player)

# global param
global turn_flag
global curr_node

# prepare biom 0
biom_image_path, resources = Logic.get_image(curr_node)
background = pygame.image.load(biom_image_path)
for res, res_value in resources.items():
    m = Resources(image=res_value["path"], x=res_value["x_biom"], y=res_value["y_biom"])
    all_sprites.add(m)
    mobs.add(m)

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

    # Заливаем фон - нижний слой
    screen.fill(BLACK)

    # Обновление персонажа
    players_list = all_sprites.sprites()
    for p in players_list:
        if isinstance(p, User):
            turn_flag, curr_node = p.update(turn_flag, curr_node)

    # опредееляем картинку карты
    if turn_flag:
        biom_image_path, resources = Logic.get_image(curr_node)
        background = pygame.image.load(biom_image_path)
        for m in mobs:
            all_sprites.remove_internal(m)
        mobs = pygame.sprite.Group()
        for res, res_value in resources.items():
            m = Resources(image=res_value["path"], x=res_value["x_biom"], y=res_value["y_biom"])
            all_sprites.add(m)
            mobs.add(m)
        turn_flag = False
    screen.blit(background, (0, 0))

    # Выставляем номер биома
    text = font.render(f'{curr_node}', True, GREEN, BLUE)
    textRect = text.get_rect()
    textRect.center = (font.get_height(), font.get_height())
    screen.blit(text, textRect)

    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()