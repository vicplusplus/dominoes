import unittest
from src.domino import Domino
from src.move import Move

class TestMove(unittest.TestCase):
    def test_str(self):
        move = Move(Domino(1, 2), "left")
        self.assertEqual(str(move), "Add [1|2] to left side.")