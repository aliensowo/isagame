import warnings
import sys
import random
from typing import Tuple, Dict

import pygame as pg
from client.settings import *
from client.class_inventory.inventory import Inventory, Weapon, Armor, Consumable
from client.class_user.user import User
from client.class_coin.coin import Coin
from client.class_logic.logic import Logic
from client.class_resourse.resource import Resources


warnings.filterwarnings("ignore")


class Game:

    background: pg.Surface
    all_sprites: pg.sprite.Group
    all_coins: pg.sprite.Group
    resource_group: pg.sprite.Group
    player: User
    coin: Coin
    inventory: Inventory
    hp: pg.Surface
    prot: pg.Surface
    atk: pg.Surface
    coins: pg.Surface
    wood: pg.Surface
    hp_img: pg.Surface
    prot_img: pg.Surface
    atk_img: pg.Surface
    coin_img: pg.Surface
    wood_img: pg.Surface

    def __init__(self, new_map: bool = False):
        pg.init()
        pg.font.init()
        self.myfont = pg.font.SysFont('Calibri', 25)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.turn_flag = False
        self.curr_node = START_NODE
        if new_map:
            self.map_path = Logic.generate_map(max_size_map_bioms=(50, 50), biom_size=512, resources_size=32)
        else:
            self.map_path = Logic.get_random_map()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.resource_group = pg.sprite.Group()
        self.player = User(self, DEFUALT_HP, DEFUALT_PROT, DEFUALT_ATK)
        self.all_sprites.add(self.player)
        self.coin = Coin(self, random.randrange(*GRIDWIDTH), random.randrange(*GRIDHEIGHT))
        self.inventory = Inventory(self.player, 10, 5, 2)

        for staff in self.get_staff():
            self.inventory.add_item_inv(staff)
        self.run()

    @staticmethod
    def get_staff():
        return [
            Weapon(
                os.path.join(images_dir, 'sprites/sword.png'), 20, 20, 'weapon', 'sword',
            ),
            Weapon(
                os.path.join(images_dir, 'sprites/swordWood.png'), 10, 10, 'weapon', 'sword',
            ),
            Consumable(
                os.path.join(images_dir, 'sprites/potionRed.png'), 2, 30,
            ),
            Armor(
                os.path.join(images_dir, 'sprites/helmet.png'), 10, 20, 'head',
            ),
            Armor(
                os.path.join(images_dir, 'sprites/chest.png'), 10, 40, 'chest',
            ),
            Armor(
                os.path.join(images_dir, 'sprites/upg_helmet.png'), 10, 40, 'head',
            ),
            Armor(
                os.path.join(images_dir, 'sprites/upg_chest.png'), 10, 80, 'chest',
            ),
        ]

    def load_static(self, node: int = START_NODE) -> Tuple:
        return Logic.get_image(node, self.map_path)

    def run(self):
        self.draw_map_background()
        # game loop
        while True:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()

    def update(self):
        # game loop update
        self.turn_flag, self.curr_node = self.player.update(self.turn_flag, self.curr_node)
        if self.turn_flag:
            self.draw_map_background()
            self.new_coin()
        self.all_coins.update()

    def events(self):
        events = pg.event.get()
        for event in events:
            # check for closing window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and event.unicode == 'k':
                self.inventory.toggle_inventory()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                if self.inventory.display_inventory:
                    mouse_pos = pg.mouse.get_pos()
                    self.inventory.check_slot(self.screen, mouse_pos)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.inventory.display_inventory:
                    self.inventory.move_item(self.screen)
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.inventory.display_inventory:
                    self.inventory.place_item(self.screen)
        self.resource_group.update(events, (self.player.rect.x, self.player.rect.y))

    def render_resources(self, resources: Dict):
        self.resource_group = pg.sprite.Group()
        for res, res_value in resources.items():
            for rv in res_value:
                element = Resources(
                    image=rv["path"], x=rv["x_biom"], y=rv["y_biom"], res_type=rv["type"], size=rv["size"],
                )
                self.resource_group.add(element)
        self.turn_flag = False

    def draw_map_background(self):
        biom_image_path, resources = self.load_static(self.curr_node)
        self.background = pg.image.load(biom_image_path)
        self.render_resources(resources=resources)

    def grind_resources(self):
        for resource in self.resource_group.sprites():
            pg.draw.rect(
                self.screen, GREEN, [resource.rect.x, resource.rect.y, resource.healthcheck, 10]
            )
            delta_health = resource.full_health - resource.healthcheck
            pg.draw.rect(
                self.screen, RED, [resource.rect.x + resource.healthcheck, resource.rect.y, delta_health, 10]
            )
            if resource.healthcheck == 0:
                if resource.type == "wood":
                    self.player.add_wood()
                self.resource_group.remove(resource)

    def new_coin(self):
        self.coin.set_position(x=random.randrange(*GRIDWIDTH), y=random.randrange(*GRIDHEIGHT))

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self):
        biom_text = self.myfont.render(f'biom: {self.curr_node}', True, GREEN, BLUE)
        biom_text_obj = biom_text.get_rect()
        biom_text_obj.center = (HEIGHT - biom_text.get_size()[0], self.myfont.get_height())
        self.screen.blit(biom_text, biom_text_obj)

    def draw_player_stats(self):
        self.hp = self.myfont.render(f"{self.player.hp}", False, RED)
        self.prot = self.myfont.render(f"{self.player.prot}", False, WHITE)
        self.atk = self.myfont.render(f"{self.player.atk}", False, WHITE)
        self.coins = self.myfont.render(f"{self.player.p_coins}", False, GOLD)
        self.wood = self.myfont.render(f"{self.player.wood}", False, GOLD)
        self.bag = self.myfont.render(f"K", False, RED)
        self.hp_img = pg.image.load(os.path.join(images_dir, 'sprites/heart.png')).convert_alpha()
        self.prot_img = pg.image.load(os.path.join(images_dir, 'sprites/upg_shieldSmall.png')).convert_alpha()
        self.atk_img = pg.image.load(os.path.join(images_dir, 'sprites/upg_dagger.png')).convert_alpha()
        self.coin_img = pg.image.load(os.path.join(images_dir, 'sprites/coin1.png')).convert_alpha()
        self.wood_img = pg.image.load(os.path.join(images_dir, 'sprites/wood.png')).convert_alpha()
        self.bag_img = pg.image.load(os.path.join(images_dir, 'sprites/bag.png')).convert_alpha()
        self.screen.blit(self.hp, (STATPOSX, 25))
        self.screen.blit(self.prot, (STATPOSX, 75))
        self.screen.blit(self.atk, (STATPOSX, 125))
        self.screen.blit(self.coins, (STATPOSX, 175))
        self.screen.blit(self.wood, (STATPOSX, 225))
        self.screen.blit(self.hp_img, (STATPOSX - 50, 5))
        self.screen.blit(self.prot_img, (STATPOSX - 50, 55))
        self.screen.blit(self.atk_img, (STATPOSX - 50, 105))
        self.screen.blit(self.coin_img, (STATPOSX - 55, 155))
        self.screen.blit(self.wood_img, (STATPOSX - 40, 215))
        self.screen.blit(self.bag_img, (STATPOSX - 40, HEIGHT - 50))
        self.screen.blit(self.bag, (STATPOSX - 40, HEIGHT - 50))

    def draw(self):
        # game loop draw
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, (0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.inventory.draw(self.screen)
        self.resource_group.draw(self.screen)
        self.draw_player_stats()
        self.draw_text()
        # flipping display after drawing
        self.grind_resources()
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    @staticmethod
    def quit():
        sys.exit()
