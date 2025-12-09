import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw(self, surface, player, game_state, difficulty_level=1):
        score_text = self.font.render(f"Score: {player.score}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        surface.blit(lives_text, (10, 50))
        
        difficulty_names = {1: "NORMAL", 2: "HARD", 3: "EXTREME"}
        difficulty_color = {1: (0, 255, 0), 2: (255, 165, 0), 3: (255, 0, 0)}
        diff_text = self.small_font.render(f"Difficulty: {difficulty_names[difficulty_level]}", 
                                         True, difficulty_color[difficulty_level])
        surface.blit(diff_text, (10, 90))      
        if game_state == "game_over":
            self._draw_centered(surface, "GAME OVER - Press R to restart", self.font)
            self._draw_centered(surface, "Press T to view high scores", self.small_font, 40)
        elif game_state == "paused":
            self._draw_centered(surface, "PAUSED - Press P to continue", self.font)
        controls = "Controls: LEFT/RIGHT - Move, SPACE - Shoot, P - Pause"
        controls_text = self.small_font.render(controls, True, (200, 200, 200))
        surface.blit(controls_text, (10, 570))
    def _draw_centered(self, surface, text, font, offset=0):
        text_surface = font.render(text, True, (255, 255, 255))
        rect = text_surface.get_rect(center=(400, 300 + offset))
        surface.blit(text_surface, rect)
    def draw_high_scores(self, surface, high_scores):
        title = pygame.font.Font(None, 48).render("HIGH SCORES", True, (255, 255, 0))
        surface.blit(title, title.get_rect(center=(400, 80)))
        if not high_scores:
            self._draw_centered(surface, "No scores yet!", self.font)
        else:
            for i, score in enumerate(high_scores):
                score_text = self.font.render(f"{i+1}. {score}", True, (255, 255, 255))
                rect = score_text.get_rect(center=(400, 150 + i * 40))
                surface.blit(score_text, rect)
        back_text = self.small_font.render("Press ESC to return to menu", True, (200, 200, 200))
        surface.blit(back_text, back_text.get_rect(center=(400, 550)))