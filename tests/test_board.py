import unittest
from unittest.mock import Mock, patch
from src.board import Board
from src.move import Move
from src.domino import Domino


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_initialization(self):
        """Test the board is initialized with no dominoes and no ends."""
        self.assertEqual(
            len(self.board.dominoes), 0, "Board should be initialized with no dominoes."
        )
        self.assertEqual(
            len(self.board.ends), 0, "Board should have no ends initially."
        )

    def test_board_str_empty(self):
        """Test the string representation of an empty board."""
        self.assertEqual(
            str(self.board),
            "",
            "String representation of an empty board should be an empty string.",
        )


if __name__ == "__main__":
    unittest.main()
