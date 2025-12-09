import pygame
import random
import json
import os
from src.objects.player import Player
from src.objects.asteroid import Asteroid
from src.objects.projectile import Projectile
from src.ui.hud import UI
from src.ui.menu import Menu

class GameEngine:
    def __init__(self):
        self.game_config = self.load_config('src/config/game_config.json')
        self.graphics_config = self.load_config('src/config/graphics.json')
        
        screen_width = self.game_config['game']['screen_width']
        screen_height = self.game_config['game']['screen_height']
        title = self.game_config['game']['title']
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"
        
        initial_lives = self.game_config['game']['initial_lives']
        self.player = Player(screen_width // 2, screen_height - 50, 
                           initial_lives, self.graphics_config)
        self.player.screen_width = screen_width
        
        self.projectiles = []
        self.asteroids = []
        self.ui = UI()
        self.menu = Menu()
        
        self.spawn_timer = 0
        self.spawn_interval = 180
        self.wave_count = 0
        self.max_asteroids = 5
        
        self.high_scores = self.load_high_scores()
        self.difficulty_level = 1
        self.speed_multiplier = 1.0
        
        self.spawn_wave(2)
    
    def load_config(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки {file_path}: {e}")
            return {}
    
    def load_high_scores(self):
        try:
            if os.path.exists('high_scores.json'):
                with open('high_scores.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_high_score(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)
    
    def update_difficulty(self):
        if self.player.score >= 5000:
            self.difficulty_level, self.speed_multiplier = 3, 1.8
        elif self.player.score >= 2000:
            self.difficulty_level, self.speed_multiplier = 2, 1.4
        else:
            self.difficulty_level, self.speed_multiplier = 1, 1.0
        
        for asteroid in self.asteroids:
            asteroid.speed = asteroid.base_speed * self.speed_multiplier
    
    def spawn_asteroid(self):
        screen_width = self.game_config['game']['screen_width']
        x = random.uniform(50, screen_width - 50)
        asteroid = Asteroid(x, -30, 3, True, self.graphics_config)
        asteroid.speed = asteroid.base_speed * self.speed_multiplier
        self.asteroids.append(asteroid)
    
    def spawn_wave(self, count):
        for _ in range(min(count, self.max_asteroids - len(self.asteroids))):
            self.spawn_asteroid()
        self.wave_count += 1
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "high_scores":
                        self.game_state = "menu"
                    else:
                        self.running = False
                elif event.key == pygame.K_p and self.game_state in ["playing", "paused"]:
                    self.game_state = "paused" if self.game_state == "playing" else "playing"
                elif event.key == pygame.K_r and self.game_state in ["menu", "game_over"]:
                    self.start_game()
                elif event.key == pygame.K_t and self.game_state in ["menu", "game_over"]:
                    self.game_state = "high_scores"
                elif event.key == pygame.K_SPACE and self.game_state == "playing":
                    # ПЕРЕДАЕМ graphics_config в shoot()
                    if projectile := self.player.shoot(self.graphics_config):
                        self.projectiles.append(projectile)
    
    def start_game(self):
        screen_width = self.game_config['game']['screen_width']
        screen_height = self.game_config['game']['screen_height']
        initial_lives = self.game_config['game']['initial_lives']
        
        self.player = Player(screen_width // 2, screen_height - 50, 
                           initial_lives, self.graphics_config)
        self.player.screen_width = screen_width
        self.projectiles.clear()
        self.asteroids.clear()
        self.game_state = "playing"
        self.wave_count = 0
        self.difficulty_level = 1
        self.speed_multiplier = 1.0
        self.spawn_wave(2)
    
    def update(self):
        if self.game_state != "playing":
            return
            
        self.update_difficulty()
        self.player.update()
        
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.active:
                self.projectiles.remove(projectile)
        
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if not asteroid.active:
                self.asteroids.remove(asteroid)
                continue
            
            if asteroid.collides_with(self.player) and self.player.take_damage():
                if self.player.lives <= 0:
                    if self.player.score > 0:
                        self.save_high_score(self.player.score)
                    self.game_state = "game_over"
            
            for projectile in self.projectiles[:]:
                if asteroid.collides_with(projectile):
                    self.player.score += asteroid.points
                    self.asteroids.remove(asteroid)
                    self.projectiles.remove(projectile)
                    
                    for new_asteroid in asteroid.split():
                        new_asteroid.speed = new_asteroid.base_speed * self.speed_multiplier
                        self.asteroids.append(new_asteroid)
                    break
        
        self.spawn_timer += 1
        if (self.spawn_timer >= self.spawn_interval and 
            len(self.asteroids) < self.max_asteroids - 1):
            self.spawn_wave(random.randint(1, min(3, 1 + self.wave_count // 5)))
            self.spawn_timer = 0
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if self.game_state == "menu":
            self.menu.draw(self.screen)
        elif self.game_state == "high_scores":
            self.ui.draw_high_scores(self.screen, self.high_scores)
        else:
            for obj in self.asteroids + self.projectiles:
                obj.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw(self.screen, self.player, self.game_state, self.difficulty_level)
        
        pygame.display.flip()
    
    def run(self):
        fps = self.game_config['game']['fps']
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(fps)