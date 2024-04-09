from typing import List, Optional
from dominoes import Domino, Board, Move
from dominoes.strategies import Strategy


class SmallestPieceStrategy(Strategy):
    def select_move(self, hand: List[Domino], board: Board) -> Optional[Move]:
        # create a list of moves that can be played
        moves = board.possible_moves(hand)
        # if there are no moves, return None
        if not moves:
            return None
        # find the largest playable piece in moves
        largest_piece = min(moves, key=lambda move: move.domino.value())

        return largest_piece

    def __str__(self) -> str:
        return "SmallestPieceStrategy"
