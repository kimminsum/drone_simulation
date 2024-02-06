import pygame

from drone import Drone


# Window setup
WIDTH = 800
HEIGHT = 600


if __name__=="__main__":
    pygame.init()
    pygame.font.init()

    Title = "Drone Project (User)"
    pygame.display.set_caption(Title)

    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    drone = Drone(screen, genome=None)
    drone.run()