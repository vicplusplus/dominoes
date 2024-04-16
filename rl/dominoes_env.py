import gymnasium as gym
from gymnasium import spaces
from dominoes import Game, Move, Player, Domino
from dominoes.strategies import LargestPieceStrategy
import numpy as np


class DominoesEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, max_value: int, num_pieces: int, num_players: int):
        super(DominoesEnv, self).__init__()

        self.action_space = spaces.Discrete(num_pieces * 2 + 1)  # +1 for passing
        self.observation_space = spaces.Box(
            low=0,
            high=max_value + 1,
            shape=(num_pieces * 2 * (num_players + 1)),  # +1 for the hand
            dtype=np.uint8,  # max value will guaranteed fit in an unsigned byte
        )
        self.num_players = num_players
        self.num_pieces = num_pieces
        self.max_value = max_value

        self.reset()

    def step(self, action):
        reward = self._enact_action(action)
        self.game.play_until_player_turn(
            self.player
        )  # Use LargestPieceStrategy to play all turns until it is the agent's turn
        observation = self._get_observation()
        done = self._is_done()
        info = {}

        return observation, reward, done, info

    def reset(self):
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

    def render(self, mode="human"):
        # Optional: Implement rendering the game state for visualization
        pass

    def _enact_action(self, action) -> float:
        # Implement translating the action into a move in the game
        if action == self.num_pieces * 2:
            move = None
            return 0
        else:
            hand_index = action // 2
            side = action % 2
            move = Move(self.player[hand_index], side)
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
        return np.array(observation, dtype=np.uint8)

    def _is_done(self):
        return self.game.is_done()
