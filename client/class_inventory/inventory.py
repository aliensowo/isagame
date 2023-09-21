import warnings
import pygame as pg
from client.settings import *


warnings.filterwarnings("ignore")


class Inventory:
    def __init__(self, player, totalSlots, cols, rows):
        self.totalSlots = totalSlots
        self.rows = rows
        self.cols = cols
        self.inventory_slots = []
        self.armor_slots = []
        self.weapon_slots = []
        self.display_inventory = False
        self.player = player
        self.appendSlots()
        self.set_slot_types()

        self.movingitem = None
        self.movingitemslot = None

    def appendSlots(self):
        while len(self.inventory_slots) != self.totalSlots:
            for x in range(
                    WIDTH // 2 - ((INVTILESIZE + 2) * self.cols) // 2,
                    WIDTH // 2 + ((INVTILESIZE + 2) * self.cols) // 2, INVTILESIZE + 2
            ):
                for y in range(
                        UIHEIGTH,
                        UIHEIGTH + INVTILESIZE * self.rows,
                        INVTILESIZE + 2
                ):
                    self.inventory_slots.append(InventorySlot(x, y))

        while len(self.armor_slots) != 4:
            for y in range(UIHEIGTH - 100, UIHEIGTH - 100 + (INVTILESIZE + 1) * 4, INVTILESIZE + 2):
                self.armor_slots.append(EquipableSlot(self.inventory_slots[0].x - 100, y))

        while len(self.weapon_slots) != 1:
            self.weapon_slots.append(EquipableSlot(self.armor_slots[3].x - 50, self.armor_slots[3].y))

    def set_slot_types(self):
        self.armor_slots[0].slottype = 'head'
        self.armor_slots[1].slottype = 'chest'
        self.armor_slots[2].slottype = 'legs'
        self.armor_slots[3].slottype = 'feet'
        self.weapon_slots[0].slottype = 'weapon'

    def draw(self, screen):
        if self.display_inventory:
            for slot in self.armor_slots + self.inventory_slots + self.weapon_slots:
                slot.draw(screen)
            for slot in self.armor_slots + self.inventory_slots + self.weapon_slots:
                slot.draw_items(screen)

    def toggle_inventory(self):
        self.display_inventory = not self.display_inventory

    def add_item_inv(self, item, slot=None):
        if slot is None:
            for slots in self.inventory_slots:
                if slots.item is None:
                    slots.item = item
                    break
        if slot is not None:
            if slot.item is not None:
                self.movingitemslot.item = slot.item
                slot.item = item
            else:
                slot.item = item

    def remove_item_inv(self, item):
        for slot in self.inventory_slots:
            if slot.item == item:
                slot.item = None
                break

    def move_item(self, screen):
        mousepos = pg.mouse.get_pos()
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if slot.draw(screen).collidepoint(mousepos) and slot.item is not None:
                slot.item.is_moving = True
                self.movingitem = slot.item
                self.movingitemslot = slot
                break

    def place_item(self, screen):
        mousepos = pg.mouse.get_pos()
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if slot.draw(screen).collidepoint(mousepos) and self.movingitem is not None:
                if (
                        isinstance(self.movingitemslot, EquipableSlot)
                ) and (
                        isinstance(slot, InventorySlot)
                ) and (
                        not isinstance(slot, EquipableSlot)
                ) and (
                        slot.item is None
                ):
                    self.un_equip_item(self.movingitem)
                    break
                if (
                        isinstance(slot, InventorySlot)
                ) and (
                        not isinstance(slot, EquipableSlot)
                ) and (
                        not isinstance(self.movingitemslot, EquipableSlot)
                ):
                    self.remove_item_inv(self.movingitem)
                    self.add_item_inv(self.movingitem, slot)
                    break
                if isinstance(self.movingitemslot, EquipableSlot) and isinstance(slot.item, Equipable):
                    if self.movingitem.slot == slot.item.slot:
                        self.un_equip_item(self.movingitem)
                        self.equip_item(slot.item)
                        break
                if isinstance(slot, EquipableSlot) and isinstance(self.movingitem, Equipable):
                    if slot.slottype == self.movingitem.slot:
                        self.equip_item(self.movingitem)
                        break
        if self.movingitem is not None:
            self.movingitem.is_moving = False
            self.movingitem = None
            self.movingitemslot = None

    def check_slot(self, screen, mousepos):
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if isinstance(slot, InventorySlot):
                if slot.draw(screen).collidepoint(mousepos):
                    if isinstance(slot.item, Equipable):
                        self.equip_item(slot.item)
                    if isinstance(slot.item, Consumable):
                        self.use_item(slot.item)
            if isinstance(slot, EquipableSlot):
                if slot.draw(screen).collidepoint(mousepos):
                    if slot.item is not None:
                        self.un_equip_item(slot.item)

    def get_equip_slot(self, item):
        for slot in self.armor_slots + self.weapon_slots:
            if slot.slottype == item.slot:
                return slot

    def use_item(self, item):
        if isinstance(item, Consumable):
            item.use(self, self.player)

    def equip_item(self, item):
        if isinstance(item, Equipable):
            item.equip(self, self.player)

    def un_equip_item(self, item):
        if isinstance(item, Equipable):
            item.un_equip(self)


