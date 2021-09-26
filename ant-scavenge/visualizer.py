"""
Creates graphical interface to visualize simulation
"""

import pygame


def set_background(screen):
    background = pygame.Surface(screen.get_size())
    background.fill((230,230,230))
    background.convert()
    screen.blit(background, (0,0))


def main():
    print("Visualization Activated")
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("ant-scavenge")

    set_background(screen)
    pygame.display.update()

    pygame.time.delay(5000)
    pygame.quit()


if __name__=="__main__":
    main()  
