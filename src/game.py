from typing import List
from random import shuffle

from src.board import Board
from src.domino import Domino
from src.player import Player


class Game:
    def __init__(self, players: list[Player], max_value: int, pieces_per_hand: int) -> None:
        self.board: Board = Board(max_value, len(players), pieces_per_hand)
        self.players: List[Player] = players

    def distribute_pieces(self, max_value: int) -> None:
        # generate all possible dominoes
        dominoes = Domino.generate_all(max_value)
        # shuffle the dominoes
        shuffle(dominoes)
        # give each player a hand of dominoes
        for player in self.players:
            player.hand = dominoes[:self.board.pieces_per_hand]
            dominoes = dominoes[len(dominoes) - self.board.pieces_per_hand:]

    def play(self, initial_player: int = 0) -> Player:
        # set initial values
        current_player_index = initial_player
        passes = 0
        winner = None
        # play until there is a winner
        while not winner:
            # get the domino played by the player
            played = self.players[current_player_index].play(self.board)
            # if the player can't play, pass
            if not played:
                passes += 1
            else:
                passes = 0
                # add the domino to the board
                self.board.add(played.domino, played.side)
                # check if the player has won
                if not self.players[current_player_index].hand:
                    winner = self.players[current_player_index]
            # go to the next player
            current_player_index = (current_player_index + 1) % len(self.players)
            # if all players have passed, winner is the player with the lowest score
            if passes == len(self.players):
                winner = min(self.players, key=lambda player: player.score())
        return winner
    

