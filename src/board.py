from src.domino import Domino
from typing import List
from src.move import Move


class Board:
    def __init__(self, max_value: int, num_players: int, pieces_per_hand: int) -> None:
        self.dominoes: List[Domino] = []
        self.max_value = max_value
        self.num_players = num_players
        self.pieces_per_hand = pieces_per_hand

    def add(self, domino: Domino, side: str) -> None:
        if not self.can_add(domino, side):
            raise ValueError("Invalid move")
        if side == "right":
            self.dominoes.append(domino)
        elif side == "left":
            self.dominoes.insert(0, domino)
        else:
            raise ValueError("Invalid side")

    def can_add(self, domino: Domino, side: str) -> bool:
        if not self.dominoes:
            return True
        if side == "right":
            return domino.left == self.dominoes[-1].right
        if side == "left":
            return domino.right == self.dominoes[0].left
        return False

    def possible_moves(self, hand: List[Domino]) -> List[Move]:
        if not self.dominoes:
            return [Move(domino, "right") for domino in hand]

        moves = []

        for domino in hand:
            if domino.left == self.dominoes[-1].right:
                moves.append(Move(domino, "right"))
            if domino.right == self.dominoes[0].left:
                moves.append(Move(domino, "left"))
            if domino.left != domino.right:
                if domino.right == self.dominoes[-1].right:
                    moves.append(Move(domino.flipped(), "right"))
                if domino.left == self.dominoes[0].left:
                    moves.append(Move(domino.flipped(), "left"))

        return moves

    def copy(self):
        new_board = Board(self.max_value, self.num_players, self.pieces_per_hand)
        new_board.dominoes = self.dominoes.copy()
        return new_board
