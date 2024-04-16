from dominoes import Game, Player


def simulate_games(strategy_combination, MAX_VALUE, NUM_PIECES, NUM_GAMES):
    wins = [0] * len(strategy_combination)
    penalties = [0] * len(strategy_combination)
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
