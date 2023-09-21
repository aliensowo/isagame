import pygame as pg
from client.class_inventory.inventory import Inventory
from client.class_user.user import User
from client.class_coin.coin import Coin


class GameProperty:
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
    bag: pg.Surface
    bag_img: pg.Surface
