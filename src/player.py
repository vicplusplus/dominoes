from dataclasses import dataclass
from typing import List, Optional
from src.domino import Domino
from src.strategies.strategy import Strategy
from src.move import Move
from src.board import Board

class Player:
    def __init__(self, name: str, strategy: Strategy) -> None:
        self.name = name
        self.hand: List[Domino] = []
        self.strategy: Strategy = strategy

    def play(self, board: Board) -> Optional[Move]:
        selected = self.strategy.select_move(self.hand, board)
        if selected:
            if selected.domino in self.hand:
                self.hand.remove(selected.domino)
            else:
                self.hand.remove(selected.domino.flipped())
            return selected
        return None

    def score(self) -> int:
        return sum(domino.value() for domino in self.hand)