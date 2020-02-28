from snake import Snake
from utils import create_empty_board
from utils import Dimension
from utils import Direction
from utils import Entity
from utils import Point


class GreedyChoosing(Snake):

    def __init__(self):
        Snake.__init__(self)

    def _advance(self):
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

    def _post_advance(self):
        pass

    def _save(self):
        pass


class Lee(Snake):

    def __init__(self):
        Snake.__init__(self)
        self.path = []

    def _advance(self):
        def Lee():
            def calculate_path(target):
                start = self.head.copy()

                cur_path = [target]
                while target != start:
                    target = parrent_board[target.row][target.col]
                    cur_path.append(target)

                for index in range(len(cur_path) - 1, 0, -1):
                    for direction in Direction.directions:
                        if cur_path[index] + direction == cur_path[index - 1]:
                            self.path.append(direction)

            queue = [self.head.copy()]
            index = 0

            visited_board = create_empty_board(0)
            parrent_board = create_empty_board(Point(0, 0).copy())

            while index < len(queue):
                cur_pos = queue[index]

                for direction in Direction.directions:
                    new_pos = cur_pos + direction

                    if visited_board[new_pos.row][new_pos.col] == 0 and\
                       self._canMoveTowards(new_pos):
                        visited_board[new_pos.row][new_pos.col] = visited_board[cur_pos.row][cur_pos.col] + 1
                        parrent_board[new_pos.row][new_pos.col] = cur_pos
                        queue.append(new_pos)

                    if new_pos == self.food:
                        calculate_path(self.food.copy())
                        return

                index += 1

            calculate_path(queue[-1])

        if self.path == []:
            Lee()

        elif not self._canMoveTowards(self.head + self.path[0]):
            self.path = []
            Lee()

        if self.path != []:
            self._change_direction(self.path[0])
            del self.path[0]

    def _post_advance(self):
        pass

    def _save(self):
        pass

