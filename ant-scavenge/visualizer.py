"""
Creates graphical interface to visualize simulation
"""

import pygame
from board import BoardFactory
from board import Point

colors = {'white-ish':  (230,230,230),
          'black':      (0,0,0)}

class Visualizer():
    _boarder_size = 2
    _voxel_size = 20
    _right_space = 200

    def __init__(self, shape):
        self.shape = shape
        # Sizes of board area, not full image
        self.x_size = self._boarder_size + shape.x*self._voxel_size
        self.y_size = self._boarder_size + shape.y*self._voxel_size 

        pygame.init()
        self.screen = pygame.display.set_mode((self.x_size + self._right_space, self.y_size))
        self.background = self._build_background()
        pygame.display.set_caption("ant-scavenge")

    def _build_background(self):
        background = pygame.Surface(self.screen.get_size())
        background.fill(colors['white-ish'])

        for x in range(self.shape.x+1):
            rect = pygame.Rect(x*self._voxel_size, 0, self._boarder_size, self.y_size)
            pygame.draw.rect(background, colors['black'], rect, 1)

        for y in range(self.shape.y+1):
            rect = pygame.Rect(0, y*self._voxel_size, self.x_size, self._boarder_size)
            pygame.draw.rect(background, colors['black'], rect, 1)

        background.convert()
        return background

    def show(self, board):
        self.screen.blit(self.background, (0,0))

        pygame.display.update()

    def close(self):
        pygame.time.delay(10000)
        pygame.quit()



if __name__=="__main__":
    bf = BoardFactory()
    board = bf.build((25,25))

    vis = Visualizer(board.shape)
    vis.show(board)
    vis.close()
