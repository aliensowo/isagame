import pygame


class Resources(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
