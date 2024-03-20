import unittest
from src.player import Player
from src.domino import Domino
from src.strategies.strategy import Strategy
from src.move import Move
from src.board import Board

class MockStrategy(Strategy):
    def select_move(self, hand, board):
        moves = board.possible_moves(hand)
        return moves[0] if moves else None

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.strategy = MockStrategy()
        self.player = Player('Test Player', self.strategy)

    def test_valid_move(self):
        self.player.hand = [Domino(1, 2), Domino(3, 4)]
        board = Board()
        board.add(Domino(1, 5), "right")
        move = self.player.play(board)
        self.assertEqual(move, Move(Domino(2, 1), "left"))
    
    def test_invalid_move(self):
        self.player.hand = [Domino(1, 2), Domino(3, 4)]
        board = Board()
        board.add(Domino(5, 6), "left")
        move = self.player.play(board)
        self.assertIsNone(move)

    def test_score(self):
        self.player.hand = [Domino(1, 2), Domino(3, 4)]
        self.assertEqual(self.player.score(), 10)

if __name__ == '__main__':
    unittest.main()