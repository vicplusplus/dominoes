from dataclasses import dataclass
from src.domino import Domino

@dataclass
class Move:
    domino: Domino
    side: str

    def __str__(self) -> str:
        return f"Add {self.domino} to {self.side} side."
    
    # static method to remove a played domino from a hand
    @staticmethod
    def remove_from_hand(move: "Move", hand: list) -> None:
        if move.domino in hand:
            hand.remove(move.domino)
        else:
            hand.remove(move.domino.flipped())