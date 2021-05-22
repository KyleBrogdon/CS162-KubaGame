# Kyle Brogdon
# 20 MAY 2021
# Program that creates a KubaGame board, CS 162's final project

class KubaGame:
    """Represents a Kuba game, played by two players"""
    def __init__(self, player_a_tuple, player_b_tuple):
        """Creates a 7x7 Kuba game board with two players playing either black marbles or white marbles by taking a tuple
        containing each player's name and color, sets current turn to None, sets game winner to None, and sets
        each player's red marble captured count to 0"""
        self._player_a = player_a_tuple[0]  # assign the first value in the tuple to player a's name
        self._player_a_color = player_a_tuple[1]  # assign the second value in the tuple to be player a's color
        self._player_b = player_b_tuple[0]  # assign the first value in the tuple to player b's name
        self._player_b_color = player_b_tuple[1]  # assign the second value in the tuple to be player b's color
        # initializes a 7x7 game board, top left corner is 0,0, bottom right is 6,6
        self._game_board = [['X'] * 7 for x in range(7)]  # 'X' represents no marble or an empty space
        self._game_board[0][0],  self._game_board[0][1],  \
        self._game_board[1][0],  self._game_board[1][1] = "W", "W", "W", "W"  # "W" represents white marbles
        self._game_board[5][5], self._game_board[5][6], \
        self._game_board[6][5], self._game_board[6][6] = "W", "W", "W", "W"
        self._game_board[5][0], self._game_board[5][1], \
        self._game_board[6][0], self._game_board[6][1] = "B", "B", "B", "B"  # "B" represents black marbles
        self._game_board[0][5], self._game_board[0][6], \
        self._game_board[1][5], self._game_board[1][6] = "B", "B", "B", "B"
        for y in range(1, 6):  # iterate through to put red marbles at correct positions
            self._game_board[y][3] = "R"  # "R" represents red marbles
            self._game_board[3][y] = "R"
        for j in range(2, 5):  # iterate through to put red marbles at correct positions
            self._game_board[j][2] = "R"
            self._game_board[j][4] = "R"
        self._current_turn = None  # initializes current turn to None as either player can start the game
        self._game_winner = None  # initializes game winner to None since game has not started
        self._player_a_captured = 0  # sets each player's captured red marble count to 0
        self._player_b_captured = 0  # sets each player's captured red marble count to 0
        self._current_roworcolumn = []

    def get_current_turn(self):
        """Returns the player whose turn it is to make a move"""
        return self._current_turn

    def make_move(self, playername, coordinates, direction):
        """Takes a player name, a tuple containing coordinates on the game board of the marble the
        player wishes to move, and the direction (L for left, R for right, F for forward, and B for backwards) the
        player wishes to move that marble. This method will check that moves are valid in accordance with the rules,
        then update the game board, check if the move resulted in a winner for the game, and then set
        the next turn to the other player"""
        if self._game_winner == None:
            if playername is True:  # if valid turn is possible code goes here
                pass
                if self._current_turn == playername:
                    if coordinates[0] < 7 and coordinates[0] >= 0:  # check if coordinates are on the game board
                        if coordinates[1] < 7 and coordinates[1] >= 0: # check if coordinates are on the game board
                            x_coord = coordinates[0]
                            y_coord = coordinates[1]
                            player_color = self.get_player_color(playername)
                            marble_being_moved = self.get_marble(coordinates)
                            if player_color == marble_being_moved:  # if player is moving his own color marble
                                if direction == "L":
                                    if x_coord == 6:  # if marble is on edge of board
                                        pass  # move code
                                    if self.get_marble((x_coord+1, y_coord)) == "X":  # if space behind marble is empty
                                        previous_board = []
                                        for x in range(0, 7):
                                            temp_move = self.get_marble((x, y_coord))
                                            previous_board.append(temp_move)
                                        for i in range(x_coord, 0, -1):
                                           if self.get_marble((i, y_coord)) == "X":
                                                proposed_move = previous_board
                                                counter = 0
                                                increment = 1
                                                while counter + i < x_coord:
                                                    proposed_move[i+counter] = proposed_move[i+increment]
                                                    counter +=1
                                                    increment += 1
                                                proposed_move[x_coord] = "X"
                                                if proposed_move == self._current_roworcolumn:  # violates Ko rule by checking if move would result in same board as last turn
                                                    return False
                                                for x in range(0,7):
                                                    self._game_board[x][y_coord] = proposed_move[x]  # update values in that row
                                                    self._current_roworcolumn = previous_board  # stores previous board to check for ko violation on future move
                                                if self._player_a == playername:  # set next turn to appropriate player
                                                    self._current_turn = self._player_b
                                                    return
                                                else:
                                                    self._current_turn = self._player_a
                                                    return
                                           if i == 0:  # if there are marbles lined up till edge of the board and one will get pushed off by this move
                                                marble_getting_knocked_off = previous_board[0]
                                                if self.get_player_color(playername) == marble_getting_knocked_off:
                                                    return False  # player cannot knock off their own marble
                                                proposed_move = previous_board
                                                counter = 0
                                                increment = 1
                                                for j in range(0, x_coord + 1):
                                                    proposed_move[j + counter] = proposed_move[j + increment]
                                                    counter += 1
                                                    increment += 1
                                                proposed_move[x_coord] = "X"
                                                for x in range(0, 7):
                                                    self._game_board[x][y_coord] = proposed_move[x]
                                                    self._current_roworcolumn = previous_board
                                                if self._player_a == playername:
                                                    if marble_getting_knocked_off == "R":
                                                        self._player_a_captured +=1
                                                        self._current_turn = self._player_b
                                                        return
                                                else:
                                                    if marble_getting_knocked_off == "R":
                                                        self._player_b_captured += 1
                                                    self._current_turn = self._player_a
                                                    return
                                    else:  # not a valid move because space behind marble is not empty
                                        return False
                                if direction == "R":
                                    if x_coord == 0:  # if marble is on edge of board
                                        pass  # move code
                                    if self.get_marble((x_coord - 1, y_coord)) == "X":  # if space behind marble is empty
                                        pass  # move code
                                    else:  # not a valid move because space behind marble is not empty
                                        return False
                                if direction == "B":
                                    if y_coord == 0:  # if marble is on edge of board
                                        pass  # move code
                                    if self.get_marble((x_coord, y_coord - 1)) == "X":  # if space behind marble is empty
                                        pass  # move code
                                    else:  # not a valid move because space behind marble is not empty
                                        return False
                                if direction == "F":
                                    if y_coord == 6:  # if marble is on edge of board
                                        pass  # move code
                                    if self.get_marble((x_coord, y_coord + 1)) == "X":  # if space behind marble is empty
                                        pass  # move code
                                    else:  # not a valid move because space behind marble is not empty
                                        return False
                                return False  # invalid direction was passed
                            return False  # player is not moving his own color marble
                        return False  # coordinates are off the game board
                    return False  # coordinates are off the game board
                return False  # not the correct player's turn
            if self._player_a == playername:
                self._game_winner = self._player_b
                return False # valid turn by player A is not possible, so player B is the winner
            else:
                self._game_winner = self._player_a
                return False  # valid turn is not possible by player B, so Player A is the winner
        return False  # someone has already won the game

    def make_move_left(self):
        """Helper method that moves marbles to the left"""

    def get_winner(self):
        """Returns the current status of the winner of the game"""
        return self._game_winner

    def get_captured(self, playername):
        """Takes a player name and returns the number of red marbles captured by the player"""
        if self._player_a == playername:  # checks to see which player we are returning the value for
            return self._player_a_captured
        else:
            return self._player_b_captured

    def get_marble(self, coordinates):
        """Takes a coordinate tuple and returns the value at the coordinate, which is
        either a red, black, white marble, or 'X' for no marble"""
        x = coordinates[0]
        y = coordinates[1]
        return self._game_board[x][y]  # returns the value at the correct coordinates on the board

    def get_marble_count(self):
        """Iterates over the entire game board, counts the number of each color of marble, and
        returns a tuple consisting of white, black, red marbles left on the game board"""
        W = 0  # number of white marbles
        B = 0  # number of black marbles
        R = 0  # number of red marbles
        for x in range(0,7):
            for y in range(0,7):  # iterates through entire 7x7 board
                if self._game_board[x][y] == "W":  # if marble is white, increment white
                    W += 1
                if self._game_board[x][y] == "B":  # if marble is black, increment black
                    B += 1
                if self._game_board[x][y] == "R":  # if marble is red, increment red
                    R += 1
        return(W, B, R)  # returns the tuple of white, black, red marbles

    def get_player_color(self, playername):
        """Takes a player name and returns what color they are playing with"""
        if self._player_a == playername:  # checks to see which player we are returning the value for
            return self._player_a_color
        else:
            return self._player_b_color

game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
# print(game.get_marble_count()) #returns (8,8,13)
# print(game.get_captured('PlayerA')) #returns 0
# game.get_current_turn() #returns 'PlayerB' because PlayerA has just played.
# game.get_winner() #returns None
# game.make_move('PlayerA', (6,5), 'F')
game.make_move('PlayerA', (6,6), 'L') #Cannot make this move
# game.get_marble((5,5)) #returns 'W'
