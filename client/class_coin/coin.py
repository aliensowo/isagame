import warnings
import pygame as pg
from client.settings import *


warnings.filterwarnings("ignore")


class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(images_dir, 'sprites/coin.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y