import unittest
from src.game import Game
from src.player import Player
from src.domino import Domino
from src.strategies.random_strategy import RandomStrategy
from src.board import Board

class TestGame(unittest.TestCase):
    def setUp(self):
        self.players = [Player('Player 1', RandomStrategy()), Player('Player 2', RandomStrategy())]
        self.game = Game(self.players)

    def test_distribute_pieces(self):
        self.game.distribute_pieces(6, 7)
        for player in self.players:
            self.assertEqual(len(player.hand), 7)

    def test_play(self):
        self.game.distribute_pieces(6, 7)
        winner = self.game.play()
        self.assertIn(winner, self.players)

    def test_score(self):
        self.game.distribute_pieces(6, 7)
        self.game.play()
        for player in self.players:
            self.assertGreaterEqual(player.score(), 0)
    
    def test_winner_deadlock(self):
        self.game.players[0].hand = [Domino(1, 2), Domino(3, 4)]
        self.game.players[1].hand = [Domino(5, 6), Domino(7, 8)]
        winner = self.game.play()
        self.assertEqual(winner, self.game.players[0])
        self.assertGreater(winner.score(), 0)

    def test_winner(self):
        self.game.players[0].hand = [Domino(1, 2), Domino(3, 4)]
        self.game.players[1].hand = [Domino(1, 3), Domino(5, 6)]
        winner = self.game.play()
        self.assertEqual(winner, self.game.players[0])
        self.assertEqual(winner.score(), 0)