from snake import Snake
from utils import Dimension
from utils import Direction
from utils import Entity


class GreedyChoosing(Snake):

    def __init__(self):
        Snake.__init__(self)

    def advance(self):
        min_direction = Dimension.NUMBER_OF_ENTITIES_Y + Dimension.NUMBER_OF_ENTITIES_X
        mini_direction = None

        def heuristic(new_pos):
            if self.board[new_pos.row][new_pos.col] == Entity.Type.FOOD:
                return 0
            return abs(new_pos.row - self.food.row) + abs(new_pos.col - self.food.col)

        for npos in range(len(Direction.directions)):
            new_pos = self.head + Direction.directions[npos]

            if self._canMoveTowards(new_pos) and\
               heuristic(new_pos) < min_direction:
                min_direction = heuristic(new_pos)
                mini_direction = npos

        if mini_direction is not None:
            self._change_direction(Direction.directions[mini_direction])
