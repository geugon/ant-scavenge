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

        # Last used values of these, used as temp storage for convenience
        self.action = None
        self.view = None
        self.reward = None

    @property
    def pos(self):
        return self.history[-1]
        
    @pos.setter
    def pos(self, pos):
        self.history.append(Point.cast(pos))

    def choose_action(self, view):
        self.view = view
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

    def step(self):

        # Execute simulation
        np.random.shuffle(self.ants)  # random order of resolution
        views = self.board.get_views([ant.pos for ant in self.ants])
        for ant, view in zip(self.ants, views):
            ant.choose_action(view)
            ant.reward = self._resolve(ant)

        # Build records for training
        records = []
        new_views = self.board.get_views([ant.pos for ant in self.ants])
        for ant, view in zip(records, new_views):
            records.append( Record(ant.view, ant.action, ant.reward, view) )
        return records

    def _resolve(self, ant):
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

            # get food reward
            if self.board.data['food'][dst] == 1 and ant.hasFood==False:
                reward += 1
                ant.hasFood = True
                self.board.data['food'][dst] = 0

            # deliver food reward
            if self.board.data['mound'][dst] == 1 and ant.hasFood==True:
                reward += 1
                ant.hasFood = False

        else:
            reward -= 0.01
            ant.pos = src # required, autosave in ant history

        return reward
        

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
