import random

from abc import ABC
from abc import abstractmethod
from utils import create_empty_board
from utils import Dimension
from utils import Direction
from utils import Entity
from utils import Point


class Snake(ABC):

    def __init__(self):
        self.board = create_empty_board(Entity.Type.FREE)

        self.head = Point(0, 0)
        self.tail = []

        self.direction = Direction.EAST

        self.enemy = self

        self.food = Point(random.randint(1, Dimension.NUMBER_OF_ENTITIES_Y - 1),
                          random.randint(1, Dimension.NUMBER_OF_ENTITIES_X - 1))

        self.board[self.head.row][self.head.col] = Entity.Type.HEAD
        self.board[self.food.row][self.food.col] = Entity.Type.FOOD

        self._is_dead = False

    def set_wall(self, wall_pos):
        if self.board[wall_pos.row][wall_pos.col] == Entity.Type.FREE:
            self.board[wall_pos.row][wall_pos.col] = Entity.Type.WALL

    def _change_direction(self, new_direction):
        if self.direction + new_direction != Point(0, 0):
            self.direction = new_direction

    def _canMoveTowards(self, new_pos):
        return self.board[new_pos.row][new_pos.col] == Entity.Type.FREE or\
            self.board[new_pos.row][new_pos.col] == Entity.Type.FOOD

    def move(self):
        if not self._is_dead:
            self._move()

    @abstractmethod
    def _advance(self):
        pass

    def _move(self):
        self._advance()

        new_pos = self.head + self.direction

        def eatsByMoving(new_pos):
            return self.board[new_pos.row][new_pos.col] == Entity.Type.FOOD

        def diesByMoving(new_pos):
            return self.board[new_pos.row][new_pos.col] == Entity.Type.WALL or\
                self.board[new_pos.row][new_pos.col] == Entity.Type.TAIL

        if not diesByMoving(new_pos):
            if eatsByMoving(new_pos):
                self.tail.insert(0, self.head)
                self.enemy.set_wall(self.food)

                self.board[self.head.row][self.head.col] = Entity.Type.TAIL
                self.head = new_pos

                food_possibilities = []
                for npos in range(len(self.board)):
                    for mpos in range(len(self.board[0])):
                        if self.board[npos][mpos] == Entity.Type.FREE:
                            food_possibilities.append(Point(npos, mpos))
                self.food = food_possibilities[random.randint(0, len(food_possibilities) - 1)]
                self.board[self.food.row][self.food.col] = Entity.Type.FOOD

            else:
                self.tail.insert(0, self.head)

                self.board[self.head.row][self.head.col] = Entity.Type.TAIL
                self.head = new_pos

                self.board[self.tail[-1].row][self.tail[-1].col] = Entity.Type.FREE
                del self.tail[-1]

            self.board[new_pos.row][new_pos.col] = Entity.Type.HEAD

        else:
            self._is_dead = True
