import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from alien import Alien
from bullet import Bullet
from button import Button

class AlienInvasion: 
    """Overall class to manage game """
    def __init__(self):
        """initialize the game"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((1200,800))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        #Create an instance to store game statistics
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.play_button = Button(self, "Play", 600 , 400)
        self.level_one_button = Button(self, "2XSpeed", 100, 100)
        self.level_two_button = Button(self, "4XSpeed", 100, 200)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # set background color 
        self.bg_color = (230, 230, 230)
        # start Alien Invasion in an active state
        self.game_active = False
        
    def _ship_hit(self):
        """Respond to ship being hit"""
        if self.stats.ships_left > 0:   
            # Decrement ships_left
            self.stats.ships_left -= 1
            # Get rid fo any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # Crete a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5) 
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
        
    def run_game(self):
        """Start the main loop fo the game"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()    
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        # Watch for keboard and mouse envents.
        for event in pygame.event.get(): #<- this is called event loop
            # if event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
        
                
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        level_one_activated = self.level_one_button.rect.collidepoint(mouse_pos)
        level_two_activated = self.level_two_button.rect.collidepoint(mouse_pos)
        if  button_clicked and not self.game_active :
            # Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active=True
            # Get rid of any remaining bullets adn aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse
            pygame.mouse.set_visible(False)
        elif level_one_activated: 
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            self.stats.reset_stats()
            self.game_active=True
            # Get rid of any remaining bullets adn aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse
            pygame.mouse.set_visible(False)
        elif level_two_activated: 
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            self.settings.increase_speed()
            self.stats.reset_stats()
            self.game_active=True
            # Get rid of any remaining bullets adn aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse
            pygame.mouse.set_visible(False)
            
        
            
    def _fire_bullet(self):
        """Crete a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)   
             
    def _update_bullets(self):
        """Update postion of bullets adn get rigd fo old bullets"""
        #update bullet position
        self.bullets.update()
            # Get rigt of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)   
        # Check for any bullets that have hit aliens. if so, get rid of the bullet and the alien
        self._check_bullet_alien_collision()
    
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions"""
        # remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # If/when all the aliens are destroyed, destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
    def _update_aliens(self):
        """Update the postiions of all aliens in teh fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
            
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit. 
                self._ship_hit()
                break    
                      
    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row, reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop th entire fleet and chagne the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
            
    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()   
            self.aliens.draw(self.screen)  
            if not self.game_active:
                self.play_button.draw_button()
                self.level_one_button.draw_button()
                self.level_two_button.draw_button()
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
                self._fire_bullet()
        elif event.key == pygame.K_p and not self.game_active :
            # Start the game if the user presses P
            # Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active=True
            # Get rid of any remaining bullets adn aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse
            pygame.mouse.set_visible(False)
            
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
if __name__ == '__main__': #<-Only run if the file is called directly 
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
    print("Hello")
    