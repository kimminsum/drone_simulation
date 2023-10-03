import pygame
from pygame.locals import *
import math

class Drone(pygame.sprite.Sprite):
    def __init__(self, window):
        super().__init__()
        self. window = window
        # Drone's size        
        self.width = 100
        self.height = 30
        
        self.colour = (135, 206, 235) # Setup Drone's colour to skyblue
        
        # State (Position, Rotate rate)
        self.vec = pygame.math.Vector2(450, 300)
        self.angle = (30) % 360
        
        # Draw first square sprite object
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.image.set_colorkey((0, 0, 0))  
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(center = self.vec)
        
    def update(self):
        self.angle += 5
        self.angle %= 360
        # Draw first object
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.colour)
        self.image.set_colorkey((0, 0, 0))  
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(center=self.rect.center)

        pygame.draw.line(self.window, (255, 0, 0), self.rect.center, (self.rect.center[0], self.rect.center[1]-50), 2)
   

