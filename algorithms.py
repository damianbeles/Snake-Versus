import enums

from snake import Snake

class GreedyChoosing(Snake):
    def __init__(self):
        Snake.__init__(self)
    
    def advance(self):
        directions = [enums.Direction.EAST, enums.Direction.SOUTH,\
            enums.Direction.WEST, enums.Direction.NORTH]
        min_direction = enums.Dimension.NUMBER_OF_ENTITIES_Y + enums.Dimension.NUMBER_OF_ENTITIES_X
        mini_direction = None

        def canMoveTowards(new_pos):
            return self.board[new_pos[0]][new_pos[1]] == enums.EntityType.FREE or\
                self.board[new_pos[0]][new_pos[1]] == enums.EntityType.FOOD

        def heuristic(new_pos):
            if canMoveTowards(new_pos):
                if self.board[new_pos[0]][new_pos[1]] == enums.EntityType.FOOD:
                    return 0
            return abs(new_pos[0] - self.food[0]) + abs(new_pos[1] - self.food[1])

        for npos in range(len(directions)):
            new_pos = [(self.head[0] + directions[npos][0]) % enums.Dimension.NUMBER_OF_ENTITIES_Y,\
                (self.head[1] + directions[npos][1]) % enums.Dimension.NUMBER_OF_ENTITIES_X]

            if canMoveTowards(new_pos) and\
                heuristic(new_pos) < min_direction:
                min_direction = heuristic(new_pos)
                mini_direction = npos
            
        if mini_direction != None:
            self.direction = directions[mini_direction]
