import random
import time
from typing import Dict
import os

from client.map.map_error import MapGenerateError, SymbolAssociationError
from client.map.map_types import SymbolAssociation, WoodAssociation, StoneAssociation, FishAssociation
from client.map.resources_weights import MapBioWeights, WoodWeights, StoneWeights, FishWeights
from PIL import Image


# TODO: batch generation?
class Map:
    _mask: list[list]
    _mask_size: tuple = (100, 100)  # (100, 100) MAX SIZE TO GENERATE!! Image size around 280-300mb
    _map: str
    _dict_textures_info = {
        "biom": {
            "texture_size": 512,
            "original_image_path": "../images/image_original/used_bioms",
            "used_texture": "../images/used_bioms",
        },
        "resources": {
            "texture_size": 128,
            "original_image_path": "../images/image_original/used_resources",
            "used_texture": "../images/used_resources",
        }
    }

    def __init__(self, max_size: tuple = (100, 100)):
        self._dirs_prepare()
        self._mask_size = max_size
        self._map = f"map_{int(time.time())}.jpeg"
        self._scale_image()
        self._generate_mask()

    def _dirs_prepare(self):
        for key, value in self._dict_textures_info.items():
            try:
                os.mkdir(value["used_texture"])
            except FileExistsError:
                pass
        try:
            os.mkdir("../images/map_directory")
        except FileExistsError:
            pass

    def _generate_mask(self):
        self._mask = [[None for _ in range(self._mask_size[0])] for _ in range(self._mask_size[1])]
        self._mask[0][0] = "_"

    def get_map(self):
        return self._map

    def get_scale_str(self, texture_type: str) -> str:
        size = self._dict_textures_info[texture_type]["texture_size"]
        return f"{size}x{size}"

    def get_scale_tuple(self, texture_type: str) -> int:
        size = self._dict_textures_info[texture_type]["texture_size"]
        return size

    def _scale_image(self):
        for key, values in self._dict_textures_info.items():
            size_str = self.get_scale_str(key)
            try:
                os.mkdir("/".join([values["used_texture"], f"{size_str}"]))
            except Exception as e:
                print(e)
            img_in_dir = os.listdir(values["original_image_path"])
            for img in img_in_dir:
                pil_img = Image.open("/".join([values["original_image_path"], img]))
                size_tuple = self.get_scale_tuple(key)
                new_image = pil_img.resize((size_tuple, size_tuple))
                image_name = img.split(".")[0] + size_str + "." + img.split(".")[1]
                new_image.save("/".join([values["used_texture"], f"{size_str}", image_name]))

    def generate_map(self):
        dir_for_map = f"../images/map_directory/g{MapBioWeights.green}_w{MapBioWeights.water}_m{MapBioWeights.mountain}_s{self._mask_size}_t{int(time.time())}"
        os.mkdir(dir_for_map)
        map_image = Image.new(
            "RGB",
            (
                self._mask_size[0] * self._dict_textures_info["biom"]["texture_size"],
                self._mask_size[1] * self._dict_textures_info["biom"]["texture_size"]),
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
                map_image.paste(
                    paste_image,
                    (
                        x_axis * self._dict_textures_info["biom"]["texture_size"],
                        y_axis * self._dict_textures_info["biom"]["texture_size"],
                    ),
                )

                self._mask[y_axis][x_axis] = curr_point

        map_image.save(
            "/".join([
                dir_for_map,
                f"{self._map}"
            ])
        )
        return "/".join([
                dir_for_map,
                f"{self._map}"
            ])

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

    def _generate_green(self) -> Image:
        resource = random.choices(
            [WoodAssociation.wood, WoodAssociation.none],
            weights=[WoodWeights.wood, WoodWeights.none]
        )[0]
        size_str_biom = self.get_scale_str("biom")
        path_biom = "/".join([self._dict_textures_info["biom"]["used_texture"], size_str_biom, f"green{size_str_biom}.jpg"])
        paste_image = Image.open(path_biom)
        if resource:
            size_str_resource = self.get_scale_str("resources")
            path_resource = "/".join([
                self._dict_textures_info["resources"]["used_texture"],
                size_str_resource, f"wood{size_str_resource}.png"
            ])
            resource_image = Image.open(path_resource)
            count = random.randint(1, 4)
            for wood_number in range(count):
                x_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] - self._dict_textures_info["resources"]["texture_size"]-1)
                y_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] - self._dict_textures_info["resources"]["texture_size"]-1)
                paste_image.paste(
                    resource_image,
                    (x_axis_wood, y_axis_wood)
                )
        return paste_image

    def _generate_fish(self) -> Image:
        resource = random.choices(
            [FishAssociation.fish, FishAssociation.none],
            weights=[FishWeights.fish, WoodWeights.none]
        )[0]
        size_str_biom = self.get_scale_str("biom")
        path_biom = "/".join([self._dict_textures_info["biom"]["used_texture"], size_str_biom, f"water{size_str_biom}.jpg"])
        paste_image = Image.open(path_biom)
        if resource:
            size_str_resource = self.get_scale_str("resources")
            path_resource = "/".join(
                [self._dict_textures_info["resources"]["used_texture"], size_str_resource, f"fish{size_str_resource}.png"])
            resource_image = Image.open(path_resource)
            count = random.randint(1, 4)
            for fish_number in range(count):
                x_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] - self._dict_textures_info["resources"]["texture_size"]-1)
                y_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] - self._dict_textures_info["resources"]["texture_size"]-1)
                paste_image.paste(
                    resource_image,
                    (x_axis_wood, y_axis_wood)
                )
        return paste_image

    def _generate_stone(self) -> Image:
        size_str_biom = self.get_scale_str("biom")
        path_biom = "/".join([self._dict_textures_info["biom"]["used_texture"], size_str_biom, f"mountain{size_str_biom}.jpg"])
        paste_image = Image.open(path_biom)
        return paste_image


if __name__ == '__main__':
    mapp = Map()
    img_path = mapp.generate_map()
    mmaapp = mapp.get_map()
    # for row in mmaapp:
    #     print(row)
