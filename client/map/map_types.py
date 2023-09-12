from typing import DefaultDict


class SymbolAssociation(DefaultDict):
    green = "_"
    mountain = "^"
    water = "~"


class WoodAssociation(DefaultDict):
    wood = "wood"
    none = None


class StoneAssociation(DefaultDict):
    stone = "stone"
    none = None


class FishAssociation(DefaultDict):
    fish = "fish"
    none = None
