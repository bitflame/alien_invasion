import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self, ai_game):
        """initialize the alien and set its starting position"""
        super.__init__()
        self.screen = ai_game.screen
        
        # load the star image and set its rect attributes
        self.image = pygame.image.load('images/star.png')
        self.rect = self.image.get_rect()
        
        # Start each new star near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store star's exact horizontal position
        self.x = float(self.rect.x)