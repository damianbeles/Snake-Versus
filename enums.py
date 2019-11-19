import pygame

class EntityType:
    FREE = 0
    WALL = 1
    HEAD = 2
    TAIL = 3
    FOOD = 4

EntityPygameColor = [\
    pygame.Color('white'),\
    pygame.Color('black'),\
    pygame.Color('orange'),\
    pygame.Color('green'),\
    pygame.Color('red')]

class CustomEvent:
    FIRST_PLAYER_MOVE_EVENT, FIRST_PLAYER_MOVE_EVENT_TIMER = pygame.USEREVENT + 1, 100
    SECOND_PLAYER_MOVE_EVENT, SECOND_PLAYER_MOVE_EVENT_TIMER = pygame.USEREVENT + 2, 100

class Direction:
    EAST = [0, 1]
    SOUTH = [1, 0]
    WEST = [0, -1]
    NORTH = [-1, 0]

class Dimension:
    NUMBER_OF_ENTITIES_X = 32
    NUMBER_OF_ENTITIES_Y = 32
    ENTITY_WIDTH = 16
    ENTITY_HEIGHT = 16
    BOARD_WIDTH = NUMBER_OF_ENTITIES_X * ENTITY_WIDTH
    BOARD_HEIGHT = NUMBER_OF_ENTITIES_Y * ENTITY_HEIGHT
    ALIGNMENT = 2 * ENTITY_WIDTH
    SCREEN_WIDTH = ALIGNMENT + BOARD_WIDTH + ALIGNMENT + BOARD_WIDTH + ALIGNMENT
    SCREEN_HEIGHT = ALIGNMENT + BOARD_HEIGHT + ALIGNMENT
    FIRST_BOARD_TOP_LEFT_X = ALIGNMENT
    FIRST_BOARD_TOP_LEFT_Y = ALIGNMENT
    SECOND_BOARD_TOP_LEFT_X = 2 * ALIGNMENT + BOARD_WIDTH
    SECOND_BOARD_TOP_LEFT_Y = ALIGNMENT