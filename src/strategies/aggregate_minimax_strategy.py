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
        # create a list of moves that can be played
        moves = board.possible_moves(hand)
        # if there are no moves, return None
        if not moves:
            return None
        
        best_score = -inf
        best_move = None
        for move in moves:
            new_board = board.copy()
            new_board.add(move.domino, move.side)
            new_hand = hand.copy()
            if move.domino in new_hand:
                new_hand.remove(move.domino)
            else:
                new_hand.remove(move.domino.flipped())
            score = minimax(new_hand, new_board, self.depth, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

def minimax(hand, current_board, depth, isMaximizingPlayer):
    if depth == 0 or is_terminal(hand, current_board):
        return heuristic_value(hand, current_board)
    
    if isMaximizingPlayer:
        maxScore = -inf
        moves = current_board.possible_moves(hand)
        if not moves:
            score = minimax(hand, current_board, depth - 1, False)
            maxScore = max(maxScore, score)
        else:
            for move in moves:
                next_board = board_after_move(current_board, move)
                next_player_hand = hand_after_move(hand, move)

                score = minimax(next_player_hand, next_board, depth - 1, False)
                maxScore = max(maxScore, score)
        return maxScore
    else: # Minimizing player
        minScore = +inf
        for current_board in list_possible_opponent_boards(hand, current_board, current_board.num_players - 1):
            score = minimax(hand, current_board, depth - 1, True)
            minScore = min(minScore, score)
        return minScore

def opponents_hand(player_hand: List[Domino], board: Board) -> List[Domino]:
    # Generate all possible dominoes up to board's max value
    all_dominoes = set(Domino.generate_all(board.max_value))
    
    # Convert player's hand and board dominoes to sets for efficient lookup
    player_hand_set = {domino for domino in player_hand} | {domino.flipped() for domino in player_hand}
    board_dominoes_set = {domino for domino in board.dominoes} | {domino.flipped() for domino in board.dominoes}
    
    # Use set difference to find dominoes not in player's hand or on the board
    remaining_dominoes = all_dominoes - player_hand_set - board_dominoes_set
    
    return list(remaining_dominoes)

def list_possible_opponent_boards(hand, board, depth) -> List[Board]:
    # All other players are treated as a single opponent that can make K-1 moves where K
    # is the number of players in the game
    # This function returns the list of all possible boards that can result from opponents' moves
    if depth == 0:
        return [board]
    opponent_hand = opponents_hand(hand, board)
    possible_boards = []
    possible_moves = board.possible_moves(opponent_hand)
    if not possible_moves:
        possible_boards.append(board)
    else:
        for move in possible_moves:
            next_board = board_after_move(board, move)
            possible_boards.extend(list_possible_opponent_boards(opponent_hand, next_board, depth - 1))
    return possible_boards

def heuristic_value(hand, board):
    # the value of a hand is contingent on two factors:
    # 1. the number of possible moves the player can make relative to the size of the hand
    # 2. the sum of the values of the dominoes in the hand
    # A player with a large hand and few possible moves is at a disadvantage
    # A player with a small hand and many possible moves is at an advantage
    if not hand:
        return inf
    return len(board.possible_moves(hand)) / len(hand) + sum(domino.value() for domino in hand)

def is_terminal(hand, board):
    # a terminal node is a node where the player's hand is empty
    # or neither player can make a move
    return not hand or not board.possible_moves(hand) and not board.possible_moves(opponents_hand(hand, board))

def board_after_move(board, move):
    new_board = board.copy()
    new_board.add(move.domino, move.side)
    return new_board

def hand_after_move(hand, move):
    new_hand = hand.copy()
    Move.remove_from_hand(move, new_hand)
    return new_hand