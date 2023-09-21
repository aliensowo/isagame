import os

# image path
images_dir = os.path.join(os.path.dirname(__file__), 'images')

# player setup
DEFUALT_HP = 100
DEFUALT_PROT = 100
DEFUALT_ATK = 10

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 102, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)

# screen settings
WIDTH = 512
HEIGHT = 512
FPS = 30
TITLE = "Is a Game?"
BGCOLOR = DARKGREY
START_NODE = 0

#
STATPOSX = 50
TILESIZE = 32
UIHEIGTH = 300
INVTILESIZE = 48
COINOFFSET = 4
GRIDWIDTH = (TILESIZE, WIDTH - TILESIZE)
GRIDHEIGHT = (TILESIZE, HEIGHT - TILESIZE)

# globals
turn_flag = False
curr_node = 0
