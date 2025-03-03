# CLEMENTE, BRIAN MATTHEW E.

import os
import random
import oxo_data

class Game:
    def __init__(self):
        self.board = [" "] * 9

    def new_game(self):
        """resets the board to start a new game"""
        self.board = [" "] * 9

    def save_game(self):
        """saves the current game state"""
        oxo_data.saveGame(self.board)
    
    def restore_game(self):
        """restores the previously saved game. If it is invalid, then it will start a new game"""
        try:
            game = oxo_data.restoreGame()
            if len(game) == 9:
                self.board = game
            else:
                self.new_game()
        except IOError:
            self.new_game()
    
    def _generate_move(self):
        """generates a random available cell on the board"""
        options = [i for i in range(len(self.board)) if self.board[i] == " "]
        return random.choice(options) if options else -1
    
    def _is_winning_move(self):
        """checks if the current board state has a winning combination"""
        wins = (
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        )

        for a, b, c in wins:
            chars = self.board[a] + self.board[b] + self.board[c]
            if chars == 'XXX' or chars == 'OOO':
                return True
        return False
    
    def user_move(self, cell):
        """processes the user's move"""
        if self.board[cell] != ' ':
            raise ValueError('Invalid cell')
        self.board[cell] = 'X'
        return 'X' if self._is_winning_move() else ""
    
    def computer_move(self):
        """processes the computer's move"""
        cell = self._generate_move()
        if cell == -1:
            return 'D'                      # DRAW
        self.board[cell] = 'O'
        return 'O' if self._is_winning_move() else ""
    
    def display_board(self):
        """returns the current board state as a formatted string"""
        return f"""
        {self.board[0]} | {self.board[1]} | {self.board[2]}
        ---------
        {self.board[3]} | {self.board[4]} | {self.board[5]}
        ---------
        {self.board[6]} | {self.board[7]} | {self.board[8]}
        """
    
    def test(self):
        """test game flow"""
        result = ""
        self.new_game()
        while not result:
            print(self.display_board())
            try:
                result = self.user_move(self._generate_move())
            except ValueError:
                print("Oops, that shouldn't happen!")
            if not result:
                result = self.computer_move()
            if not result:
                continue
            elif result == 'D':
                print("It's a draw!")
            else:
                print("Winner is:", result)
            print(self.display_board())

if __name__ == "__main__":
    game = Game()
    game.test()
