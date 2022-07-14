"""
Representation for game board
"""
from board import BoardFactory
from board import Point
import numpy as np


action_map = {0: (0,0),
              1: (0,1),
              2: (1,0),
              3: (-0,-1),
              4: (-1,0),}

class Ant():
    """
    Enivornment's interal representation of an ant
    (Not associated with visualization sprite)

    """
    def __init__(self, init_pos):
        self.history = [init_pos]
        self.hasFood = False

    @property
    def pos(self):
        return self.history[-1]
        

class Environment():
    """
    Simulation Environment
    """
    def __init__(self, shape):
        self.shape = Point.cast(shape)
        self.bf = BoardFactory()
        self.reset()

    def reset(self):
        self.board = self.bf.build(self.shape)
        self.history = [self.board]

    def get_views(self, centers):
        """
        return 5x5 views from centers
        corners and areas behind walls are hidden
        """
        data = np.asarray([self.board.data['walls'], 
                           self.board.data['food'], 
                           self.board.data['ants'], 
                           self.board.data['mound']])
        view_all = np.zeros((data.shape[0]+1,  #last dim is for hidden
                             data.shape[1]+2,
                             data.shape[2]+2))
        view_all[:-1,1:-1,1:-1] = data

        def hide_helper(arr, x, y):
            arr[:,x,y] = 0
            arr[-1,x,y] = 1

        views = []
        for pos in centers:
            view = view_all[:,pos[0]-2+1:pos[0]+3+1, (pos[1]-2+1):(pos[1]+3+1)].copy()
            hide_helper(view, 0, 0)
            hide_helper(view, -1, 0)
            hide_helper(view, -1, -1)
            hide_helper(view, 0, -1)
            if view[0,1,1]: 
                hide_helper(view, 0, 1)
                hide_helper(view, 1, 0)
            if view[0,2,1]:
                hide_helper(view, 2, 0)
            if view[0,3,1]:
                hide_helper(view, 3, 0)
                hide_helper(view, 4, 1)
            if view[0,3,2]:
                hide_helper(view, 4, 2)
            if view[0,3,3]:
                hide_helper(view, 4, 3)
                hide_helper(view, 3, 4)
            if view[0,2,3]:
                hide_helper(view, 2, 4)
            if view[0,1,3]:
                hide_helper(view, 1, 4)
                hide_helper(view, 0, 3)
            if view[0,1,2]:
                hide_helper(view, 0, 2)
            views.append(view)
       
        return views


class Sim():
    """
    ???
    """
    def __init__(self, shape):
        self.env = Environment(shape)
        self.ants = [Ant(pos) for pos in np.asarray(np.where(self.env.board.data['ants'])).T]

    def step(self):
        pass
        centers = [ant.pos for ant in self.ants]
        views = self.env.get_views([ant.pos for ant in self.ants])
        print(views)



if __name__ == "__main__":
    sim = Sim((25,25))
    sim.step()
