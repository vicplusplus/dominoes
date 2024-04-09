from typing import List, Optional
from src.domino import Domino
from src.strategies.strategy import Strategy
from src.move import Move
from src.board import Board
from math import inf


class AggregateMinimaxStrategy(Strategy):
    def __init__(self, depth: int) -> None:
        self.depth = depth

    def select_move(self, hand: List[Domino], board: Board) -> Optional[Move]:
        moves = board.possible_moves(hand)
        if not moves:
            return None

        best_move = max(
            moves, key=lambda move: self.score_move(move, hand, board), default=None
        )
        return best_move

    def score_move(self, move: Move, hand: List[Domino], board: Board) -> float:
        new_board = board_after_move(board, move)
        new_hand = hand_after_move(hand, move)
        return minimax(new_hand, new_board, self.depth, False)

    def __str__(self) -> str:
        return f"AggregateMinimaxStrategy(depth={self.depth})"


def minimax(
    hand: List[Domino],
    board: Board,
    depth: int,
    isMaximizingPlayer: bool,
    alpha=float("-inf"),
    beta=float("inf"),
):
    # Base condition: If we've reached the desired depth or the game is in a terminal state
    if depth == 0 or is_terminal(hand, board):
        return heuristic_value(hand, board)

    if isMaximizingPlayer:
        maxEval = float("-inf")
        moves = board.possible_moves(hand) or [
            None
        ]  # Ensures there is always a move to consider
        for move in moves:
            evaluation = minimax(
                hand_after_move(hand, move),
                board_after_move(board, move),
                depth - 1,
                False,
                alpha,
                beta,
            )
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:  # Beta cut-off
                break
        return maxEval
    else:
        minEval = float("inf")
        moves = board.possible_moves(hand) or [None]
        for move in moves:
            evaluation = minimax(
                hand_after_move(hand, move),
                board_after_move(board, move),
                depth - 1,
                True,
                alpha,
                beta,
            )
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:  # Alpha cut-off
                break
        return minEval


def board_after_move(board: Board, move: Move):
    new_board = board.copy()
    if move:  # Might be None if no moves are possible
        new_board.add(move.domino, move.side)
    return new_board


def hand_after_move(hand: List[Domino], move: Move):
    new_hand = hand.copy()
    if move:  # Might be None if no moves are possible
        domino_to_remove = move.domino if move.domino in hand else move.domino.flipped()
        new_hand.remove(domino_to_remove)
    return new_hand


def heuristic_value(hand: List[Domino], board: Board):
    # the value of a hand is contingent on two factors:
    # 1. the number of possible moves the player can make relative to the size of the hand
    # 2. the sum of the values of the dominoes in the hand
    # A player with a large hand and few possible moves is at a disadvantage
    # A player with a small hand and many possible moves is at an advantage
    if not hand:
        return inf
    return len(board.possible_moves(hand)) / len(hand) + sum(
        domino.value() for domino in hand
    )


def is_terminal(hand: List[Domino], board: Board):
    # a terminal node is a node where the player's hand is empty
    # or neither player can make a move
    return (
        not hand
        or not board.possible_moves(hand)
        and not board.possible_moves(opponents_hand(hand, board))
    )


def opponents_hand(player_hand: List[Domino], board: Board) -> List[Domino]:
    # Generate all possible dominoes up to board's max value
    all_dominoes = set(Domino.generate_all(board.max_value))

    # Convert player's hand and board dominoes to sets for efficient lookup
    player_hand_set = {domino for domino in player_hand} | {
        domino.flipped() for domino in player_hand
    }
    board_dominoes_set = {domino for domino in board.dominoes} | {
        domino.flipped() for domino in board.dominoes
    }

    # Use set difference to find dominoes not in player's hand or on the board
    remaining_dominoes = all_dominoes - player_hand_set - board_dominoes_set

    return list(remaining_dominoes)
