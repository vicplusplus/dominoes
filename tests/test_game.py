import unittest
from dominoes import Domino, Game, Player
from dominoes.strategies import RandomStrategy


class TestGame(unittest.TestCase):
    def setUp(self):
        self.players = [
            Player("Player 1", RandomStrategy()),
            Player("Player 2", RandomStrategy()),
        ]
        self.game = Game(self.players, 9, 7)

    def test_distribute_pieces(self):
        self.game.distribute_pieces()
        for player in self.players:
            self.assertEqual(len(player.hand), 7)
        # each hand should have unique dominoes
        self.assertNotEqual(self.players[0].hand, self.players[1].hand)

    def test_play(self):
        winner = self.game.play()
        self.assertIn(winner, self.players)

    def test_score(self):
        self.game.play()
        for player in self.players:
            self.assertGreaterEqual(player.penalty(), 0)

    def test_winner_deadlock(self):
        self.game.players[0].hand = [Domino(1, 2), Domino(3, 4)]
        self.game.players[1].hand = [Domino(5, 6), Domino(7, 8)]
        winner = self.game.play()
        self.assertEqual(winner, self.game.players[0])
        self.assertGreater(winner.penalty(), 0)

    def test_winner(self):
        self.game.players[0].hand = [Domino(1, 2), Domino(3, 4)]
        self.game.players[1].hand = [Domino(1, 3), Domino(5, 6)]
        winner = self.game.play()
        self.assertEqual(winner, self.game.players[0])
        self.assertEqual(winner.penalty(), 0)
