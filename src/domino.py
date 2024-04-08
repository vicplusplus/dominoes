from dataclasses import dataclass
from typing import List
@dataclass
class Domino:
    left: int
    right: int

    def flipped(self) -> "Domino":
        return Domino(self.right, self.left)

    def value(self) -> int:
        return self.left + self.right
    
    def __str__(self) -> str:
        return f"[{self.left}|{self.right}]"
    
    @staticmethod
    def generate_all(max_value: int) -> List["Domino"]:
        dominoes = []
        for i in range(max_value + 1):
            for j in range(i, max_value + 1):
                dominoes.append(Domino(i, j))
        return dominoes