from src.domino import Domino
from typing import Generator


class Move:
    """
    Represents a move made by a player.
    - The played domino is the domino played by the current player.
    - The target domino is the domino the played domino is connected to.
    - If the target domino is None, the played domino is just added to the board.
    """

    def __init__(
        self,
        played: Domino,
        played_side: int,
        target: Domino = None,
        target_side: int = None,
    ):
        self.played = played
        self.target = target
        self.played_side = played_side
        self.target_side = target_side

    def validate(self, board) -> bool:
        """
        Validates the move. Returns True if the move is legal, False otherwise.
        Starting moves must be doubles.
        """
        # cannot play a domino without a target if the board is not empty
        if not self.target and board.dominoes:
            return False

        # cannot play a domino without a target if it is not a double
        if (
            self.played.sides[0]["value"] != self.played.sides[1]["value"]
            and not self.target
        ):
            return False

        # cannot target a domino that is not in the board's ends
        if (
            self.target
            and {"domino": self.target, "side": self.target_side} not in board.ends
        ):
            return False

        # cannot play a domino that does not match the target
        if (
            self.target
            and self.played.sides[self.played_side]["value"]
            != self.target.sides[self.target_side]["value"]
        ):
            return False

        return True
