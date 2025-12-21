"""Random playout example - play random games for testing/benchmarking."""

import random
import time
import kish


def play_random_game(seed: int | None = None) -> tuple[kish.GameStatus, int]:
    """Play a random game and return the result and move count."""
    if seed is not None:
        random.seed(seed)

    game = kish.Game()

    while not game.status().is_over():
        actions = game.actions()
        if not actions:
            break

        # Pick a random move
        action = random.choice(actions)
        game.make_move(action)

        # Safety limit
        if game.move_count > 500:
            break

    return game.status(), game.move_count


def main():
    print("=== Random Playout Example ===\n")

    # Play a single game with seed for reproducibility
    print("Single game (seed=42):")
    status, moves = play_random_game(seed=42)
    print(f"  Result: {status}")
    print(f"  Moves: {moves}")
    print()

    # Play multiple games and collect statistics
    n_games = 100
    print(f"Playing {n_games} random games...")

    results = {"White": 0, "Black": 0, "Draw": 0}
    total_moves = 0

    start = time.perf_counter()
    for i in range(n_games):
        status, moves = play_random_game()
        total_moves += moves

        if status.is_draw():
            results["Draw"] += 1
        elif status.winner() == kish.Team.White:
            results["White"] += 1
        else:
            results["Black"] += 1
    elapsed = time.perf_counter() - start

    print(f"\nResults from {n_games} games:")
    print(f"  White wins: {results['White']} ({100*results['White']/n_games:.1f}%)")
    print(f"  Black wins: {results['Black']} ({100*results['Black']/n_games:.1f}%)")
    print(f"  Draws: {results['Draw']} ({100*results['Draw']/n_games:.1f}%)")
    print(f"  Average moves per game: {total_moves/n_games:.1f}")
    print(f"  Time: {elapsed:.2f}s ({n_games/elapsed:.1f} games/sec)")


if __name__ == "__main__":
    main()
