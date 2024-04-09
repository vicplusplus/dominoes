from src.game import Game
from src.player import Player
from src.strategies.random_strategy import RandomStrategy
from src.strategies.largest_piece_strategy import LargestPieceStrategy
from src.strategies.aggregate_minimax_strategy import AggregateMinimaxStrategy
from src.strategies.smallest_piece_strategy import SmallestPieceStrategy
from itertools import product
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

NUM_PLAYERS = 4
MAX_VALUE = 6
NUM_PIECES = 7

NUM_GAMES = 100


def simulate_games(strategy_combination):
    wins = [0] * NUM_PLAYERS
    penalties = [0] * NUM_PLAYERS
    for _ in range(NUM_GAMES):
        players = [
            Player(index, strategy)
            for index, strategy in enumerate(strategy_combination)
        ]
        game = Game(players, MAX_VALUE, NUM_PIECES)
        game.distribute_pieces()
        winner = game.play()
        wins[int(winner.name)] += 1
        for _, player in enumerate(game.players):
            penalties[int(player.name)] += player.penalty()
    return strategy_combination, wins, [penalty / 100 for penalty in penalties]


def main():
    strategies = [
        RandomStrategy(),
        LargestPieceStrategy(),
        SmallestPieceStrategy(),
        AggregateMinimaxStrategy(10),
    ]
    strategy_combinations = list(product(strategies, repeat=NUM_PLAYERS))

    num_cores = multiprocessing.cpu_count()
    results = {}

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(simulate_games, sc) for sc in strategy_combinations]

        for future in futures:
            strategy_combination, wins, avg_penalty = future.result()
            results[strategy_combination] = (wins, avg_penalty)

    total_wins = [0] * len(strategies)
    total_scores = [0] * len(strategies)

    # Create a dictionary to map each strategy to its index for easy lookup
    strategy_index_map = {
        str(strategy): index for index, strategy in enumerate(strategies)
    }

    # Aggregating wins and scores based on strategy
    for strategy_combination, (wins, penalties) in results.items():
        for player_index, strategy in enumerate(strategy_combination):
            # Use the strategy as a key to find the corresponding index
            strategy_idx = strategy_index_map[str(strategy)]
            total_wins[strategy_idx] += wins[player_index]
            total_scores[strategy_idx] += penalties[player_index]

    # Normalize scores if needed (depending on how you want to represent them)
    total_scores = [score / len(results) for score in total_scores]

    # Display the results
    for i, strategy in enumerate(strategies):
        print(
            f"Strategy {str(strategy)}: Total Wins = {total_wins[i]}, Average Penalty = {total_scores[i]:.2f}"
        )


if __name__ == "__main__":
    main()
