import pygame

from algorithms import GreedyChoosing
from algorithms import Lee
from player import Player
from utils import CustomEvent
from utils import Dimension


def init_game_window():
    game_window = pygame.display.set_mode([Dimension.SCREEN_WIDTH,
                                           Dimension.SCREEN_HEIGHT])
    game_window.fill(pygame.Color('white'))

    pygame.draw.rect(game_window,
                     pygame.Color('black'),
                     [Dimension.FIRST_BOARD_TOP_LEFT_X - 2,
                      Dimension.FIRST_BOARD_TOP_LEFT_Y - 2,
                      Dimension.BOARD_WIDTH + 1,
                      Dimension.BOARD_HEIGHT + 1],
                     True)

    pygame.draw.rect(game_window,
                     pygame.Color('black'),
                     [Dimension.SECOND_BOARD_TOP_LEFT_X - 2,
                      Dimension.SECOND_BOARD_TOP_LEFT_Y - 2,
                      Dimension.BOARD_WIDTH + 1,
                      Dimension.BOARD_HEIGHT + 1],
                     True)

    return game_window


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Snake Versus Prototype')

    game_window = init_game_window()

    pygame.time.set_timer(CustomEvent.FIRST_PLAYER_MOVE_EVENT,
                          CustomEvent.FIRST_PLAYER_MOVE_EVENT_TIMER)
    pygame.time.set_timer(CustomEvent.SECOND_PLAYER_MOVE_EVENT,
                          CustomEvent.SECOND_PLAYER_MOVE_EVENT_TIMER)

    players = [Player(Dimension.FIRST_BOARD_TOP_LEFT_X,
                      Dimension.FIRST_BOARD_TOP_LEFT_Y,
                      GreedyChoosing()),
               Player(Dimension.SECOND_BOARD_TOP_LEFT_X,
                      Dimension.SECOND_BOARD_TOP_LEFT_Y,
                      Lee())]

    players[0].snake.set_enemy(players[1].snake)
    players[1].snake.set_enemy(players[0].snake)

    running = True
    while running:
        for player in players:
            player.draw_on_display(game_window)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == CustomEvent.FIRST_PLAYER_MOVE_EVENT:
                players[0].snake.advance()
                players[0].snake.move()

            if event.type == CustomEvent.SECOND_PLAYER_MOVE_EVENT:
                players[1].snake.advance()
                players[1].snake.move()

    pygame.quit()
