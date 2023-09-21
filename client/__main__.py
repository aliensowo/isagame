import warnings
from client.class_game.game import Game


warnings.filterwarnings("ignore")


if __name__ == '__main__':
    g = Game(new_map=False)
    while True:
        g.new()
    pg.quit()
