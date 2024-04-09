import unittest
from game.domino import Domino
from game.board import Board
from game.move import Move


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 4, 7)

    def test_add_to_empty_board(self):
        domino = Domino(1, 2)
        self.board.add(domino, "right")
        self.assertEqual(self.board.dominoes, [domino])

    def test_add_to_right(self):
        domino1 = Domino(1, 2)
        domino2 = Domino(2, 3)
        self.board.add(domino1, "right")
        self.board.add(domino2, "right")
        self.assertEqual(self.board.dominoes, [domino1, domino2])

    def test_add_to_left(self):
        domino1 = Domino(1, 2)
        domino2 = Domino(3, 1)
        self.board.add(domino1, "right")
        self.board.add(domino2, "left")
        self.assertEqual(self.board.dominoes, [domino2, domino1])

    def test_add_invalid_side(self):
        domino = Domino(1, 2)
        with self.assertRaises(ValueError):
            self.board.add(domino, "invalid_side")

    def test_add_invalid_value(self):
        domino1 = Domino(1, 2)
        domino2 = Domino(3, 4)
        self.board.add(domino1, "right")
        with self.assertRaises(ValueError):
            self.board.add(domino2, "right")

    def test_cannot_add_invalid_side_to_non_empty_board(self):
        domino = Domino(1, 2)
        self.board.add(domino, "right")
        with self.assertRaises(ValueError):
            self.board.add(domino, "invalid_side")

    def test_possible_moves(self):
        domino1 = Domino(1, 2)
        domino2 = Domino(1, 3)
        domino3 = Domino(2, 3)
        self.board.add(domino1, "right")
        self.assertEqual(
            self.board.possible_moves([domino2, domino3]),
            [Move(domino2.flipped(), "left"), Move(domino3, "right")],
        )
