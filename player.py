import enums
import pygame

class Player:
    def __init__(self, draw_offset_x, draw_offset_y, snake):
        self.draw_offset_x = draw_offset_x - 1
        self.draw_offset_y = draw_offset_y - 1
        self.snake = snake

    def draw_on_display(self, game_window):
        for npos in range(len(self.snake.board)):
            for mpos in range(len(self.snake.board[0])):
                pygame.draw.rect(game_window, enums.EntityPygameColor[self.snake.board[npos][mpos]],\
                    [\
                        self.draw_offset_x + enums.Dimension.ENTITY_WIDTH * mpos,\
                        self.draw_offset_y + enums.Dimension.ENTITY_HEIGHT * npos,\
                        enums.Dimension.ENTITY_WIDTH - 1,\
                        enums.Dimension.ENTITY_HEIGHT - 1\
                    ], False)