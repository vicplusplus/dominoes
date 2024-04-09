import unittest
from game.player import Player
from game.domino import Domino
from game.strategies.random_strategy import RandomStrategy
from game.move import Move
from game.board import Board


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.strategy = RandomStrategy()
        self.player = Player("Test Player", self.strategy)

    def test_valid_move(self):
        self.player.hand = [Domino(1, 2), Domino(3, 4)]
        board = Board(6, 4, 7)
        board.add(Domino(1, 5), "right")
        move = self.player.play(board)
        self.assertEqual(move, Move(Domino(2, 1), "left"))

    def test_invalid_move(self):
        self.player.hand = [Domino(1, 2), Domino(3, 4)]
        board = Board(6, 4, 7)
        board.add(Domino(5, 6), "left")
        move = self.player.play(board)
        self.assertIsNone(move)

    def test_score(self):
        self.player.hand = [Domino(1, 2), Domino(3, 4)]
        self.assertEqual(self.player.penalty(), 10)
