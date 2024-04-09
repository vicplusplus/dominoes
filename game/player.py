from dataclasses import dataclass
from typing import List, Optional
from game.domino import Domino
from game.strategies.strategy import Strategy
from game.move import Move
from game.board import Board


class Player:
    def __init__(self, name: str, strategy: Strategy) -> None:
        self.name = name
        self.hand: List[Domino] = []
        self.strategy: Strategy = strategy

    def play(self, board: Board) -> Optional[Move]:
        selected = self.strategy.select_move(self.hand, board)
        if selected:
            Move.remove_from_hand(selected, self.hand)
            return selected
        return None

    def penalty(self) -> int:
        return sum(domino.value() for domino in self.hand)

    def min_domino(self) -> Domino:
        return min(self.hand, key=lambda domino: domino.value())
