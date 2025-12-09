# Класс , от которого наследуются все игровые объекты/общий интерфейс: обновление, отрисовка, коллизии
import pygame

class GameObject:
    def __init__(self, x, y, width, height):
        # Позиция объекта в игровом мире
        self.x = x  # Координата X центра объекта
        self.y = y  # Координата Y центра объекта
        # Размеры объекта (используются для коллизий)
        self.width = width    # Ширина объекта
        self.height = height  # Высота объекта
        # если False, объект будет удален из игры
        self.active = True
        
    def update(self):
        # Вызывается каждый кадр для обновления состояния объекта
        pass
        
    def draw(self, surface):
        # Отрисовывает объект на переданной поверхности Pygame
        pass
        
    def get_rect(self):
        # Возвращает прямоугольник Pygame для обнаружения столкновений
        # Расчет от центра к краям (x - width/2)
        return pygame.Rect(self.x - self.width/2, self.y - self.height/2, 
                          self.width, self.height)
    
    def collides_with(self, other):
        # Проверяет столкновение с другим игровым объектом
        return self.get_rect().colliderect(other.get_rect())
