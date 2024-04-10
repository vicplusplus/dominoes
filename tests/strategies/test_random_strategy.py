import unittest
from dominoes import Domino, Board
from dominoes.strategies import RandomStrategy


class TestRandomStrategy(unittest.TestCase):
    def test_select_piece(self):
        strategy = RandomStrategy()
        hand = [Domino(1, 2), Domino(3, 4)]
        board = Board(6, 4, 7)
        board.add(Domino(1, 5), "right")
        move = strategy.select_move(hand, board)
        # either the domino or its flipped version should be in the hand
        self.assertTrue(move.domino in hand or move.domino.flipped() in hand)
        # the move should be valid
        self.assertTrue(move in board.possible_moves(hand))
