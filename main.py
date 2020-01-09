import algorithms
import pygame

from datetime import datetime
from player import Player
from utils import CustomEvent
from utils import Dimension

FIRST_PLAYER_ALGORITHM = algorithms.GreedyChoosing
SECOND_PLAYER_ALGORITHM = algorithms.Lee

REPORT_FILE_NAME = f"{datetime.now():%d_%m_%Y___%H_%M_%S}.csv"
with open(REPORT_FILE_NAME, 'w') as fout:
    fout.write(f"{FIRST_PLAYER_ALGORITHM.__name__}, {SECOND_PLAYER_ALGORITHM.__name__}")


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


def generate_new_players():
    players = [Player(Dimension.FIRST_BOARD_TOP_LEFT_X,
                      Dimension.FIRST_BOARD_TOP_LEFT_Y,
                      FIRST_PLAYER_ALGORITHM()),
               Player(Dimension.SECOND_BOARD_TOP_LEFT_X,
                      Dimension.SECOND_BOARD_TOP_LEFT_Y,
                      SECOND_PLAYER_ALGORITHM())]

    players[0].snake.set_enemy(players[1].snake)
    players[1].snake.set_enemy(players[0].snake)

    return players


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Snake Versus Prototype')

    game_window = init_game_window()

    pygame.time.set_timer(CustomEvent.FIRST_PLAYER_MOVE_EVENT,
                          CustomEvent.FIRST_PLAYER_MOVE_EVENT_TIMER)
    pygame.time.set_timer(CustomEvent.SECOND_PLAYER_MOVE_EVENT,
                          CustomEvent.SECOND_PLAYER_MOVE_EVENT_TIMER)

    players = generate_new_players()

    running = True
    while running:
        for player in players:
            player.draw_on_display(game_window)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    players = generate_new_players()

            if event.type == CustomEvent.FIRST_PLAYER_MOVE_EVENT:
                players[0].snake.move()

            if event.type == CustomEvent.SECOND_PLAYER_MOVE_EVENT:
                players[1].snake.move()

            if players[0].snake._is_dead and players[1].snake._is_dead:
                with open(REPORT_FILE_NAME, 'a') as fout:
                    fout.write(f"\n{len(players[0].snake.tail)}, {len(players[1].snake.tail)}")

                players = generate_new_players()

    pygame.quit()
