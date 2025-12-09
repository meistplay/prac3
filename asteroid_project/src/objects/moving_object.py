# Класс движущихся обьектов
from src.objects.game_object import GameObject

class MovingObject(GameObject):
    def __init__(self, x, y, width, height, speed):
        # Вызов конструктора родительского класса
        super().__init__(x, y, width, height)
        # Скорость движения (пикселей за кадр)
        self.speed = speed
        # Направление движения по осям (-1, 0, 1)
        self.dx = 0  # Направление по X: -1=влево, 0=стоп, 1=вправо
        self.dy = 0  # Направление по Y: -1=вверх, 0=стоп, 1=вниз
        
    def move(self):
        # Обновляет позицию объекта на основе направления и скорости
        self.x += self.dx * self.speed  # Движение по горизонтали
        self.y += self.dy * self.speed  # Движение по вертикали
