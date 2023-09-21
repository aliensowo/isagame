import warnings
from client.class_game import Game


warnings.filterwarnings("ignore")


if __name__ == '__main__':
    g = Game(new_map=True)
    while True:
        g.new()
    pg.quit()
