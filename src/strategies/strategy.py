from abc import ABC, abstractmethod
from typing import List, Optional
from src.domino import Domino
from src.move import Move
from src.board import Board

class Strategy(ABC):
    @abstractmethod
    def select_move(self, hand: List[Domino], board: Board) -> Optional[Move]:
        pass
