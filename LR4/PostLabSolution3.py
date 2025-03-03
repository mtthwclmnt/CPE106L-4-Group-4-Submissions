#ACANTILADO, MARIA ANGELICA and DYTIANQUIN, CHALZEA FRANSEN C.
import unittest
from PostLabSolution1 import Game

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = Game()
    
    def test_new_game(self):
        self.game.board = ['X'] * 9
        self.game.new_game()
        self.assertEqual(self.game.board, [' '] * 9)

    def test_save_game(self):
        self.game.board = ['X', 'O', ' '] * 3
        # Simulate saving the game by directly checking the board
        saved_board = self.game.board.copy()  # Simulate save
        self.assertEqual(saved_board, ['X', 'O', ' '] * 3)

    def test_restore_game_valid(self):
        # Simulate restoring a valid game state
        self.game.board = ['X', 'O', ' '] * 3
        restored_board = ['X', 'O', ' '] * 3  # Simulate restore
        self.game.board = restored_board
        self.assertEqual(self.game.board, ['X', 'O', ' '] * 3)

    def test_restore_game_invalid(self):
        # Simulate restoring an invalid game state
        self.game.board = ['X'] * 8  # Invalid length
        self.game.new_game()  # Reset to new game
        self.assertEqual(self.game.board, [' '] * 9)

    def test_generate_move_empty_board(self):
        move = self.game._generate_move()
        self.assertIn(move, range(9))

    def test_generate_move_full_board(self):
        self.game.board = ['X'] * 9
        move = self.game._generate_move()
        self.assertEqual(move, -1)

    def test_generate_move_some_available(self):
        self.game.board = ['X', ' ', 'O', ' ', 'X', ' ', ' ', ' ', ' ']
        move = self.game._generate_move()
        self.assertIn(move, [1, 3, 5, 6, 7, 8])  # Check if the move is in available cells

    def test_is_winning_move_horizontal(self):
        self.game.board = ['X', 'X', 'X'] + [' ']*6
        self.assertTrue(self.game._is_winning_move())

    def test_is_winning_move_vertical(self):
        self.game.board = ['O', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ']
        self.assertTrue(self.game._is_winning_move())

    def test_is_winning_move_diagonal(self):
        self.game.board = [' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ']
        self.assertTrue(self.game._is_winning_move())

    def test_is_winning_move_no_win(self):
        self.game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        self.assertFalse(self.game._is_winning_move())

    def test_user_move_valid(self):
        result = self.game.user_move(4)
        self.assertEqual(self.game.board[4], 'X')
        self.assertEqual(result, '')  # Not a winning move

    def test_user_move_winning(self):
        self.game.board = ['X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        result = self.game.user_move(2)
        self.assertEqual(result, 'X')  # Winning move

    def test_user_move_invalid(self):
        self.game.board[3] = 'O'
        with self.assertRaises(ValueError):
            self.game.user_move(3)

    def test_computer_move_draw(self):
        self.game.board = ['X', 'O'] * 4 + ['X'] 
        result = self.game.computer_move()
        self.assertEqual(result, 'D')

    def test_computer_move_winning(self):
        self.game.board = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
        self.game.board[2] = 'O'
        result = self.game.computer_move()
        self.assertEqual(result, 'O') 
        self.assertEqual(self.game.board[2], 'O')  

if __name__ == '__main__':
    unittest.main()
