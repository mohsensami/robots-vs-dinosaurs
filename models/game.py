from services.utils import create_new_board, select_empty_position

import pprint
import random


class Board:

    """ Initialize the size of the game board and the number of roles in each camp. """

    def __init__(self, dim: int):
        self.dim = dim
        self._board = []
        self._robots_count = 0
        self._dinosaurs_count = 0
        self._create_new_board()

    def _create_new_board(self):
        self._board = create_new_board(self.dim)
        self.dinosaurs_position = []
        self.robots_position = []
        self.robots = {}

    def set_dinosaurs(self, row: int = None, column: int = None):
        """
        Set the position of dinosaurs
        :param row: the row coordinate of the position
        :param column: the column coordinate of the position
        :return: the list of dinosaurs' positions
        """
        # Check the total number of occupied in the grid
        if self._dinosaurs_count + self._robots_count >= self.dim * self.dim:
            raise Exception(
                "All positions in the grid have been occupied or you set too many robots/dinosaurs in the grid"
            )

        position = (row, column)
        # Randomly select in available positions if the position not specified or specified wrong
        if row is None or column is None:
            available = select_empty_position(self._board)
            position = random.choice(available)

        if not self.is_in_grid(position):
            
            raise Exception("The dinosaurs placement is out of grid scope")

        # Record the position of a new role
        
        self.dinosaurs_position.append(position)

    def set_robots(self, row: int = None, column: int = None, direction: str = "E"):
        """
        Set the position of robots
        :param row: the row coordinate of the position
        :param column: the column coordinate of the position
        :param direction: the facing direction of the robot, the default is east (->)
        :return: the list of robots' positions, the dictionary of robots' detailed position
        """
        # Check the total number of occupied in the grid
        if self._dinosaurs_count + self._robots_count >= self.dim * self.dim:

            raise Exception(
                "All positions in the grid have been occupied or you set too many robots/dinosaurs in the grid"
            )

        # Create robots
        # Define a random id for robot
        robot_id = str(random.getrandbits(16))

        position = (row, column)
        # Randomly select in available positions if the position not specified or specified wrong
        if row is None or column is None:
            available = select_empty_position(self._board)
            position = random.choice(available)

        if not self.is_in_grid(position):
            
            raise Exception("The dinosaurs placement is out of grid scope")

        # Record the position of a new role
        
        self.robots_position.append(position)
        self.robots.update(**{robot_id: {"coordinate": position, "direction": direction}})

    def validate_move(self, position: (int, int)):
        # Check the next move is an empty space
        if self._board[position] != 0:
            return False
        return True

    def is_in_grid(self, position: (int, int)):
        # Check the next move is within boundaries
        if 0 <= position[0] < self.dim and 0 <= position[1] < self.dim:
            return True
        return False

    def get_board(self):
        return self._board

    def delete_board(self):
        self._board = []

    def print_board(self):
        pprint.pprint(self._board)


class Game(Board):

    """ Inherit the Board instance and begin a game"""

    def __init__(self, dim):
        super().__init__(dim)
        self.game_id = random.randint(1, 9999)

        # The total number of move in a game
        self._moves = 0

        # Indicate each dinosaur has 1 life point
        self._dinosaur_life = 1

        # Indicate each robot has 1 attack power
        self._robot_power = -1

    def initial_placement(self):
        # Place all roles to the board
        for dinosaur in self.dinosaurs_position:
            self._board[dinosaur] = self._dinosaur_life

        for robot in self.robots_position:
            self._board[robot] = self._robot_power

        self.print_board()

    def set_random_game(self, robots_count: int = 1, dinosaurs_count: int = 1):
        """
        Set a random-placement game, define the number of roles in each camp
        :param robots_count: the total number of robots, the default is 1
        :param dinosaurs_count: the total number of dinosaurs, the default is 1
        """
        # The default is an 1 vs 1 game
        if not robots_count:
            robots_count = 1
        if not dinosaurs_count:
            dinosaurs_count = 1

        while dinosaurs_count != self._dinosaurs_count:
            self.set_dinosaurs()
            self._dinosaurs_count += 1

        while robots_count != self._robots_count:
            self.set_robots()
            self._robots_count += 1

        self.initial_placement()
