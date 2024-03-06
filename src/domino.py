class Domino:
    """
    A class to represent a domino piece.
    """

    def __init__(self, value1: int, value2: int) -> None:
        """
        Initializes a domino with two values.
        """
        self.sides = (
            {"value": value1, "domino": None},
            {"value": value2, "domino": None},
        )

    def f_repr(self, reverse=False) -> str:
        """
        Returns a string representation of the domino with optional reverse order.
        """
        if reverse:
            return f"[{self.sides[1]['value']}|{self.sides[0]['value']}]"
        return f"[{self.sides[0]['value']}|{self.sides[1]['value']}]"

    def value(self) -> int:
        """
        Returns the sum of the values of the domino.
        """
        return self.sides[0]["value"] + self.sides[1]["value"]

    def connect(self, other: "Domino", self_side: int, other_side: int) -> None:
        """
        Connects two dominoes, setting their sides' references to each other.
        """
        self.sides[self_side]["domino"] = other
        other.sides[other_side]["domino"] = self
