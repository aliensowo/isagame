from typing import DefaultDict, List


class MapBioWeights(DefaultDict):
    green = 30
    water = 25
    mountain = 25


class WoodWeights(DefaultDict):
    wood = 25
    none = 75

    @staticmethod
    def values() -> List:
        return [25, 75]


class StoneWeights(DefaultDict):
    stone = 25
    none = 75


class FishWeights(DefaultDict):
    fish = 15
    none = 85

    @staticmethod
    def values() -> List:
        return [15, 85]
