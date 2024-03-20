import unittest
from src.player import Player
from src.domino import Domino
from src.strategies.random_strategy import RandomStrategy
from src.move import Move
from src.board import Board

class TestMove(unittest.TestCase):
    def test_str(self):
        move = Move(Domino(1, 2), "left")
        self.assertEqual(str(move), "Add [1|2] to left side.")