from dataclasses import dataclass
from src.domino import Domino

@dataclass
class Move:
    domino: Domino
    side: str

    def __str__(self) -> str:
        return f"Add {self.domino} to {self.side} side."