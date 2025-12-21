"""Basic game example - play moves and check game status."""

import kish


def main():
    # Create a new game with standard starting position
    board = kish.Board()
    print("Starting position:")
    print(board)
    print()

    # Get legal moves
    actions = board.actions()
    print(f"White has {len(actions)} legal moves:")
    for action in actions[:5]:  # Show first 5
        print(f"  {action.notation()}")
    if len(actions) > 5:
        print(f"  ... and {len(actions) - 5} more")
    print()

    # Play a few moves
    print("Playing some moves:")
    move_count = 0
    while not board.status().is_over() and move_count < 10:
        actions = board.actions()
        if not actions:
            break

        # Pick the first move (you could pick randomly or use AI here)
        action = actions[0]
        print(f"  {board.turn}: {action.notation()}")

        # Apply move (returns new board)
        board = board.apply(action)
        move_count += 1

    print()
    print(f"Position after {move_count} moves:")
    print(board)

    # Check game status
    status = board.status()
    if status.is_in_progress():
        print("Game is still in progress")
    elif status.is_draw():
        print("Game ended in a draw")
    else:
        print(f"Game won by {status.winner()}")


if __name__ == "__main__":
    main()
