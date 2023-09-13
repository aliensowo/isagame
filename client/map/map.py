import random
import time
from typing import Dict

from client.map.map_error import MapGenerateError, SymbolAssociationError
from map_types import SymbolAssociation, WoodAssociation, StoneAssociation, FishAssociation
from resources_weights import MapBioWeights, WoodWeights, StoneWeights, FishWeights
from PIL import Image


class Map:
    _mask: list[list]
    _mask_size: tuple = (255, 255)
    _texture_size = 16
    _map: str

    def __init__(self):
        self._map = f"map_{int(time.time())}.jpeg"
        self._generate_mask()

    def _generate_mask(self):
        self._mask = [[None for _ in range(self._mask_size[0])] for _ in range(self._mask_size[1])]
        self._mask[0][0] = "_"

    def get_map(self):
        return self._map

    def generate_map(self):
        map_image = Image.new(
            "RGB",
            (self._mask_size[0] * self._texture_size, self._mask_size[1] * self._texture_size),
            "white",
        )
        for y_axis in range(len(self._mask)):
            for x_axis in range(len(self._mask[y_axis])):
                green_boost, water_boost, mountain_boost = (0, 0, 0)
                try:
                    left_point = self._mask[y_axis][x_axis - 1]
                    green_boost, water_boost, mountain_boost = self._default_boost_values(
                        point=left_point,
                        boost={"green_boost": green_boost, "water_boost": water_boost, "mountain_boost": mountain_boost}
                    )
                except IndexError:
                    pass
                try:
                    up_point = self._mask[y_axis - 1][x_axis]
                    green_boost, water_boost, mountain_boost = self._default_boost_values(
                        point=up_point,
                        boost={"green_boost": green_boost, "water_boost": water_boost, "mountain_boost": mountain_boost}
                    )
                except IndexError:
                    pass
                curr_point = random.choices(
                    [SymbolAssociation.water, SymbolAssociation.green, SymbolAssociation.mountain],
                    weights=[
                        MapBioWeights.water + water_boost,
                        MapBioWeights.green + green_boost,
                        MapBioWeights.mountain + mountain_boost,
                    ],
                )[0]
                paste_image = self._generate_element(curr_point=curr_point)
                map_image.paste(paste_image, (x_axis * self._texture_size, y_axis * self._texture_size))

                self._mask[y_axis][x_axis] = curr_point
        map_image.save(f"../images/map_directory/g{MapBioWeights.green}_w{MapBioWeights.water}_m{MapBioWeights.mountain}_{self._map}")

    def _generate_element(self, curr_point: str) -> Image:
        if curr_point == SymbolAssociation.green:
            # generate wood
            paste_image = self._generate_green()
        elif curr_point == SymbolAssociation.water:
            # generate fish
            paste_image = self._generate_fish()
        elif curr_point == SymbolAssociation.mountain:
            # TODO: generate stone
            paste_image = self._generate_stone()
        else:
            raise MapGenerateError
        return paste_image

    @staticmethod
    def _default_boost_values(point: str, boost: Dict) -> tuple:
        """ boost = {"green_boost": cur_value, ... }"""
        if point == SymbolAssociation.green:
            green_boost, water_boost, mountain_boost = 20, -15, -15
        elif point == SymbolAssociation.water:
            green_boost, water_boost, mountain_boost = -15, 20, -15
        elif point == SymbolAssociation.mountain:
            green_boost, water_boost, mountain_boost = -15, -15, 20
        elif point is None:
            green_boost, water_boost, mountain_boost = 0, 0, 0
        else:
            raise SymbolAssociationError
        green_boost = boost["green_boost"] + green_boost
        water_boost = boost["water_boost"] + water_boost
        mountain_boost = boost["mountain_boost"] + mountain_boost
        return green_boost, water_boost, mountain_boost

    @staticmethod
    def _generate_green() -> Image:
        resource = random.choices(
            [WoodAssociation.wood, WoodAssociation.none],
            weights=[WoodWeights.wood, WoodWeights.none]
        )[0]
        paste_image = Image.open("../images/used_bios/green16x16.jpg")
        if resource:
            resource_image = Image.open("../images/used_resources/wood4x4.png")
            count = random.randint(1, 4)
            for wood_number in range(count):
                paste_image.paste(
                    resource_image,
                    (random.randint(1, 14), random.randint(1, 14))
                )
        return paste_image

    @staticmethod
    def _generate_fish() -> Image:
        resource = random.choices(
            [FishAssociation.fish, FishAssociation.none],
            weights=[FishWeights.fish, WoodWeights.none]
        )[0]
        paste_image = Image.open("../images/used_bios/water16x16.jpg")
        if resource:
            resource_image = Image.open("../images/used_resources/fish4x4.png")
            count = random.randint(1, 4)
            for fish_number in range(count):
                paste_image.paste(
                    resource_image,
                    (random.randint(1, 14), random.randint(1, 14))
                )
        return paste_image

    @staticmethod
    def _generate_stone() -> Image:
        paste_image = Image.open("../images/used_bios/mountain16x16.jpg")
        return paste_image


if __name__ == '__main__':
    mapp = Map()
    mapp.generate_map()
    mmaapp = mapp.get_map()
    # for row in mmaapp:
    #     print(row)
