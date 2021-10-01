"""
Creates graphical interface to visualize simulation
"""
import pygame
from board import BoardFactory
from board import Point
import numpy as np


colors = {'white-ish':  (230,230,230),
          'black':      (0,0,0),
          'dark grey':  (60,60,60)}


class Wall(pygame.sprite.Sprite):
    def __init__(self, size, pos, imgFile=None):
        super().__init__()
        
        if imgFile:
            self.image = pygame.image.load(imgFile).convert_alpha()
        else:
            self.image = pygame.Surface(size)
            self.image.fill(colors['dark grey'])

        self.rect = self.image.get_rect()
        self.rect = pos


class Visualizer():
    _boarder_size = 2
    _voxel_size = 20 # includes one-sided boarder
    _right_space = 200

    def __init__(self, shape):
        self.shape = shape
        # Sizes of board area, not full image
        self.x_size = self._boarder_size + shape.x*self._voxel_size
        self.y_size = self._boarder_size + shape.y*self._voxel_size 
        self.piece_size = Point(self._voxel_size-self._boarder_size, self._voxel_size-self._boarder_size)

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

        walls = pygame.sprite.Group()
        for wall_coord in np.asarray(np.where(board.data['walls'])).T:
            pos = Point.cast(wall_coord)
            pos = Point.cast(wall_coord)*self._voxel_size + self._boarder_size
            walls.add(Wall(self.piece_size, pos))
        walls.draw(self.screen)
 
        pygame.display.update()
        pygame.time.delay(4000)

    def close(self):
        pygame.quit()



if __name__=="__main__":
    bf = BoardFactory()
    board1 = bf.build((25,25))
    board2 = bf.build((25,25))

    vis = Visualizer(board1.shape)
    vis.show(board1)
    vis.show(board2)
    vis.close()
