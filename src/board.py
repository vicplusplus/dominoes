from src.domino import Domino
from typing import Generator
from random import shuffle
from src.move import Move
from src.board_end import BoardEnd


class Board:
    """
    Represents the board of the game.
    - The dominoes is a list of the dominoes in the board.
    - The ends is a list of the ends of the board.
    """

    def __init__(self):
        self.dominoes = []
        self.ends = []

    def add(self, move: Move) -> None:
        """
        Adds a domino to the board.
        """
        if not move.validate(self):
            raise ValueError("Invalid move")

        if not move.target:
            self.dominoes.append(move.played)
            self.ends = [BoardEnd(move.played, 0), BoardEnd(move.played, 1)]
        else:
            self.ends.remove(BoardEnd(move.target, move.target_side))
            # set the new end to the opposite side of the played domino
            self.ends.append(BoardEnd(move.played, 1 - move.played_side))

    def __str__(self) -> str:
        """
        Returns a string representation of the board.
        """
        if not self.dominoes:
            return ""
        current_side = 1 - self.ends[0].side
        start = self.ends[0].domino
        while start is not None:
            print(start.f_repr(current_side), end=" ")
            current_side = start.sides[current_side]["domino"].sides.index(start)
            start = start.sides[current_side]["domino"]
