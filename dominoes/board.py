from .domino import Domino
from .move import Move
from typing import List


class Board:
    def __init__(self, max_value: int, num_players: int, pieces_per_hand: int) -> None:
        self.dominoes: List[Domino] = []
        self.max_value = max_value
        self.num_players = num_players
        self.pieces_per_hand = pieces_per_hand

    def add(self, domino: Domino, side: str) -> None:
        if side != "right" and side != "left":
            raise ValueError("Invalid side")
        if not self.dominoes:
            self.dominoes.append(domino)
            return
        if side == "right":
            if domino.left == self.dominoes[-1].right:
                self.dominoes.append(domino)
            elif domino.right == self.dominoes[-1].right:
                self.dominoes.append(domino.flipped())
            else:
                raise ValueError("Invalid move")
        elif side == "left":
            if domino.right == self.dominoes[0].left:
                self.dominoes.insert(0, domino)
            elif domino.left == self.dominoes[0].left:
                self.dominoes.insert(0, domino.flipped())
            else:
                raise ValueError("Invalid move")
        else:
            raise ValueError("Invalid side")

    def can_play(self, move: Move) -> bool:
        if not move:
            return True
        if not self.dominoes:
            return True
        if move.side == "right":
            return (
                move.domino.left == self.dominoes[-1].right
                or move.domino.right == self.dominoes[-1].right
            )
        elif move.side == "left":
            return (
                move.domino.right == self.dominoes[0].left
                or move.domino.left == self.dominoes[0].left
            )
        else:
            raise ValueError("Invalid side")

    def possible_moves(self, hand: List[Domino]) -> List[Move]:
        if not self.dominoes:
            return [Move(domino, "right") for domino in hand]

        moves = []
        added = False

        for domino in hand:
            if domino.left == self.dominoes[-1].right:
                moves.append(Move(domino, "right"))
                added = True
            if domino.right == self.dominoes[0].left:
                moves.append(Move(domino, "left"))
                added = True
            if not added and domino.left != domino.right:
                if domino.right == self.dominoes[-1].right:
                    moves.append(Move(domino.flipped(), "right"))
                if domino.left == self.dominoes[0].left:
                    moves.append(Move(domino.flipped(), "left"))

        return moves

    def copy(self):
        new_board = Board(self.max_value, self.num_players, self.pieces_per_hand)
        new_board.dominoes = self.dominoes.copy()
        return new_board
