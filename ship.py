import pygame

class Ship: 
    def __init__(self, ai_game):
        """initialize the ship and set its sarting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Load the ship images and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # start each new ship at the bottom center of teh screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Update ship's position based on movement flags"""
        # Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0: 
            self.x -= self.settings.ship_speed
        #Update rectangle objects
        self.rect.x = self.x
        
    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    
    