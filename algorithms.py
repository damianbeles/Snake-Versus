import numpy as np

from keras.layers.core import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import to_categorical

from player import Player
from snake import Snake
from utils import create_empty_board
from utils import CustomEvent
from utils import Dimension
from utils import Direction
from utils import Entity
from utils import settings_json
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


class DFS(Snake):

    def __init__(self):
        Snake.__init__(self)
        self.path = []

    def _advance(self):
        def DFS():
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

            visited_board = create_empty_board(0)
            parrent_board = create_empty_board(Point(0, 0).copy())
            stack = [self.head.copy()]

            last_calculated_pos = None

            while stack != []:
                cur_pos = stack[-1].copy()
                del stack[-1]

                if visited_board[cur_pos.row][cur_pos.col] != 1:
                    visited_board[cur_pos.row][cur_pos.col] = 1

                    for direction in Direction.directions:
                        new_pos = cur_pos + direction

                        if self.board[new_pos.row][new_pos.col] not in [Entity.Type.TAIL, Entity.Type.WALL] and\
                           visited_board[new_pos.row][new_pos.col] == 0:
                            parrent_board[new_pos.row][new_pos.col] = cur_pos
                            stack.append(new_pos)
                            last_calculated_pos = new_pos

                        if new_pos == self.food:
                            calculate_path(self.food.copy())
                            return

            if last_calculated_pos is not None:
                calculate_path(last_calculated_pos)
            else:
                self.path = [Direction.NORTH]

        if self.path == []:
            DFS()

        elif not self._canMoveTowards(self.head + self.path[0]):
            self.path = []
            DFS()

        if self.path != []:
            self._change_direction(self.path[0])
            del self.path[0]

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


class DQN(Snake):

    def __init__(self):
        Snake.__init__(self)

        self.drop_percantage = 0.15
        self.output_layer_size = 3
        self.hidden_layer_size = 120
        self.input_layer_size = 11

        self.reward = 0
        self.gamma = 0.9
        self.learning_rate = 0.0005
        self.model = self.network('dqn_after_500_games.hdf5')

        self.is_training = False

    def set_reward(self):
        self.reward = 0

        if self._is_dead:
            self.reward = -10

        elif self._has_eaten:
            self.reward = 10

    def network(self, weights=None):
        model = Sequential()

        model.add(Dense(input_dim=self.input_layer_size, units=self.hidden_layer_size, activation='relu'))
        model.add(Dropout(self.drop_percantage))

        model.add(Dense(units=self.hidden_layer_size, activation='relu'))
        model.add(Dropout(self.drop_percantage))

        model.add(Dense(units=self.hidden_layer_size, activation='relu'))
        model.add(Dropout(self.drop_percantage))

        model.add(Dense(units=self.output_layer_size, activation='softmax'))

        model.compile(loss='mse', optimizer=Adam(self.learning_rate))

        if weights is not None:
            model.load_weights(weights)

        return model

    def get_state(self):
        straight = self.head + self.direction
        left = self.head + Direction.lefts[self.direction]
        right = self.head + Direction.rights[self.direction]

        state = [
            self.board[straight.row][straight.col] in [Entity.Type.WALL, Entity.Type.TAIL],
            self.board[left.row][left.col] in [Entity.Type.WALL, Entity.Type.TAIL],
            self.board[right.row][right.col] in [Entity.Type.WALL, Entity.Type.TAIL],

            self.direction == Direction.WEST,
            self.direction == Direction.EAST,
            self.direction == Direction.NORTH,
            self.direction == Direction.SOUTH,

            self.food.col < self.head.col,
            self.food.col > self.head.col,
            self.food.row < self.head.row,
            self.food.row > self.head.row
        ]

        for index in range(len(state)):
            state_value = 0

            if state[index] is True:
                state_value = 1

            state[index] = state_value

        return np.array(state)

    def _advance(self):
        self.old_state = self.get_state()
        prediction = self.model.predict(self.old_state.reshape((1, self.input_layer_size)))
        self.next = to_categorical(np.argmax(prediction[0]), num_classes=self.output_layer_size)

        if np.array_equal(self.next, [0, 0, 1]):
            self._change_direction(Direction.rights[self.direction])
        elif np.array_equal(self.next, [0, 1, 0]):
            self._change_direction(Direction.lefts[self.direction])

    def _post_advance(self):
        if not self.is_training:
            return

        self.new_state = self.get_state()
        self.set_reward()

        target = self.reward
        if not self._is_dead:
            predict = self.model.predict(self.new_state.reshape((1, self.input_layer_size)))
            target = self.reward + self.gamma * np.amax(predict[0])

        target_f = self.model.predict(self.old_state.reshape((1, self.input_layer_size)))
        target_f[0][np.argmax(self.next)] = target

        self.model.fit(self.old_state.reshape((1, self.input_layer_size)), target_f, epochs=1, verbose=0)

    def _save(self):
        self.model.save_weights('weights.hdf5')


class Human(Snake):

    def __init__(self):
        Snake.__init__(self)

    def _advance(self):
        player = "first_player"
        current_player_key = CustomEvent.FIRST_PLAYER_LAST_PRESSED_KEY

        if self.id == 1:
            player = "second_player"
            current_player_key = CustomEvent.SECOND_PLAYER_LAST_PRESSED_KEY

        DirectionMap = {0: Direction.WEST, 1: Direction.SOUTH, 2: Direction.EAST, 3: Direction.NORTH}

        for index in [0, 1, 2, 3]:
            if settings_json[player]["controls"][index] == Player.KEYS[current_player_key]:
                self._change_direction(DirectionMap[index])

    def _post_advance(self):
        pass

    def _save(self):
        pass
