import unittest
from unittest.mock import Mock
from src.domino import Domino
from src.move import Move


class TestMove(unittest.TestCase):
    def setUp(self):
        self.domino1 = Domino(6, 6)  # A double
        self.domino2 = Domino(6, 5)  # Not a double
        self.domino3 = Domino(5, 5)  # Another double

    def test_valid_starting_move(self):
        """Test a valid starting move with a double."""
        board = Mock()
        board.dominoes = []  # Board is empty at the start
        move = Move(self.domino1, played_side=0, target=None)
        self.assertTrue(move.validate(board), "Valid starting move was rejected.")

    def test_invalid_starting_move(self):
        """Test an invalid starting move with a non-double."""
        board = Mock()
        board.dominoes = []  # Board is empty at the start
        move = Move(self.domino2, played_side=0, target=None)
        self.assertFalse(move.validate(board), "Invalid starting move was accepted.")

    def test_valid_move_with_target(self):
        """Test a valid move connecting to a target on the board."""
        board = Mock()
        board.dominoes = [self.domino1]
        board.ends = [{"domino": self.domino1, "side": 1}]
        move = Move(self.domino2, played_side=0, target=self.domino1, target_side=1)
        self.assertTrue(move.validate(board), "Valid move with target was rejected.")

    def test_invalid_move_no_target_non_empty_board(self):
        """Test an invalid move with no target on a non-empty board."""
        board = Mock()
        board.dominoes = [self.domino1]  # Non-empty board
        move = Move(self.domino2, played_side=0, target=None)
        self.assertFalse(
            move.validate(board), "Move without target on non-empty board was accepted."
        )

    def test_invalid_move_wrong_connection(self):
        """Test an invalid move with incorrect connection."""
        board = Mock()
        board.dominoes = [self.domino1]
        board.ends = [{"domino": self.domino1, "side": 1}]
        move = Move(self.domino3, played_side=0, target=self.domino1, target_side=1)
        self.assertFalse(
            move.validate(board), "Move with incorrect connection was accepted."
        )


if __name__ == "__main__":
    unittest.main()
