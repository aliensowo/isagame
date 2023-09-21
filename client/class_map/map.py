from warnings import warn
import random
import time
from typing import Dict
import os
from hashlib import md5
import json
from deprecated import deprecated

from client.class_map.map_error import MapGenerateError, SymbolAssociationError
from client.class_map.map_types import SymbolAssociation, WoodAssociation, StoneAssociation, FishAssociation
from client.class_map.resources_weights import MapBioWeights, WoodWeights, StoneWeights, FishWeights
from client.settings import images_dir
from PIL import Image


# TODO: batch generation?
class Map:
    _mask: list[list]
    _mask_size: tuple = (100, 100)  # (100, 100) MAX SIZE TO GENERATE!! Image size around 280-300mb
    _map: str
    _creation_time: int = int(time.time())
    _system: Dict = {}
    _map_dir: str
    """
    system = {
        coords: {
            0: {
                x: x,
                y: y,
                size: size,
                biom: biom,
                resources: {
                    wood: [
                        {
                            type: wood | none,
                            size: size,
                            x_biom: x,
                            y_biom: y,
                        },
                        ...
                    ],
                    fish: [],
                }
            }
        }
    }

    """
    _dict_textures_info = {
        "biom": {
            "texture_size": 512,
            "original_image_path": os.path.join(images_dir, "image_original/used_bioms"),
            "used_texture": os.path.join(images_dir, "used_bioms"),
        },
        "resources": {
            "texture_size": 128,
            "original_image_path": os.path.join(images_dir, "image_original/used_resources"),
            "used_texture": os.path.join(images_dir, "used_resources"),
        }
    }
    _biom_map: dict

    @staticmethod
    def get_config_map():
        biom_map = {
            "resource": {
                "green": {
                    "wood": {
                        "association": WoodAssociation,
                        "weight": WoodWeights,
                    },
                },
                "water": {
                    "fish": {
                        "association": FishAssociation,
                        "weight": WoodWeights,
                    },
                },
            },
            "biom": {
                "weight": MapBioWeights,
            }
        }
        return biom_map

    def __init__(
            self,
            max_size_map_bioms: tuple = (100, 100),
            biom_size: int = 512,
            resources_size: int = 128
            # TODO: resource reach
            #
    ):
        self._biom_map = self.get_config_map()
        self._mask_size = max_size_map_bioms
        self._dict_textures_info["biom"]["texture_size"] = biom_size
        self._dict_textures_info["resources"]["texture_size"] = resources_size
        self._dirs_prepare()
        self._map_dir = os.path.join(
            images_dir,
            f"map_directory/g{MapBioWeights.green}_w{MapBioWeights.water}_m{MapBioWeights.mountain}_s{self._mask_size}_t{self._creation_time}"
        )
        self._map = f"map_{self._creation_time}.jpeg"
        self._scale_image()
        self._generate_mask()

    def _dirs_prepare(self):
        for key, value in self._dict_textures_info.items():
            try:
                os.mkdir(value["used_texture"])
            except FileExistsError:
                pass
        try:
            os.mkdir(os.path.join(images_dir, "map_directory"))
        except FileExistsError:
            pass

    def _generate_mask(self):
        print("Prepare mask")
        self._mask = [[None for _ in range(self._mask_size[0])] for _ in range(self._mask_size[1])]
        self._mask[0][0] = "_"

    def get_scale_str(self, texture_type: str) -> str:
        size = self._dict_textures_info[texture_type]["texture_size"]
        return f"{size}x{size}"

    def get_scale_tuple(self, texture_type: str) -> int:
        size = self._dict_textures_info[texture_type]["texture_size"]
        return size

    def _scale_image(self):
        print("Prepare textures")
        for key, values in self._dict_textures_info.items():
            size_str = self.get_scale_str(key)
            try:
                os.mkdir(os.path.join(values["used_texture"], f"{size_str}"))
                img_in_dir = os.listdir(values["original_image_path"])
                for img in img_in_dir:
                    pil_img = Image.open(os.path.join(values["original_image_path"], img))
                    size_tuple = self.get_scale_tuple(key)
                    new_image = pil_img.resize((size_tuple, size_tuple))
                    image_name = img.split(".")[0] + size_str + "." + img.split(".")[1]
                    new_image.save(os.path.join(values["used_texture"], f"{size_str}", image_name))
            except Exception as e:
                print(e)

    def generate_map(self):
        print("Prepare map")
        os.mkdir(self._map_dir)
        map_image = Image.new(
            "RGB",
            (
                self._mask_size[0] * self._dict_textures_info["biom"]["texture_size"],
                self._mask_size[1] * self._dict_textures_info["biom"]["texture_size"]),
            "white",
        )
        self._system["coord"] = {}
        biom_number = 0
        for y_axis in range(len(self._mask)):
            for x_axis in range(len(self._mask[y_axis])):
                green_boost, water_boost, mountain_boost = (0, 0, 0)
                try:
                    for point in [
                        self._mask[y_axis][x_axis - 1],  # left point
                        self._mask[y_axis - 1][x_axis],  # up point
                        self._mask[y_axis - 1][x_axis + 1],  # up right point
                    ]:
                        green_boost, water_boost, mountain_boost = self._default_boost_values(
                            point=point,
                            boost={
                                "green_boost": green_boost,
                                "water_boost": water_boost,
                                "mountain_boost": mountain_boost,
                            },
                        )
                except IndexError:
                    pass
                curr_point = random.choices(
                    [SymbolAssociation.water, SymbolAssociation.green, SymbolAssociation.mountain],
                    weights=[
                        MapBioWeights.water + water_boost if MapBioWeights.water + water_boost > 0 else 0,
                        MapBioWeights.green + green_boost if MapBioWeights.green + green_boost > 0 else 0,
                        MapBioWeights.mountain + mountain_boost if MapBioWeights.mountain + mountain_boost > 0 else 0,
                    ],
                )[0]
                self._system["coord"][biom_number] = {}
                self._system["coord"][biom_number]["size"] = self._dict_textures_info["biom"]["texture_size"]
                self._system["coord"][biom_number]["x"] = x_axis
                self._system["coord"][biom_number]["y"] = y_axis
                self._system["coord"][biom_number]["resources"] = {}
                paste_image = self._generate_element(curr_point=curr_point, biom_number=biom_number)
                map_image.paste(
                    paste_image,
                    (
                        x_axis * self._dict_textures_info["biom"]["texture_size"],
                        y_axis * self._dict_textures_info["biom"]["texture_size"],
                    ),
                )
                biom_number += 1
                self._mask[y_axis][x_axis] = curr_point

        save_path = os.path.join(self._map_dir, f"{self._map}")
        map_image.save(save_path)
        return save_path

    def _generate_element(self, curr_point: str, biom_number: int) -> Image:
        if curr_point == SymbolAssociation.green:
            # generate wood
            self._system["coord"][biom_number]["biom"] = "green"
            paste_image = self._generate_biom(biom_number=biom_number, biom_type="green")
        elif curr_point == SymbolAssociation.water:
            # generate fish
            self._system["coord"][biom_number]["biom"] = "water"
            paste_image = self._generate_biom(biom_number=biom_number, biom_type="water")
        elif curr_point == SymbolAssociation.mountain:
            # TODO: generate stone
            self._system["coord"][biom_number]["biom"] = "mountain"
            paste_image = self._generate_stone(biom_number=biom_number)
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
        if mountain_boost >= 60:
            mountain_boost = 0
        return green_boost, water_boost, mountain_boost

    def _generate_biom(self, biom_number: int, biom_type):
        warn(
            'Support for green, water bioms only. For stone use `_generate_stone`',
            Warning,
            stacklevel=2,
        )
        resource_list = []

        for resource_type, resource_values in self._biom_map["resource"][biom_type].items():
            resource = random.choices(
                resource_values["association"].keys(),
                weights=resource_values["weight"].values()
            )[0]
            size_str_biom = self.get_scale_str("biom")
            path_biom = os.path.join(
                self._dict_textures_info["biom"]["used_texture"],
                size_str_biom,
                f"{biom_type}{size_str_biom}.jpg",
            )
            paste_image = Image.open(path_biom)
            if resource:
                size_str_resource = self.get_scale_str("resources")
                path_resource = os.path.join(
                    self._dict_textures_info["resources"]["used_texture"],
                    size_str_resource,
                    f"{resource_type}{size_str_resource}.png",
                )
                resource_image = Image.open(path_resource)
                count = random.randint(0, 4)
                for resource_number in range(count):
                    x_max = self._dict_textures_info["biom"]["texture_size"] - self._dict_textures_info["resources"]["texture_size"] - 1
                    x_axis_resource = random.randint(1, x_max)
                    y_max = self._dict_textures_info["biom"]["texture_size"] - self._dict_textures_info["resources"]["texture_size"] - 1
                    y_axis_resource = random.randint(1, y_max)
                    resource_element = {
                        "type": resource_type,
                        "size": self._dict_textures_info["resources"]["texture_size"],
                        "x_biom": x_axis_resource,
                        "y_biom": y_axis_resource,
                    }
                    if md5(json.dumps(resource_element).encode("utf8")).hexdigest() in [
                        md5(json.dumps(i).encode("utf8")).hexdigest() for i in resource_list
                    ]:
                        continue
                    paste_image.paste(
                        resource_image,
                        (x_axis_resource, y_axis_resource)
                    )
                    resource_list.append(resource_element.copy())
            self._system["coord"][biom_number]["resources"][resource_type] = resource_list
            return paste_image

    @deprecated(version='0.0.1', reason="You should use `generate_biom` function")
    def _generate_wood(self, biom_number: int) -> Image:
        # warn('This method is deprecated. Use `generate_biom`', DeprecationWarning, stacklevel=2)
        wood_list = []

        resource = random.choices(
            [WoodAssociation.wood, WoodAssociation.none],
            weights=[WoodWeights.wood, WoodWeights.none]
        )[0]
        size_str_biom = self.get_scale_str("biom")
        path_biom = "/".join(
            [self._dict_textures_info["biom"]["used_texture"], size_str_biom, f"green{size_str_biom}.jpg"])
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
                x_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] -
                                             self._dict_textures_info["resources"]["texture_size"] - 1)
                y_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] -
                                             self._dict_textures_info["resources"]["texture_size"] - 1)
                wood_element = {
                    "type": resource,
                    "size": self._dict_textures_info["resources"]["texture_size"],
                    "x_biom": x_axis_wood,
                    "y_biom": y_axis_wood,
                }
                # TODO: resolve collision as 1 px between
                if md5(json.dumps(wood_element).encode("utf8")).hexdigest() in [
                    md5(json.dumps(w).encode("utf8")).hexdigest() for w in wood_list]:
                    continue
                paste_image.paste(
                    resource_image,
                    (x_axis_wood, y_axis_wood)
                )
                wood_list.append(wood_element.copy())
        self._system["coord"][biom_number]["resources"]["wood"] = wood_list
        return paste_image

    @deprecated(version='0.0.1', reason="You should use `generate_biom` function")
    def _generate_fish(self, biom_number: int) -> Image:
        # warn('This method is deprecated. Use `generate_biom`', DeprecationWarning, stacklevel=2)
        fish_list = []
        resource = random.choices(
            [FishAssociation.fish, FishAssociation.none],
            weights=[FishWeights.fish, WoodWeights.none]
        )[0]
        size_str_biom = self.get_scale_str("biom")
        path_biom = "/".join(
            [self._dict_textures_info["biom"]["used_texture"], size_str_biom, f"water{size_str_biom}.jpg"])
        paste_image = Image.open(path_biom)
        if resource:
            size_str_resource = self.get_scale_str("resources")
            path_resource = "/".join(
                [self._dict_textures_info["resources"]["used_texture"], size_str_resource,
                 f"fish{size_str_resource}.png"])
            resource_image = Image.open(path_resource)
            count = random.randint(1, 4)
            for fish_number in range(count):
                x_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] -
                                             self._dict_textures_info["resources"]["texture_size"] - 1)
                y_axis_wood = random.randint(1, self._dict_textures_info["biom"]["texture_size"] -
                                             self._dict_textures_info["resources"]["texture_size"] - 1)
                fish_element = {
                    "type": resource,
                    "size": self._dict_textures_info["resources"]["texture_size"],
                    "x_biom": x_axis_wood,
                    "y_biom": y_axis_wood,
                }
                # TODO: resolve collision as 1 px between
                if md5(json.dumps(fish_element).encode("utf8")).hexdigest() in [
                    md5(json.dumps(f).encode("utf8")).hexdigest() for f in fish_list]:
                    continue
                paste_image.paste(
                    resource_image,
                    (x_axis_wood, y_axis_wood)
                )
                fish_list.append(fish_element.copy())
        self._system["coord"][biom_number]["resources"]["fish"] = fish_list
        return paste_image

    def _generate_stone(self, biom_number: int) -> Image:
        stone_list = []
        size_str_biom = self.get_scale_str("biom")
        path_biom = os.path.join(
            self._dict_textures_info["biom"]["used_texture"],
            size_str_biom,
            f"mountain{size_str_biom}.jpg"
        )
        paste_image = Image.open(path_biom)
        self._system["coord"][biom_number]["resources"]["stone"] = stone_list
        return paste_image

    def save_system(self):
        with open(os.path.join(self._map_dir, "system.json"), "w") as fp:
            json.dump(self._system, fp)
        return os.path.join(self._map_dir, "system.json")


if __name__ == '__main__':
    mapp = Map(max_size_map_bioms=(50, 50), resources_size=32)
    img_path = mapp.generate_map()
    print(img_path)
    mapp.save_system()

