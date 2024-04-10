from typing import List, Optional
from ..domino import Domino
from ..move import Move
from ..board import Board
from .strategy import Strategy
import random


class RandomStrategy(Strategy):
    def select_move(self, hand: List[Domino], board: Board) -> Optional[Move]:
        # create a list of moves that can be played
        moves = board.possible_moves(hand)
        # if there are no moves, return None
        if not moves:
            return None
        # return a random move
        return random.choice(moves)

    def __str__(self) -> str:
        return "RandomStrategy"
