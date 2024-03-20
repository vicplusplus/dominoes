from typing import List
from random import shuffle

from src.board import Board
from src.domino import Domino
from src.player import Player


class Game:
    def __init__(self, players: list[Player], max_value: int, pieces_per_hand: int, initial_player: int = 0) -> None:
        self.board: Board = Board()
        self.players: List[Player] = players
        self.initial_player = initial_player
        self.max_value = max_value
        self.pieces_per_hand = pieces_per_hand

    def distribute_pieces(self, max_value: int, pieces_per_hand: int) -> None:
        # generate all possible dominoes
        dominoes = [Domino(left, right) for left in range(max_value + 1) for right in range(left, max_value + 1)]
        # shuffle the dominoes
        shuffle(dominoes)
        # give each player a hand of dominoes
        for player in self.players:
            player.hand = dominoes[:pieces_per_hand]
            dominoes = dominoes[pieces_per_hand:]

    def play(self) -> Player:
        # set initial values
        self.current_player_index = self.initial_player
        self.passes = 0
        self.winner = None
        # play until there is a winner
        while not self.winner:
            # get the domino played by the player
            played = self.players[self.current_player_index].play(self.board.dominoes)
            # if the player can't play, pass
            if not played:
                self.passes += 1
            else:
                self.passes = 0
                # add the domino to the board
                self.board.add(played.domino, played.side)
                # check if the player has won
                if not self.current_player.hand:
                    self.winner = self.current_player
            # go to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            # if all players have passed, winner is the player with the lowest score
            if self.passes == len(self.players):
                self.winner = min(self.players, key=lambda player: player.score())
        return self.winner
    

