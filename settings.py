class Settings:
    """A class to store all the settings"""
    def __init__(self):
        """Initialize the game's settings"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Alien settings
        self.fleet_drop_speed = 10
        # self.fleet_drop_speed = 100
        # How quickly the game speeds up
        self.speedup_scale = 2.0
        # How quickly the alien point values increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        self.button_width = 200
        self.button_height = 50
        
    def initialize_dynamic_settings(self):
        """initialize the settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 1.0
        self.alien_points = 50
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(f"increased alien points to {self.alien_points}")
        