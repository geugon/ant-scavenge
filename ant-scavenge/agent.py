import numpy as np


class RandomMover():
    def __init__(self):
        pass

    def get_action(self, view):
        return np.random.choice(5)

