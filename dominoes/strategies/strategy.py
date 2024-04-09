from abc import ABC, abstractmethod
from typing import List, Optional
from dominoes import Domino, Board, Move


class Strategy(ABC):
    @abstractmethod
    def select_move(self, hand: List[Domino], board: Board) -> Optional[Move]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
