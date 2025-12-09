import pygame

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw(self, surface):
        title = self.font.render("ASTEROIDS DEFENSE", True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(400, 200)))
        
        start = self.small_font.render("Press R to start game", True, (200, 200, 200))
        surface.blit(start, start.get_rect(center=(400, 300)))
        
        scores = self.small_font.render("Press T to view high scores", True, (200, 200, 200))
        surface.blit(scores, scores.get_rect(center=(400, 350)))
        
        controls = "Controls: ARROWS to move, SPACE to shoot, P to pause"
        controls_text = self.small_font.render(controls, True, (150, 150, 150))
        surface.blit(controls_text, controls_text.get_rect(center=(400, 450)))