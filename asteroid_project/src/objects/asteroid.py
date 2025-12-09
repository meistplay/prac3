import pygame
import math
import random
from src.objects.moving_object import MovingObject
class Asteroid(MovingObject):
    def __init__(self, x, y, size=3, can_split=True, graphics_config=None):
        sizes = {3: 50, 2: 35, 1: 20}  
        if graphics_config and 'asteroid_sizes' in graphics_config.get('sizes', {}):
            asteroid_sizes = graphics_config['sizes']['asteroid_sizes']
            sizes = {3: asteroid_sizes.get('3', 50),2: asteroid_sizes.get('2', 35),1: asteroid_sizes.get('1', 20)}    
        speed = {3: 1.5, 2: 2.0, 1: 2.5}    
        super().__init__(x, y, sizes[size], sizes[size], speed[size])
        self.size = size
        self.can_split = can_split
        self.base_speed = speed[size]
        self.points = {3: 20, 2: 30, 1: 50}[size]
        self.dy = 1
        self.dx = random.uniform(-0.3, 0.3)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-3, 3)
    def update(self):
        self.move()
        self.rotation += self.rotation_speed
        if self.y > 800 + self.height:
            self.active = False 
    def draw(self, surface):
        points = []
        for i in range(8):
            angle = 2 * math.pi * i / 8 + math.radians(self.rotation)
            radius = self.width / 2 * random.uniform(0.8, 1.2)
            points.append((
                self.x + math.cos(angle) * radius,
                self.y + math.sin(angle) * radius
            ))
        pygame.draw.polygon(surface, (255, 0, 0), points)
        pygame.draw.polygon(surface, (200, 0, 0), points, 2)
    def split(self):
        if self.size == 3 and self.can_split:
            return [
                Asteroid(self.x, self.y, 2, False),
                Asteroid(self.x, self.y, 1, False)
            ]
        return []