import enums
import pygame

from algorithms import GreedyChoosing
from player import Player

def init_game_window():
    game_window = pygame.display.set_mode(
        [
            enums.Dimension.SCREEN_WIDTH,\
            enums.Dimension.SCREEN_HEIGHT\
        ])
    game_window.fill(pygame.Color('white'))

    pygame.draw.rect(game_window, pygame.Color('black'),\
        [
            enums.Dimension.FIRST_BOARD_TOP_LEFT_X - 2,\
            enums.Dimension.FIRST_BOARD_TOP_LEFT_Y -2,\
            enums.Dimension.BOARD_WIDTH + 1,\
            enums.Dimension.BOARD_HEIGHT + 1\
        ], True)
    
    pygame.draw.rect(game_window, pygame.Color('black'),\
        [
            enums.Dimension.SECOND_BOARD_TOP_LEFT_X - 2,\
            enums.Dimension.SECOND_BOARD_TOP_LEFT_Y -2,\
            enums.Dimension.BOARD_WIDTH + 1,\
            enums.Dimension.BOARD_HEIGHT + 1\
        ], True)

    return game_window

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Snake Versus Prototype')

    game_window = init_game_window()

    pygame.time.set_timer(enums.CustomEvent.FIRST_PLAYER_MOVE_EVENT, 10)#enums.CustomEvent.FIRST_PLAYER_MOVE_EVENT_TIMER)
    pygame.time.set_timer(enums.CustomEvent.SECOND_PLAYER_MOVE_EVENT, 10)#enums.CustomEvent.SECOND_PLAYER_MOVE_EVENT_TIMER)

    players =\
        [
            Player(\
                enums.Dimension.FIRST_BOARD_TOP_LEFT_X,\
                enums.Dimension.FIRST_BOARD_TOP_LEFT_Y,\
                GreedyChoosing()\
            ),\
            Player(\
                enums.Dimension.SECOND_BOARD_TOP_LEFT_X,\
                enums.Dimension.SECOND_BOARD_TOP_LEFT_Y,\
                GreedyChoosing()\
            )
        ]

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
            
            if event.type == enums.CustomEvent.FIRST_PLAYER_MOVE_EVENT:
                players[0].snake.advance()
                players[0].snake.move()

            if event.type == enums.CustomEvent.SECOND_PLAYER_MOVE_EVENT:
                players[1].snake.advance()
                players[1].snake.move()

    pygame.quit()