from src.domino import Domino


class BoardEnd:
    """
    Represents an end of the board.
    - The domino is the domino at the end.
    - The side is the side of the domino at the end.
    """

    def __init__(self, domino: Domino, side: int):
        self.domino = domino
        self.side = side
