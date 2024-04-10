from typing import List, Optional
from .strategy import Strategy
from ..domino import Domino
from ..move import Move
from ..board import Board


class LargestPieceStrategy(Strategy):
    def select_move(self, hand: List[Domino], board: Board) -> Optional[Move]:
        # create a list of moves that can be played
        moves = board.possible_moves(hand)
        # if there are no moves, return None
        if not moves:
            return None
        # find the largest playable piece in moves
        largest_piece = max(moves, key=lambda move: move.domino.value())

        return largest_piece

    def __str__(self) -> str:
        return "LargestPieceStrategy"
