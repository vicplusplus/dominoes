import unittest
from src.domino import Domino
from src.board import Board
from src.move import Move
from src.strategies.largest_piece_strategy import LargestPieceStrategy

class TestLargestPieceStrategy(unittest.TestCase):
    def test_select_largest_piece(self):
        strategy = LargestPieceStrategy()
        hand = [Domino(1, 2), Domino(6, 6), Domino(4, 5)]
        board = Board(6, 4, 7)
        # Assuming `Board.add()` method and `Board.possible_moves()` 
        # are implemented in a way to allow adding to the board directly and
        # to determine possible moves based on the current board state
        board.add(Domino(1, 5), "right")
        
        move = strategy.select_move(hand, board)
        
        # Check if the selected move contains the largest domino in the hand
        # This assumes your Move object stores the domino and possibly a side ("left" or "right")
        # Adjust the assertion based on your implementation details
        self.assertEqual(move.domino, Domino(5, 4), "The strategy did not select the largest piece available.")

    def test_no_possible_moves(self):
        strategy = LargestPieceStrategy()
        hand = [Domino(2, 3), Domino(4, 5)]
        board = Board(6, 4, 7)
        # Set the board in a state where no moves can be played from the hand
        board.add(Domino(0, 1), "right")  # Assuming this sets the board to a state incompatible with the hand
        
        move = strategy.select_move(hand, board)
        
        # Expecting None since no moves can be played
        self.assertIsNone(move, "The strategy should return None when no moves can be played.")