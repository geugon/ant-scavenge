"""
Creates graphical interface to visualize simulation
"""
import pygame
from board import BoardFactory
from board import Point
import numpy as np


colors = {'white-ish':  (230,230,230),
          'black':      (0,0,0),
          'dark grey':  (60,60,60),
          'red':        (255,0,0),
          'dark red':   (128,0,0),
          'green':      (0,255,0),
          }


class Piece(pygame.sprite.Sprite):
    def __init__(self, size, pos, imgFile=None):
        super().__init__()

        if imgFile:
            self.image = pygame.image.load(imgFile).convert_alpha()
        else:
            self.image = pygame.Surface(size)
            self.image.fill(self._color)
 
        self.rect = self.image.get_rect()
        self.rect = pos


class Wall(Piece):
    _color = colors['dark grey']


class Mound(Piece):
    _color = colors['dark red']


class Ant(Piece):
    _color = colors['red']


class Food(Piece):
    _color = colors['green']


class SpriteManager():
    """
    Builds and Stores Sprites
    """
    _class_lookup = {'walls': Wall,
                     'ants': Ant,
                     'food': Food,
                     'mound': Mound,
                    }

    def __init__(self, _voxel_size, _boarder_size):
        self._voxel_size = _voxel_size
        self._boarder_size = _boarder_size
        self.piece_size = Point(self._voxel_size-self._boarder_size, self._voxel_size-self._boarder_size)

        self.sprites = {'walls': pygame.sprite.Group(),
                        'ants': pygame.sprite.Group(),
                        'mound': pygame.sprite.Group(),
                        'food': pygame.sprite.Group(),
                       }
        self.src_data = {'walls': np.array(0),
                        'ants': np.array(0),
                        'mound': np.array(0),
                        'food': np.array(0),
                       }

    def update(self, data):
        for item in data.items():
            self._build_group(*item)

    def get_all(self):
        return self.sprites

    def _build_group(self, name, data):
        if np.array_equal(self.src_data[name], data):
            return #no change

        group = pygame.sprite.Group()
        for coord in np.asarray(np.where(data)).T:
            pos = Point.cast(coord)*self._voxel_size + self._boarder_size
            group.add(self._class_lookup[name](self.piece_size, pos))

        self.sprites[name] = group
        self.src_data[name] = data


class Visualizer():
    _boarder_size = 2
    _voxel_size = 20 # includes one-sided boarder
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

        self.sprites = SpriteManager(self._voxel_size, self._boarder_size)

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

        self.sprites.update(board.data)
        for name, group in self.sprites.get_all().items():
            group.draw(self.screen)
 
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
    vis.show(board2)
    vis.close()
