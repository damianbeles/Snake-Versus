# Snake-Versus Game
# Description
Snake-Versus is a snake game based on two players, each one playing on his own field. The player who gets more points wins.
# Game Mechanics
- The snake can move in 4 directions: NORTH, WEST, SOUTH, EAST.
- The snake can move through sides.
- The snake dies when he collides with his tail or a wall.
- Eating a food brings you a point.
# Game Modes
- Player versus player.
- Players versus algorithm.
- Algorithm versus algorithm.
# Adding Algorithms
See this [commit](https://github.com/damianbeles/Snake-Versus/commit/cc3be19606d36e79b98e74bbf2a7d15207837e7d) in case you want to add your own algorithm.
Use:
- `_advance()` function for changing the direction (using `_change_direction()` function)
- `_post_advance()` function for actions after making a movement (example: for rewarding the snake in case of Machine Learning algorithms)
- `_save()` function for saving algorithms metadata (example: for weights in case of DQN algorithm)
# Reports
For each run / simulation, a report is saved in a `.csv` file format.
Example:
| GreedyChoosing | Lee | Winner |
| ---------------|:---:| ------:|
| 26             | 120 | second |
| 57             | 42  | first  |
| 25             | 142 | second |
# Main Window & Settings Windows
![Main and settings windows](https://i.imgur.com/ApbJmBQ.png)
# Game Window
![Game window](https://i.imgur.com/ajyR495.png)
