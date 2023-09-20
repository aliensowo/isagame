import os
import json
from typing import Dict, Tuple
from client.settings import images_dir


map_path = os.path.join(images_dir, "map_directory/g30_w25_m25_s(50, 50)_t1694823254/system.json")


class Logic:

    @staticmethod
    def get_image(node: int) -> Tuple[str, Dict]:
        with open(map_path, "r") as fp:
            system = json.load(fp)

            node = system["coord"][f"{node}"]
            size = f"{node['size']}x{node['size']}"

            biom_image_background = os.path.join(images_dir, f"used_bioms/{size}/{node['biom']}{size}.jpg")
            resource_data = {}

            for resource, res_value in node["resources"].items():
                for elements in res_value:
                    e_size = f"{elements['size']}x{elements['size']}"
                    resource_data[resource] = {
                        "path": os.path.join(images_dir, f"../images/used_resources/{e_size}/{elements['type']}{e_size}.png"),
                        "type": elements['type'],
                        "x_biom": elements["x_biom"],
                        "y_biom": elements["y_biom"],
                    }

            return biom_image_background, resource_data
