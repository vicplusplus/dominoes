from dataclasses import dataclass
from src.domino import Domino

@dataclass
class Move:
    domino: Domino
    side: str