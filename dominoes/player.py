from dataclasses import dataclass
from typing import List, Optional
from .domino import Domino
from .board import Board
from .move import Move
from .strategies.strategy import Strategy


class Player:
    def __init__(self, name: str, strategy: Optional[Strategy] = None) -> None:
        self.name = name
        self.hand: List[Domino] = []
        self.strategy: Strategy = strategy

    def select_move(self, board: Board) -> Optional[Move]:
        if not self.strategy:
            raise ValueError("Player must have a strategy to play")
        return self.strategy.select_move(self.hand, board)

    def penalty(self) -> int:
        return sum(domino.value() for domino in self.hand)

    def min_domino(self) -> Domino:
        return min(self.hand, key=lambda domino: domino.value())
