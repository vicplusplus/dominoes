from dataclasses import dataclass
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