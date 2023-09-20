import json


map_path = "../images/map_directory/g30_w25_m25_s(50, 50)_t1694823254/system.json"


def get_image(node: int):
    with open(map_path, "r") as fp:
        system = json.load(fp)

        node = system["coord"][f"{node}"]
        size = f"{node['size']}x{node['size']}"

        biom_image_background = f"../images/used_bioms/{size}/{node['biom']}{size}.jpg"
        return biom_image_background
