class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initializes statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # high score should not be reset
        self.high_score = 0

        
    def reset_stats(self):
        """Initialize statistics that can chagne durin the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    
    