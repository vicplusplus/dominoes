import gymnasium as gym
from gymnasium import spaces
from typing import Tuple
from dominoes import Game, Player


class DominoesEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, max_value: int, pieces_per_hand: int):
        super(DominoesEnv, self).__init__()
        self.game = None
        self.action_space = None  # Define your action space
        self.observation_space = None  # Define your observation space
        self.max_value = max_value
        self.pieces_per_hand = pieces_per_hand
        self.setup()

    def setup(self):
        # Initialize your game here with 4 players
        players = [Player() for _ in range(4)]
        self.game = Game(players, self.max_value, self.pieces_per_hand)
        # Setup your action and observation spaces based on the game

    def step(self, action):
        # Implement taking a step in the game
        # This should involve translating the action into a move in the game, updating the game state, and returning observation, reward, done, info
        return observation, reward, done, info

    def reset(self):
        # Reset the environment/game
        self.setup()
        # Return initial observation
        return observation

    def render(self, mode="human"):
        # Optional: Implement rendering the game state for visualization
        pass
