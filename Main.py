import pygame
from pygame.locals import *

from Car import Car

BLACK = (0, 0, 0)


class Simulation:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Setting window
        self.screen_width = 900
        self.screen_height = 600
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simulation") # Setup game title
        
        # Setting clock
        self.clock = pygame.time.Clock()

        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        self.car = Car(self.window)
        self.all_sprites.add(self.car)

        # Create game roop
        self.running = True
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                # Check for QUIT event      
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.update()

        pygame.quit()
    """ 
    Update window 
    """
    def update(self):
        # Setup game framerate to 60fps
        self.clock.tick(60)
        
        
        # Filling the window with black color
        self.window.fill(BLACK) 
        self.all_sprites.draw(self.window)
        self.all_sprites.update()

        # Updating the display surface
        pygame.display.update() 


if __name__=="__main__":
    world = Simulation()
    world.run()