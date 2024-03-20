import unittest
from src.domino import Domino

class TestDomino(unittest.TestCase):
    def test_value(self):
        domino = Domino(1, 2)
        self.assertEqual(domino.value(), 3)
    
    def test_flipped(self):
        domino = Domino(1, 2)
        self.assertEqual(domino.flipped(), Domino(2, 1))