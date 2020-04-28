import json
import pygame

with open("settings.json") as json_file:
    settings_json = json.load(json_file)


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


def pygame_color_from_setting(color_obj):
    red = color_obj[0]
    green = color_obj[1]
    blue = color_obj[2]

    return pygame.Color(red, green, blue)


REV_KEYS = {"a": pygame.K_a, "b": pygame.K_b, "c": pygame.K_c, "d": pygame.K_d, "e": pygame.K_e, "f": pygame.K_f,
            "g": pygame.K_g, "h": pygame.K_h, "i": pygame.K_i, "j": pygame.K_j, "k": pygame.K_k, "l": pygame.K_l,
            "m": pygame.K_m, "n": pygame.K_n, "o": pygame.K_o, "p": pygame.K_p, "q": pygame.K_q, "r": pygame.K_r,
            "s": pygame.K_s, "t": pygame.K_t, "u": pygame.K_u, "v": pygame.K_v, "w": pygame.K_w, "x": pygame.K_x,
            "y": pygame.K_y,  "z": pygame.K_z, "↓": pygame.K_DOWN, "↑": pygame.K_UP, "←": pygame.K_LEFT, "→": pygame.K_RIGHT}


class Entity:

    class Type:
        FREE = 0
        WALL = 1
        HEAD = 2
        TAIL = 3
        FOOD = 4

    PygameColor = [[pygame.Color('white'),
                    pygame_color_from_setting(settings_json["first_player"]["skin"]["WALL"]),
                    pygame_color_from_setting(settings_json["first_player"]["skin"]["HEAD"]),
                    pygame_color_from_setting(settings_json["first_player"]["skin"]["TAIL"]),
                    pygame_color_from_setting(settings_json["first_player"]["skin"]["FOOD"])],
                   [pygame.Color('white'),
                    pygame_color_from_setting(settings_json["second_player"]["skin"]["WALL"]),
                    pygame_color_from_setting(settings_json["second_player"]["skin"]["HEAD"]),
                    pygame_color_from_setting(settings_json["second_player"]["skin"]["TAIL"]),
                    pygame_color_from_setting(settings_json["second_player"]["skin"]["FOOD"])]]

    WIDTH = settings_json["entity"]["width"]
    HEIGHT = settings_json["entity"]["height"]


class CustomEvent:

    FIRST_PLAYER_MOVE_EVENT = pygame.USEREVENT + 1
    FIRST_PLAYER_MOVE_EVENT_TIMER = settings_json["speed"]
    FIRST_PLAYER_LAST_PRESSED_KEY = REV_KEYS[settings_json["first_player"]["controls"][2]]

    SECOND_PLAYER_MOVE_EVENT = pygame.USEREVENT + 2
    SECOND_PLAYER_MOVE_EVENT_TIMER = settings_json["speed"]
    SECOND_PLAYER_LAST_PRESSED_KEY = REV_KEYS[settings_json["second_player"]["controls"][2]]


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

    NUMBER_OF_ENTITIES_X = settings_json["entity"]["nof_x"]
    NUMBER_OF_ENTITIES_Y = settings_json["entity"]["nof_y"]

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


def rgb_to_hex_color(rgb_color):
    return "#%02x%02x%02x" % (rgb_color[0], rgb_color[1], rgb_color[2])


def hex_to_rgb_color(hex_color):
    hex_color = hex_color.lstrip('#')
    lc = len(hex_color)
    return tuple(int(hex_color[i:i + lc // 3], 16) for i in range(0, lc, lc // 3))
