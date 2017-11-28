
import numpy as np

class Game():
    def __init__(self, game_map):
        self.map = game_map
        self.x = np.array([])
        self.y = np.array([])
        self.r = np.array([])

    def explore(self, x, y):
        r = self.map.reward(x, y)
        self.x = np.append(self.x, x)
        self.y = np.append(self.y, y)
        self.r = np.append(self.r, r)
        return r