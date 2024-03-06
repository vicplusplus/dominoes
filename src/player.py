from src.board import Board
from src.move import Move
from src.domino import Domino
from typing import Generator


def valid_moves(board: "Board", hand: list[Domino]) -> Generator["Move", None, None]:
    """
    Generates valid moves from a player's hand given the current board state.

    :param board: The current board state.
    :param hand: A list of Domino objects representing the player's hand.
    :return: A generator yielding Move objects that are valid.
    """
    if not board.dominoes:  # If the board is empty, any double can start.
        for domino in hand:
            if domino.sides[0]["value"] == domino.sides[1]["value"]:
                yield Move(domino, played_side=0)

    else:  # Board is not empty, generate moves based on board ends and hand.
        for domino in hand:
            for end in board.ends:
                for side in range(2):
                    for target_side in [0, 1]:
                        move = Move(domino, side, end.domino, target_side)
                        if move.validate(board):
                            yield move
