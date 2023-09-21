import warnings
from typing import Tuple
import pygame


warnings.filterwarnings("ignore")


class Resources(pygame.sprite.Sprite):

    damage: int = 10

    def __init__(self, image, x, y, res_type, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = res_type
        self.size = size
        self.full_health: int = self.size
        self.healthcheck: int = self.size

    def callback(self):
        if self.healthcheck > self.damage:
            self.healthcheck -= self.damage
        else:
            self.healthcheck = 0

    def update(self, events, player_pos: Tuple):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if (
                        (0 < abs(self.rect.x - player_pos[0])) and (abs(self.rect.x - player_pos[0]) < 150)
                    ) and (
                        (0 < abs(self.rect.y - player_pos[1])) and (abs(self.rect.y - player_pos[1]) < 150)
                    ):
                        self.callback()
