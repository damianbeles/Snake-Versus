import pygame

from utils import Entity


class Player:

    def __init__(self, draw_offset_x, draw_offset_y, snake):
        self.draw_offset_x = draw_offset_x - 1
        self.draw_offset_y = draw_offset_y - 1
        self._snake = snake

    def draw_on_display(self, game_window):
        for npos in range(len(self._snake.board)):
            for mpos in range(len(self._snake.board[0])):
                pygame.draw.rect(game_window,
                                 Entity.PygameColor[self._snake.board[npos][mpos]],
                                 [self.draw_offset_x + Entity.WIDTH * mpos,
                                  self.draw_offset_y + Entity.HEIGHT * npos,
                                  Entity.WIDTH - 1,
                                  Entity.HEIGHT - 1],
                                 False)

    def move(self):
        self._snake.move()

    def set_enemy(self, enemy):
        self._snake.enemy = enemy._snake

    def is_dead(self):
        return self._snake._is_dead

    def get_score(self):
        return len(self._snake.tail)

    def play(self):
        self._snake.play()
    
    def save(self):
        self._snake.save()
