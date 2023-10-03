import pygame
from pygame.locals import *

class Car(pygame.sprite.Sprite):
    def __init__(self, window):
        super().__init__()
        self. window = window
        
        self.width = 50
        self.height = 100
        
        self.colour = (135, 206, 235) # Setup Car's colour to skyblue
        
        self.vec = pygame.math.Vector2(450, 300)

        # Draw first square sprite object
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(center = self.vec)


    def update(self):
        self.rect.x += 1
        # Draw first object
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.colour)
        self.image.set_alpha(200)

        pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(self.rect.center[0], self.rect.center[1], 2, 70))
   

