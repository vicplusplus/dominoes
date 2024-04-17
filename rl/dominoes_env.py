# add ../ to the path
import sys

sys.path.append("../")  # Adjust the path to the directory of the module

import gymnasium as gym
from gymnasium import spaces
from dominoes import Game, Move, Player, Domino
from dominoes.strategies import LargestPieceStrategy
import numpy as np


class DominoesEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, max_value: int, num_pieces: int, num_players: int):
        super(DominoesEnv, self).__init__()
        assert max_value < 255, "max_value is too high for uint8"

        self.action_space = spaces.Discrete(num_pieces * 2 + 1)  # +1 for passing
        self.observation_space = spaces.Box(
            low=np.zeros((num_pieces * 2 * (num_players + 1),), dtype=np.uint8),
            high=np.full(
                (num_pieces * 2 * (num_players + 1),), max_value + 1, dtype=np.uint8
            ),
            shape=(num_pieces * 2 * (num_players + 1),),  # +1 for the hand
            dtype=np.uint8,  # max value will guaranteed fit in an unsigned byte
        )
        self.num_players = num_players
        self.num_pieces = num_pieces
        self.max_value = max_value

        self.reset()

    def step(self, action):
        reward = self._enact_action(action)
        if not self.game.is_done():
            self.game.play_until_player_turn(
                self.player
            )  # Use LargestPieceStrategy to play all turns until it is the agent's turn
        observation = self._get_observation()
        done = self._is_done()
        truncated = False
        info = {
            "won": self.game.get_winner() == self.player,
            "lost": self.game.get_winner() is not None
            and self.game.get_winner() != self.player,
        }

        return observation, reward, done, truncated, info

    def reset(self, seed=None):
        super().reset(seed=seed)
        np.random.seed(seed)
        # randomize the player index
        player_index = np.random.randint(self.num_players)

        # Player list is all LargestPieceStrategy except for the player_index, which will be this agent, so it will not have a strategy
        players = [
            Player(index, LargestPieceStrategy()) for index in range(self.num_players)
        ]
        players[player_index] = Player(player_index, None)
        self.player = players[player_index]

        # Create the game
        self.game = Game(players, self.max_value, self.num_pieces)

        # Distribute the pieces
        self.game.distribute_pieces()

        # Play all turns until it is the agent's turn
        self.game.play_until_player_turn(self.player)

        return self._get_observation(), {}

    def close(self):
        return super().close()

    def _enact_action(self, action) -> float:
        # Implement translating the action into a move in the game
        move = None
        is_valid = True

        if action != self.num_pieces * 2:
            hand_index = action // 2
            side = "left" if action % 2 == 0 else "right"

            if hand_index >= len(self.player.hand):
                move = None
                is_valid = False
            else:
                move = Move(self.player.hand[hand_index], side)
                is_valid = self.game.board.can_play(move)
                if not is_valid:
                    move = None

        self.game.play_turn(move)
        if self.game.get_winner() == self.player:
            return 10
        elif self.game.get_winner() is not None:
            return -self.player.penalty()
        return 1 if is_valid else -1

    def _get_observation(self):
        # First, get the player's hand
        # Simply concatenate the values of the sides of the dominoes and pad with zeros
        hand_observation = np.zeros(self.num_pieces * 2)
        for i, domino in enumerate(self.player.hand):
            hand_observation[i * 2] = domino.left
            hand_observation[i * 2 + 1] = domino.right

        # Next, get the board state
        # Concatenate the values of the sides of the dominoes on the board and pad with zeros
        board_observation = np.zeros(self.num_pieces * 2 * self.num_players)
        for i, domino in enumerate(self.game.board.dominoes):
            board_observation[i * 2] = domino.left
            board_observation[i * 2 + 1] = domino.right

        # Concatenate the hand and board observations
        observation = np.concatenate([hand_observation, board_observation])

        # return the observation converted to a numpy array of uint8
        return observation.astype(np.uint8)

    def _is_done(self):
        return self.game.is_done()
