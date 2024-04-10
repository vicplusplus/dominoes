import gymnasium as gym
from gymnasium import spaces
from dominoes import Game, Move, Player, Domino
import numpy as np


class DominoesEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, game: Game, player: Player):
        super(DominoesEnv, self).__init__()
        self.game = game
        self.max_value = game.board.max_value
        self.num_players = len(game.players)
        self.pieces_per_hand = game.board.pieces_per_hand
        self.player = player

        self.action_space = spaces.Discrete(
            self.pieces_per_hand * 2 + 1
        )  # +1 for passing
        self.observation_space = spaces.Box(
            low=0,
            high=self.max_value + 1,
            shape=(
                self.pieces_per_hand * 2 * (self.num_players + 1)
            ),  # +1 for the hand
            dtype=np.uint8,  # max value will guaranteed fit in an unsigned byte
        )

    def step(self, action):
        # Implement taking a step in the game
        # This should involve translating the action into a move in the game, updating the game state, and returning observation, reward, done, info
        reward = self._enact_action(action)
        observation = self._get_observation()
        done = self._is_done()
        info = {}

        return observation, reward, done, info

    def reset(self):
        # Reset the environment/game
        # Return initial observation
        if self.game.is_done():
            self.game.reset()
        return self._get_observation()

    def render(self, mode="human"):
        # Optional: Implement rendering the game state for visualization
        pass

    def _enact_action(self, action) -> float:
        # Implement translating the action into a move in the game
        if action == self.pieces_per_hand * 2:
            move = None
            return 0
        else:
            hand_index = action // 2
            side = action % 2
            move = Move(self.player.hand[hand_index], side)
            if not self.game.board.can_play(move):
                return -1

        self.game.play_turn(move)
        if self.game.get_winner() == self.player:
            return 10
        elif self.game.get_winner() is not None:
            return -self.player.penalty()
        return 1

    def _get_observation(self):
        # First, get the player's hand
        # Simply concatenate the values of the sides of the dominoes and pad with zeros
        hand_observation = np.zeros(self.pieces_per_hand * 2)
        for i, domino in enumerate(self.player.hand):
            hand_observation[i * 2] = domino.left
            hand_observation[i * 2 + 1] = domino.right

        # Next, get the board state
        # Concatenate the values of the sides of the dominoes on the board and pad with zeros
        board_observation = np.zeros(self.pieces_per_hand * 2 * self.num_players)
        for i, domino in enumerate(self.game.board.dominoes):
            board_observation[i * 2] = domino.left
            board_observation[i * 2 + 1] = domino.right

        # Concatenate the hand and board observations
        observation = np.concatenate([hand_observation, board_observation])

        # return the observation converted to a numpy array of uint8
        return np.array(observation, dtype=np.uint8)

    def _is_done(self):
        return self.game.is_done()
