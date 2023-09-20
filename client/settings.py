import os


# image path
images_dir = os.path.join(os.path.dirname(__file__), 'images')

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# screen settings
WIDTH = 512
HEIGHT = 512
FPS = 30

# globals
turn_flag = False
curr_node = 0