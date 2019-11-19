import enums
import pygame
import random

class Snake:
    def __init__(self):
        BOARD_SIZE = [int(enums.Dimension.BOARD_WIDTH / enums.Dimension.ENTITY_WIDTH),\
            int(enums.Dimension.BOARD_HEIGHT / enums.Dimension.ENTITY_HEIGHT)]
        self.board = [[enums.EntityType.FREE] * BOARD_SIZE[0] for _ in range(BOARD_SIZE[1])]

        self.head = [0, 0]
        self.tail = []

        self.direction = enums.Direction.EAST

        self.enemy = None
    
        self.food = [random.randint(1, enums.Dimension.NUMBER_OF_ENTITIES_Y - 1),\
            random.randint(1, enums.Dimension.NUMBER_OF_ENTITIES_X - 1)]
        
        self.board[self.head[0]][self.head[1]] = enums.EntityType.HEAD
        self.board[self.food[0]][self.food[1]] = enums.EntityType.FOOD

    def set_enemy(self, enemy):
        self.enemy = enemy
    
    def set_wall(self, wall_pos):
        if self.board[wall_pos[0]][wall_pos[1]] == enums.EntityType.FREE:
            self.board[wall_pos[0]][wall_pos[1]] = enums.EntityType.WALL
        
    def change_direction(self, new_direction):
        if [self.direction[0] + new_direction[0], self.direction[1] + new_direction[1]] != [0, 0]:
            self.direction = new_direction
        
    def move(self):
        new_pos = [(self.head[0] + self.direction[0]) % enums.Dimension.NUMBER_OF_ENTITIES_Y,\
            (self.head[1] + self.direction[1]) % enums.Dimension.NUMBER_OF_ENTITIES_X]
        
        def eatsByMoving(new_pos):
            return self.board[new_pos[0]][new_pos[1]] == enums.EntityType.FOOD

        def diesByMoving(new_pos):
            return self.board[new_pos[0]][new_pos[1]] == enums.EntityType.WALL or\
                self.board[new_pos[0]][new_pos[1]] == enums.EntityType.TAIL

        if not diesByMoving(new_pos):
            if eatsByMoving(new_pos):
                self.tail.insert(0, self.head)
                self.enemy.set_wall(self.head)

                self.board[self.head[0]][self.head[1]] = enums.EntityType.TAIL
                self.head = new_pos

                food_possibilities = []
                for npos in range(len(self.board)):
                    for mpos in range(len(self.board[0])):
                        if self.board[npos][mpos] == enums.EntityType.FREE:
                            food_possibilities.append([npos, mpos])
                self.food = food_possibilities[random.randint(0, len(food_possibilities) - 1)]
                self.board[self.food[0]][self.food[1]] = enums.EntityType.FOOD
            
            else:
                self.tail.insert(0, self.head)

                self.board[self.head[0]][self.head[1]] = enums.EntityType.TAIL
                self.head = new_pos

                self.board[self.tail[-1][0]][self.tail[-1][1]] = enums.EntityType.FREE
                del self.tail[-1]

            self.board[new_pos[0]][new_pos[1]] = enums.EntityType.HEAD
