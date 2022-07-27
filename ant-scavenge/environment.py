"""
Overall environement
"""
from board import BoardFactory
from board import Point

from visualizer import Visualizer

from agent import RandomMover

from collections import namedtuple
import numpy as np


action_map = {0: (0,0),
              1: (0,1),
              2: (1,0),
              3: (-0,-1),
              4: (-1,0),}


Record = namedtuple('Record', ['state', 'action', 'reward', 'next_state'])


class Ant():
    """
    Enivornment's interal representation of an ant
    (Not associated with visualization sprite)

    """
    def __init__(self, init_pos, agent=RandomMover()):
        self.history = [Point.cast(init_pos)]
        self.hasFood = False
        self.agent = agent
        self.action = None

    @property
    def pos(self):
        return self.history[-1]
        
    @pos.setter
    def pos(self, pos):
        self.history.append(Point.cast(pos))

    def choose_action(self, view):
        self.action = self.agent.get_action(view)


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
        self.ants = [Ant(pos) for pos in np.asarray(np.where(self.board.data['ants'])).T]
        self.seen = self.board.data['ants'].copy() 
        self.history = [self.board.copy()]

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

        views = []
        blockables = {
                (1,1): [(0,1), (1,0)],
                (2,1): [(2,0)],
                (3,1): [(3,0), (4,1)],
                (3,2): [(4,2)],
                (3,3): [(4,3), (3,4)],
                (2,3): [(2,4)],
                (1,3): [(1,4), (0,3)],
                (1,2): [(0,2)],
                }

        for pos in centers:
            # slice local view
            view = view_all[:,pos[0]-2+1:pos[0]+3+1, (pos[1]-2+1):(pos[1]+3+1)].copy()

            # hide as needed
            to_hide = [(0,0), (-1,0), (-1,-1), (0,-1)] # always hide corners 
            for (x,y), blocked in blockables.items():
                if view[0, x, y]:  to_hide.extend(blocked)
            for x,y in to_hide:
                view[ :,x,y] = 0
                view[-1,x,y] = 1

            views.append(view)
       
        return views

    def step(self):
        records = []
        np.random.shuffle(self.ants)  # random order of resolution
        views = self.get_views([ant.pos for ant in self.ants])
        for ant, view in zip(self.ants, views):
            ant.choose_action(view)
        for ant in self.ants:
            reward = 0
            src = ant.pos
            dst = ant.pos + action_map[ant.action]
            if self.board.data['walls'][dst]==0 and self.board.data['ants'][dst]==0:
                # move
                ant.pos=dst
                self.board.data['ants'][src] = 0  #no check
                self.board.data['ants'][dst] = 1

                # exploration reward
                if ant.hasFood==False:
                    if self.seen[dst]:
                        reward -= 0.01
                    else:
                        reward += 0.01
                self.seen[dst] = 1

                # get food?
                if self.board.data['food'][dst] == 1 and ant.hasFood==False:
                    reward += 1
                    ant.hasFood = True
                    self.board.data['food'][dst] = 0

                # deliver food?
                if self.board.data['mound'][dst] == 1 and ant.hasFood==True:
                    reward += 1
                    ant.hasFood = False

            else:
                reward -= 0.01
                ant.pos = src # required, autosave in ant history
            #unexpaned record, require calls to get_views for training
            records.append( Record(ant.pos, ant.action, reward, dst) )
        return records


class Sim():
    """
    ???
    """
    def __init__(self, shape):
        self.env = Environment(shape)

    def step(self):
        records = self.env.step()


if __name__ == "__main__":
    sim = Sim((25,25))
    vis = Visualizer(sim.env.board.shape)
    for _ in range(200):
        vis.show(sim.env.board)
        sim.step()
    vis.close()
