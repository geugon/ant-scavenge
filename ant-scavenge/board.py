from collections import namedtuple
import numpy as np
import copy


class Point(namedtuple('Point', ['x', 'y'])):
    def __add__(self, other):
        # not a collection, attempt to use as scalar
        if not hasattr(other, 'len'):
            return Point(self.x + other, self.y + other)

        # some type of binary collection, assume it is Point-like:
        if len(other)==2: 
            return Point(self.x + other[0], self.y + other[1])

        raise TypeError(f"unsupported type for Point addition, use scalar or two-element collections, not {type(other)}")

    def __sub__(self, other):
        # not a collection, attempt to use as scalar
        if not hasattr(other, 'len'):
            return Point(self.x - other, self.y - other)

        # some type of binary collection, assume it is Point-like:
        if len(other)==2: 
            return Point(self.x - other[0], self.y - other[1])

        raise TypeError(f"unsupported type for Point subtracion, use scalar or two-element collections, not {type(other)}")

    def absDistVec(self, other):
        return np.abs(self.x-other[0]), np.abs(self.x-other[0])

    @classmethod
    def cast(cls, other):
        return Point(other[0], other[1])


class Board():
    """
    Stores location of everything in the environment.
    """
    def __init__(self, shape):
        self.shape = Point.cast(shape)
        self.generate_mound_and_ants()
        self.generate_food()
        self.generate_walls()

    def generate_mound_and_ants(self):
        """
        Spec (not technical limitations):
        Mound occupies a 3x3 area
        Mound must be least 4 from edge
        Ants occupy spaces adjacent to mound
        """

        # Select mound center
        x = np.random.randint(4, self.shape.x-4)
        y = np.random.randint(4, self.shape.y-4)
        self.mound_center = Point(x,y)

        # Place mound
        self.mound = []
        for i in range(3):
            for j in range(3):
                    self.mound.append(Point(x-1+i, y-1+j))

        # Place ants
        self.ants = []
        for i in range(5):
            for j in range(5):
                if i in [0,4] and j in [0,4]:
                    pass # ignore corners
                elif i in [0,4] or j in [0,4]:
                    self.ants.append(Point(x-2+i, y-2+j))

    def generate_food(self):
        """
        Spec (not technical limitations):
        Food exists in 5x5 square 4 from edge but not adject to mound/ants
        All open have a 2% of having food, ignorning edge (walled later)
        """        

        # Select food center
        while True:
            x = np.random.randint(4, self.shape.x-4)
            y = np.random.randint(4, self.shape.y-4)
            distVec = self.mound_center.absDistVec((x,y))
            if distVec[0]>6 and distVec[1]>6:
                break

        # Place main food 5x5
        self.food = []
        for i in range(5):
            for j in range(5):
                    self.food.append(Point(x-2+i, y-2+j))

        # Place random other food
        for i, j in zip(*np.where(np.random.random(self.shape-2) < 0.02)):
            p = Point(i,j)+1
            if (p not in self.mound and 
                p not in self.ants and
                p not in self.food):
                self.food.append(p)

    def generate_walls(self):
        """
        Spec (not technical limitations):
        Wall around edge
        All open have a 30% of having wall
        """        

        # Place outer walls
        self.walls = []
        for x in range(self.shape.x):
            self.walls.append(Point(x, 0))
            self.walls.append(Point(x, self.shape.y-1))
        for y in range(1,self.shape.y-1):
            self.walls.append(Point(0, y))
            self.walls.append(Point(self.shape.x-1, y))

        # Place random other food
        for i, j in zip(*np.where(np.random.random(self.shape-2) < 0.30)):
            p = Point(i,j)+1
            if (p not in self.mound and 
                p not in self.ants and
                p not in self.food):
                self.walls.append(p)

    def as_numpy(self):
        output = np.array([' ']*self.shape.x*self.shape.y).reshape(self.shape)
        for p in self.walls:
            output[p] = 'w'
        for p in self.food:
            output[p] = 'f'
        for p in self.mound:
            output[p] = 'm'
        for p in self.ants:
            output[p] = 'a'
        return output.T


if __name__ == "__main__":
    print("debug test only")
    board = Board((25,25))
    text_vis = board.as_numpy()
    for row in text_vis:
        print(''.join(row))