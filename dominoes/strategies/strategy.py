from abc import ABC, abstractmethod
from typing import List, Optional
from ..domino import Domino
from ..move import Move
from ..board import Board


class Strategy(ABC):
    @abstractmethod
    def select_move(self, hand: List[Domino], board: Board) -> Optional[Move]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
