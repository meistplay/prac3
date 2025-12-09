from src.objects.moving_object import MovingObject
import pygame

class Projectile(MovingObject):
    def __init__(self, x, y, graphics_config=None):
        projectile_width = 8
        projectile_height = 16
        
        if graphics_config and 'sizes' in graphics_config:
            sizes = graphics_config['sizes']
            projectile_width = sizes.get('projectile_width', 8)
            projectile_height = sizes.get('projectile_height', 16)
        
        super().__init__(x, y, projectile_width, projectile_height, 8)
        self.dy = -1
        self.lifetime = 90
        
    def update(self):
        self.move()
        self.lifetime -= 1
        if self.lifetime <= 0 or self.y < 0:
            self.active = False
            
    def draw(self, surface):
        bullet_rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, 
                                 self.width, self.height)
        pygame.draw.rect(surface, (255, 255, 0), bullet_rect)
        
        glow_rect = pygame.Rect(self.x - self.width/2 - 2, self.y - self.height/2 - 2,
                               self.width + 4, self.height + 4)
        pygame.draw.rect(surface, (255, 255, 100), glow_rect, 1)