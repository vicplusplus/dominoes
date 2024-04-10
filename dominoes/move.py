from dataclasses import dataclass
from .domino import Domino


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
        elif move.domino.flipped() in hand:
            hand.remove(move.domino.flipped())
        else:
            raise ValueError("Domino not in hand.")
