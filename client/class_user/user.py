import warnings
import math
from typing import Tuple

import pygame as pg
from client.settings import *


warnings.filterwarnings("ignore")


class User(pg.sprite.Sprite):
    _speed = 5
    _power = 1
    _level = 0

    # pygame methods
    def __init__(self, game, hp, prot, atk):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.image = pg.image.load(os.path.join(images_dir, "sprites/mario_thumb.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2
        self.speedx = 0
        self.speedy = 0

        # Player attr
        self.hp = hp
        self.prot = prot
        self.hp_max = hp
        self.atk = atk
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
        self.weapon = None
        self.p_coins = 0

    def update(self, in_turn_flag, in_curr_node) -> Tuple:
        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -8
        elif keystate[pg.K_RIGHT]:
            self.speedx = 8
        elif keystate[pg.K_UP]:
            self.speedy = -8
        elif keystate[pg.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            if math.ceil(in_curr_node / 50) < 49:
                in_turn_flag = True
                in_curr_node += 1
                self.rect.right = 60
            else:
                self.rect.right = WIDTH
        elif self.rect.left < 0:
            if math.ceil(in_curr_node / 50) > 0:
                in_turn_flag = True
                in_curr_node -= 1
                self.rect.left = WIDTH - 60
            else:
                self.rect.left = 0
        elif self.rect.top < 0:
            if math.ceil(in_curr_node / 50) > 0:
                in_turn_flag = True
                in_curr_node -= 50
                self.rect.top = HEIGHT - 50
            else:
                self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            if math.ceil(in_curr_node / 50) < 50:
                in_turn_flag = True
                in_curr_node += 50
                self.rect.top = 50
            else:
                self.rect.bottom = HEIGHT

        self.check_collision()
        return in_turn_flag, in_curr_node

    def add_hp(self, hp_gain):
        self.hp += hp_gain
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def add_prot(self, prot_gain):
        self.prot += prot_gain

    def equip_armor(self, item):
        if self.armor[item.slot] is not None:
            self.un_equip_armor(item.slot)
        self.armor[item.slot] = item
        self.prot += item.prot

    def un_equip_armor(self, slot):
        if self.armor[slot] is not None:
            self.prot -= self.armor[slot].prot
            self.armor[slot] = None

    def equip_weapon(self, weapon):
        if self.weapon is not None:
            self.un_equip_weapon()
        self.weapon = weapon
        self.atk += weapon.atk

    def un_equip_weapon(self):
        if self.weapon is not None:
            self.atk -= self.weapon.atk
            self.weapon = None

    def check_collision(self):
        self.check_coin()

    def check_coin(self):
        if (
                self.game.coin.rect.x in range(self.rect.x-10, self.rect.x+10)
        ) and (
                self.game.coin.rect.y in range(self.rect.y-10, self.rect.y+10)
        ):
            self.add_coin()
            self.game.new_coin()

    def add_coin(self):
        self.p_coins += 10
