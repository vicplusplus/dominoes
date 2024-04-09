import unittest
from dominoes import Domino, Board, Move
from dominoes.strategies import AggregateMinimaxStrategy


class TestAggregateMinimaxStrategy(unittest.TestCase):
    def test_optimal_move_selection(self):
        # Set up a scenario where the optimal move is known
        strategy = AggregateMinimaxStrategy(depth=2)
        hand = [Domino(1, 2), Domino(3, 4)]
        board = Board(6, 4, 7)
        board.add(Domino(1, 5), "right")

        # Execute the strategy
        move = strategy.select_move(hand, board)

        # Assert that the selected move is the expected optimal move
        # This is hypothetical and depends on your game's rules and the heuristic
        expected_move = Move(Domino(2, 1), "left")
        self.assertEqual(move.domino, expected_move.domino)
        self.assertEqual(move.side, expected_move.side)
