import algorithms
import pygame

from datetime import datetime
from player import Player
from utils import CustomEvent
from utils import Dimension
from utils import Entity

FIRST_PLAYER_ALGORITHM = algorithms.GreedyChoosing
SECOND_PLAYER_ALGORITHM = algorithms.GreedyChoosing

REPORT_FILE_NAME = f"reports/{datetime.now():%d_%m_%Y___%H_%M_%S}.csv"
with open(REPORT_FILE_NAME, 'w') as fout:
    fout.write(f"{FIRST_PLAYER_ALGORITHM.__name__},{SECOND_PLAYER_ALGORITHM.__name__},Winner")


def init_game_window():
    game_window = pygame.display.set_mode([Dimension.SCREEN_WIDTH,
                                           Dimension.SCREEN_HEIGHT])
    game_window.fill(Entity.PygameColor[Entity.Type.FREE])

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


def play_new_game(players):
    players[0].play()
    players[1].play()

    players[0].set_enemy(players[1])
    players[1].set_enemy(players[0])


def generate_report_entry(players):
    with open(REPORT_FILE_NAME, 'a') as fout:
        if players[0].get_score() > players[1].get_score():
            winner = "first"
        elif players[0].get_score() == players[1].get_score():
            winner = "tie"
        else:
            winner = "second"
        fout.write(f"\n{players[0].get_score()},{players[1].get_score()},{winner}")


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Snake Versus Prototype')

    players = [Player(Dimension.FIRST_BOARD_TOP_LEFT_X,
                      Dimension.FIRST_BOARD_TOP_LEFT_Y,
                      FIRST_PLAYER_ALGORITHM()),
               Player(Dimension.SECOND_BOARD_TOP_LEFT_X,
                      Dimension.SECOND_BOARD_TOP_LEFT_Y,
                      SECOND_PLAYER_ALGORITHM())]
    
    play_new_game(players)

    game_window = init_game_window()

    pygame.time.set_timer(CustomEvent.FIRST_PLAYER_MOVE_EVENT,
                          CustomEvent.FIRST_PLAYER_MOVE_EVENT_TIMER)
    pygame.time.set_timer(CustomEvent.SECOND_PLAYER_MOVE_EVENT,
                          CustomEvent.SECOND_PLAYER_MOVE_EVENT_TIMER)

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
                    play_new_game(players)

            if event.type == CustomEvent.FIRST_PLAYER_MOVE_EVENT:
                players[0].move()

            if event.type == CustomEvent.SECOND_PLAYER_MOVE_EVENT:
                players[1].move()

        if players[0].is_dead() and\
            players[1].is_dead():
            generate_report_entry(players)

            play_new_game(players)

    players[0].save()
    players[1].save()
    pygame.quit()
