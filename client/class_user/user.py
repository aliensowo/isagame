import os
import math
from typing import Tuple

import pygame
from server.errors.errors_user import InventoryFullError, InventoryElementNotEnough
from client.settings import (
    images_dir,
    WIDTH,
    HEIGHT,
)


class User(pygame.sprite.Sprite):
    _inventory_len = 25
    _inventory = {}
    _speed = 5
    _power = 1
    _level = 0

    # pygame methods
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(images_dir, "sprites/mario_thumb.png")).convert()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self, turn_flag, curr_node) -> Tuple:
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
        return turn_flag, curr_node

    # social methods
    def get_inventory(self):
        return self._inventory

    def put_to_inventory(self, element: str, count: int) -> bool:
        if element in self._inventory.keys():
            self._inventory[element] += count
        else:
            if len(self._inventory) < self._inventory_len:
                self._inventory[element] = count
            else:
                raise InventoryFullError
        return True

    def get_from_inventory(self, element: str, count: int):
        if element in self._inventory.keys():
            if self._inventory[element] >= count:
                self._inventory[element] -= count
                return {element: count}
        raise InventoryElementNotEnough

