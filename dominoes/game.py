from typing import List, Optional, Tuple
from random import shuffle

from .player import Player
from .board import Board
from .move import Move
from .domino import Domino


class Game:
    def __init__(
        self, players: list[Player], max_value: int, pieces_per_hand: int
    ) -> None:
        self.board: Board = Board(max_value, len(players), pieces_per_hand)
        self.players: List[Player] = players
        self.move_history: List[Tuple[int, Optional[Move]]] = []
        self.current_player_index: int = 0
        self.passes: int = 0
        self.winner: Optional[Player] = None
        self.distribute_pieces()

    def distribute_pieces(self) -> None:
        # generate all possible dominoes
        dominoes = Domino.generate_all(self.board.max_value)
        # cannot distribute pieces is players * pieces_per_hand > len(dominoes)
        if len(dominoes) < len(self.players) * self.board.pieces_per_hand:
            raise ValueError("Not enough dominoes to distribute to players")
        # shuffle the dominoes
        shuffle(dominoes)
        # give each player a hand of dominoes
        for player in self.players:
            player.hand = dominoes[: self.board.pieces_per_hand]
            dominoes = dominoes[len(dominoes) - self.board.pieces_per_hand :]

    def play_turn(self, move: Move) -> None:
        # if the player can't play, pass
        if not move:
            self.passes += 1
            self.move_history.append((self.current_player_index, None))
        else:
            self.passes = 0
            # add the domino to the board
            self.board.add(move.domino, move.side)
            self.move_history.append((self.current_player_index, move))
        # check if the player has won
        if not self.players[self.current_player_index].hand:
            self.winner = self.players[self.current_player_index]
        # if all players have passed, use the tie breaker
        if self.passes == len(self.players):
            self.winner = self.tie_breaker()
        # go to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play(self) -> Player:
        while not self.is_done():
            player = self.players[self.current_player_index]
            move = player.play(self.board)
            self.play_turn(move)
        return self.get_winner()

    def is_done(self) -> bool:
        return self.winner is not None

    def get_winner(self) -> Optional[Player]:
        return self.winner

    def tie_breaker(self) -> Player:
        min_penalty = float("inf")
        for player in self.players:
            penalty = player.penalty()
            if penalty < min_penalty:
                min_penalty = penalty
                winner = player
            elif penalty == min_penalty:
                player.min_domino().value() < winner.min_domino().value()
                winner = player
        return winner