class InventorySlot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None

    def draw(self, screen):
        return pg.draw.rect(screen, WHITE, (self.x+50, self.y+70, INVTILESIZE, INVTILESIZE))

    def draw_items(self, screen):
        if self.item is not None and not self.item.is_moving:
            self.image = pg.image.load(self.item.img).convert_alpha()
            screen.blit(self.image, (self.x - 7 + 50, self.y - 7 + 70))
        if self.item is not None and self.item.is_moving:
            mousepos1 = pg.mouse.get_pos()
            self.image = pg.image.load(self.item.img).convert_alpha()
            screen.blit(self.image, (mousepos1[0] - 20, mousepos1[1] - 20))


class EquipableSlot(InventorySlot):
    def __init__(self, x, y, slottype=None):
        InventorySlot.__init__(self, x, y)
        self.slottype = slottype


class InventoryItem:
    def __init__(self, img, value):
        self.img = img
        self.value = value
        self.is_moving = False


class Consumable(InventoryItem):
    def __init__(self, img, value, hp_gain=0, prot_gain=0):
        InventoryItem.__init__(self, img, value)
        self.hp_gain = hp_gain
        self.prot_gain = prot_gain

    def use(self, inv, target):
        inv.remove_item_inv(self)
        target.add_hp(self.hp_gain)
        target.add_prot(self.prot_gain)


class Equipable(InventoryItem):
    def __init__(self, img, value):
        InventoryItem.__init__(self, img, value)
        self.is_equipped = False
        self.equipped_to = None

    def equip(self, target):
        self.is_equipped = True
        self.equipped_to = target

    def un_equip(self, *args, **kwargs):
        self.is_equipped = False
        self.equipped_to = None


class Armor(Equipable):
    def __init__(self, img, value, prot, slot):
        Equipable.__init__(self, img, value)
        self.prot = prot
        self.slot = slot

    def equip(self, inv, target):
        if inv.get_equip_slot(self).item is not None:
            inv.get_equip_slot(self).item.un_equip(inv)
        Equipable.equip(self, target)
        target.equip_armor(self)
        inv.remove_item_inv(self)
        inv.get_equip_slot(self).item = self

    def un_equip(self, inv):
        self.equipped_to.un_equip_armor(self.slot)
        Equipable.un_equip(self)
        inv.add_item_inv(self)
        inv.get_equip_slot(self).item = None


class Weapon(Equipable):
    def __init__(self, img, value, atk, slot, wpn_type):
        Equipable.__init__(self, img, value)
        self.atk = atk
        self.slot = slot
        self.wpn_type = wpn_type

    def equip(self, inv, target):
        if inv.get_equip_slot(self).item is not None:
            inv.get_equip_slot(self).item.un_equip(inv)
        Equipable.equip(self, target)
        target.equip_weapon(self)
        inv.remove_item_inv(self)
        inv.get_equip_slot(self).item = self

    def un_equip(self, inv):
        self.equipped_to.un_equip_weapon()
        Equipable.un_equip(self)
        inv.add_item_inv(self)
        inv.get_equip_slot(self).item = None
