import pygame
from src.objects.moving_object import MovingObject
from src.objects.projectile import Projectile

class Player(MovingObject):
    def __init__(self, x, y, initial_lives=3, graphics_config=None):
        player_width = 50
        player_height = 30
        if graphics_config and 'sizes' in graphics_config:
            sizes = graphics_config['sizes']
            player_width = sizes.get('player_width', 50)
            player_height = sizes.get('player_height', 30)

        super().__init__(x, y, player_width, player_height, 5)
        self.lives = initial_lives
        self.score = 0
        self.shoot_cooldown = 0
        self.invincible = 0
        self.screen_width = 800
    def update(self):
        keys = pygame.key.get_pressed()
        self.dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.move()
        self.x = max(self.width/2, min(self.screen_width - self.width/2, self.x))
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if self.invincible > 0:
            self.invincible -= 1
        
    def draw(self, surface):
        if self.invincible > 0 and self.invincible % 10 < 5:
            return
            
        ship_rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, 
                               self.width, self.height)
        pygame.draw.rect(surface, (0, 255, 0), ship_rect)
        
        points = [
            (self.x - self.width/2, self.y - self.height/2),
            (self.x + self.width/2, self.y - self.height/2),
            (self.x, self.y - self.height)
        ]
        pygame.draw.polygon(surface, (0, 200, 0), points)
        
    def shoot(self, graphics_config=None):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            return Projectile(self.x, self.y - self.height, graphics_config)
        return None
        
    def take_damage(self):
        if self.invincible == 0:
            self.lives -= 1
            self.invincible = 120
            return True
        return False