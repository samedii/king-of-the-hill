
import numpy as np
import matplotlib.pyplot as plt

class Map():
    def reward(self, x, y):
        raise NotImplementedError

    def gradient(self, x, y):
        raise NotImplementedError

    def hessian(self, x, y):
        raise NotImplementedError

class HomelyHill(Map):
    target = np.random.randn(2)*10
    def reward(self, x, y):
        return (-np.square(x - self.target[0]) - np.square(y - self.target[1]))

class PeakDistrict(Map):
    target = np.random.randn(2)*10
    def reward(self, x, y):
        return -np.abs(x - self.target[0]) - np.abs(y - self.target[1])