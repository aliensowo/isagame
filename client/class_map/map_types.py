from typing import DefaultDict, List


class SymbolAssociation(DefaultDict):
    green = "_"
    mountain = "^"
    water = "~"

    # get_keys = ["green", "mountain", "water"]
    @staticmethod
    def keys() -> List:
        return ["green", "mountain", "water"]


class WoodAssociation(DefaultDict):
    wood = "wood"
    none = None

    @staticmethod
    def keys() -> List:
        return ["wood", "none"]


class StoneAssociation(DefaultDict):
    stone = "stone"
    none = None


class FishAssociation(DefaultDict):
    fish = "fish"
    none = None

    @staticmethod
    def keys() -> List:
        return ["fish", "none"]
