"""
Representation for game board
"""
from collections import namedtuple
import numpy as np
import copy


class Point(namedtuple('Point', ['x', 'y'])):
    def __add__(self, other):
        # not a collection, attempt to use as scalar
        if not hasattr(other, '__len__'):
            return Point(self.x + other, self.y + other)

        # some type of binary collection, assume it is Point-like:
        if len(other)==2: 
            return Point(self.x + other[0], self.y + other[1])

        raise TypeError(f"unsupported type for Point addition, use scalar or two-element collections, not {type(other)}")

    def __sub__(self, other):
        # not a collection, attempt to use as scalar
        if not hasattr(other, '__len__'):
            return Point(self.x - other, self.y - other)

        # some type of binary collection, assume it is Point-like:
        if len(other)==2: 
            return Point(self.x - other[0], self.y - other[1])

        raise TypeError(f"unsupported type for Point subtracion, use scalar or two-element collections, not {type(other)}")

    def __mul__(self, other):
        # not a collection, attempt to use as scalar
        if not hasattr(other, '__len__'):
            return Point(self.x * other, self.y * other)

        # some type of binary collection, assume it is Point-like:
        if len(other)==2: 
            return Point(self.x * other[0], self.y * other[1])

        raise TypeError(f"unsupported type for Point multiplication, use scalar or two-element collections, not {type(other)}")

    def absDistVec(self, other):
        return np.abs(self.x-other[0]), np.abs(self.y-other[1])

    @classmethod
    def cast(cls, other):
        return Point(other[0], other[1])


class BoardFactory():

    def build(self, shape):
        self.shape = Point.cast(shape)
        self.reset()
        self.generate_mound_and_ants()
        self.generate_food()
        self.generate_walls()

        packed = {
                  'ants':  self.ants,
                  'food':  self.food,
                  'mound': self.mound,
                  'walls': self.walls,
                  }

        return Board(self.shape, data=packed)  

    def reset(self):
        self.ants  = np.zeros(self.shape)
        self.food  = np.zeros(self.shape)
        self.mound = np.zeros(self.shape)
        self.walls = np.zeros(self.shape)
        self.mound_center = None

    def generate_mound_and_ants(self):
        """
        Spec (not technical limitations):
        Mound occupies a 3x3 area
        Mound must be least 4 from edge
        Ants occupy spaces adjacent to mound
        """

        # Place mound
        x = np.random.randint(4, self.shape.x-4)
        y = np.random.randint(4, self.shape.y-4)
        self.mound_center = Point(x,y)
        self.mound[x-1:x+2, y-1:y+2] = 1

        # Place ants
        for i in range(5):
            for j in range(5):
                if i in [0,4] and j in [0,4]:
                    pass # ignore corners
                elif i in [0,4] or j in [0,4]:
                    self.ants[Point(x-2+i, y-2+j)] = 1

    def generate_food(self):
        """
        Spec (not technical limitations):
        Food exists in 5x5 square 4 from edge but not adject to mound/ants
        All open have a 2% of having food, ignorning edge (walled later)
        """        

        # Select main food center
        while True:
            x = np.random.randint(4, self.shape.x-4)
            y = np.random.randint(4, self.shape.y-4)
            distVec = self.mound_center.absDistVec((x,y))
            if distVec[0]>6 and distVec[1]>6:
                break
        self.food[x-2:x+3, y-2:y+3] = 1

        # Place random other food
        self.food = np.logical_or(self.food, self.select_random_open(0.02))

    def generate_walls(self):
        """
        Spec (not technical limitations):
        Wall around edge
        All open have a 30% of having wall
        """        

        # Place outer walls
        new_walls = np.ones(self.shape, dtype=bool)
        new_walls[1:-1,1:-1] = self.walls[1:-1,1:-1]
        self.walls = new_walls

        # Place random other walls
        self.walls = np.logical_or(self.walls, self.select_random_open(0.3))

    def occupied(self):
        return np.logical_or.reduce((self.walls, self.food, self.ants, self.mound))

    def select_random_open(self, frac, include_edge=False):
        if include_edge:
            selection = np.random.random(self.shape) < frac
        else:
            selection = np.zeros(self.shape, dtype=bool)
            selection[1:-1,1:-1] = np.random.random(self.shape-2) < frac
        return np.logical_and(selection, np.logical_not(self.occupied()))


class Board():
    """
    Stores location of everything in the environment.

    Thin wrapper for dictionary of 2D numpy arrays
    """
    def __init__(self, shape, data=None):
        self.shape = Point.cast(shape)
        if data is None:
            self.data = {}
        else:
            self.data = data

    @classmethod
    def from_board(cls, board_instance):
        shape = board_instance.shape
        data = copy.deepcopy(board_instance.data)
        return cls(shape, data=data)

    def as_numpy(self):
        output = np.zeros(self.shape)
        output += 1*self.data['walls']
        output += 2*self.data['food']
        output += 3*self.data['ants']
        output += 4*self.data['mound']
        labels = {0: ' ',
                  1: 'w',
                  2: 'f',
                  3: 'a',
                  4: 'm',
                  7: '@', #ant on mound
                  }
        return np.vectorize(lambda x: labels[x])(output.astype(int)).T


if __name__ == "__main__":
    print("debug test only")
    bf = BoardFactory()
    board = bf.build((25,25))
    text_vis = board.as_numpy()
    for row in text_vis:
        print(''.join(row))
    board_copied = Board.from_board(board)
    text_vis = board_copied.as_numpy()
    for row in text_vis:
        print(''.join(row))

