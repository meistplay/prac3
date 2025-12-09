#pip install -r requirements.txt
#python src/main.py
import pygame
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.engine.game_engine import GameEngine

def main():
    """Главная функция запуска игры"""
    pygame.init()  # Инициализация библиотеки Pygame
    game = GameEngine()  # Создание игрового движка
    game.run()  # Запуск главного игрового цикла
    pygame.quit()  # Завершение работы Pygame
    sys.exit()  # Выход из программы

if __name__ == "__main__":
    main()