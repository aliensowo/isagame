import os
import json
import random
from typing import Dict, Tuple
from client.settings import images_dir
from client.class_map.map import Map

# map_path = os.path.join(images_dir, "map_directory/g30_w25_m25_s(50, 50)_t1694823254/system.json")


class Logic:

    @staticmethod
    def get_random_map():
        # maps = os.listdir(os.path.join(images_dir, "map_directory"))
        return os.path.join(images_dir, "map_directory", "g30_w25_m25_s(50, 50)_t1695254738", "system.json")

    @staticmethod
    def generate_map(max_size_map_bioms: Tuple = (50, 50), biom_size: int = 512, resources_size: int = 128):
        map_class = Map(max_size_map_bioms=max_size_map_bioms, biom_size=biom_size, resources_size=resources_size)
        map_class.generate_map()
        # map_path = os.path.join(images_dir, img_path, "system.json")
        map_path = map_class.save_system()
        return map_path

    @staticmethod
    def get_image(node: int, map_path) -> Tuple[str, Dict]:
        with open(map_path, "r") as fp:
            system = json.load(fp)

            node = system["coord"][f"{node}"]
            size = f"{node['size']}x{node['size']}"

            biom_image_background = os.path.join(images_dir, f"used_bioms/{size}/{node['biom']}{size}.jpg")
            resource_data = {}

            for resource, res_value in node["resources"].items():
                resource_data[resource] = []
                for elements in res_value:
                    e_size = f"{elements['size']}x{elements['size']}"
                    resource_data[resource].append({
                        "path": os.path.join(images_dir, f"../images/used_resources/{e_size}/{elements['type']}{e_size}.png"),
                        "type": elements['type'],
                        "x_biom": elements["x_biom"],
                        "y_biom": elements["y_biom"],
                        "size": elements["size"]
                    })

            return biom_image_background, resource_data
