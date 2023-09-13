from typing import DefaultDict


class MapBioWeights(DefaultDict):
    green = 30
    water = 25
    mountain = 25


class WoodWeights(DefaultDict):
    wood = 25
    none = 75


class StoneWeights(DefaultDict):
    stone = 25
    none = 75


class FishWeights(DefaultDict):
    fish = 15
    none = 85
