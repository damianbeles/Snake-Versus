import pygame

from utils import Entity


class Player:

    KEYS = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f",
            pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l",
            pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r",
            pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x",
            pygame.K_y: "y", pygame.K_z: "z", pygame.K_DOWN: "↓", pygame.K_UP: "↑", pygame.K_LEFT: "←", pygame.K_RIGHT: "→"}

    def __init__(self, draw_offset_x, draw_offset_y, snake, player_id):
        self.draw_offset_x = draw_offset_x - 1
        self.draw_offset_y = draw_offset_y - 1
        self._snake = snake
        self.player_id = player_id
        self._snake.id = player_id

    def draw_on_display(self, game_window):
        for npos in range(len(self._snake.board)):
            for mpos in range(len(self._snake.board[0])):
                pygame.draw.rect(game_window,
                                 Entity.PygameColor[self.player_id][self._snake.board[npos][mpos]],
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
