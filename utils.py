import pygame


class Point:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, other):
        return Point((self.row + other.row) % Dimension.NUMBER_OF_ENTITIES_Y,
                     (self.col + other.col) % Dimension.NUMBER_OF_ENTITIES_X)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple([self.row, self.col]))

    def copy(self):
        return Point(self.row, self.col)


class Entity:

    class Type:
        FREE = 0
        WALL = 1
        HEAD = 2
        TAIL = 3
        FOOD = 4

    PygameColor = [pygame.Color('white'),
                   pygame.Color('black'),
                   pygame.Color('orange'),
                   pygame.Color('green'),
                   pygame.Color('red')]

    WIDTH = 16
    HEIGHT = 16


class CustomEvent:

    FIRST_PLAYER_MOVE_EVENT = pygame.USEREVENT + 1
    FIRST_PLAYER_MOVE_EVENT_TIMER = 1

    SECOND_PLAYER_MOVE_EVENT = pygame.USEREVENT + 2
    SECOND_PLAYER_MOVE_EVENT_TIMER = 1


class Direction:

    EAST = Point(0, 1)
    SOUTH = Point(1, 0)
    WEST = Point(0, -1)
    NORTH = Point(-1, 0)

    directions = [EAST, SOUTH, WEST, NORTH]

    rights = {
        NORTH: EAST,
        EAST: SOUTH,
        SOUTH: WEST,
        WEST: NORTH
    }

    lefts = {
        NORTH: WEST,
        WEST: SOUTH,
        SOUTH: EAST,
        EAST: NORTH
    }


class Dimension:

    NUMBER_OF_ENTITIES_X = 32
    NUMBER_OF_ENTITIES_Y = 32

    BOARD_WIDTH = NUMBER_OF_ENTITIES_X * Entity.WIDTH
    BOARD_HEIGHT = NUMBER_OF_ENTITIES_Y * Entity.HEIGHT

    WIDTH_ALIGNMENT = 2 * Entity.WIDTH
    HEIGHT_ALIGNMENT = 2 * Entity.HEIGHT

    SCREEN_WIDTH = 3 * WIDTH_ALIGNMENT + 2 * BOARD_WIDTH
    SCREEN_HEIGHT = 2 * HEIGHT_ALIGNMENT + BOARD_HEIGHT

    FIRST_BOARD_TOP_LEFT_X = WIDTH_ALIGNMENT
    FIRST_BOARD_TOP_LEFT_Y = HEIGHT_ALIGNMENT

    SECOND_BOARD_TOP_LEFT_X = 2 * WIDTH_ALIGNMENT + BOARD_WIDTH
    SECOND_BOARD_TOP_LEFT_Y = HEIGHT_ALIGNMENT

    BOARD_SIZE = [int(BOARD_WIDTH / Entity.WIDTH),
                  int(BOARD_HEIGHT / Entity.HEIGHT)]


def create_empty_board(default_value):
    return [[default_value] * Dimension.BOARD_SIZE[0] for _ in range(Dimension.BOARD_SIZE[1])]
