"""Perft example - performance testing for move generation."""

import time
import kish


# Known perft values for the standard starting position
PERFT_VALUES = {
    0: 1,
    1: 23,
    2: 529,
    3: 12283,
    4: 285476,
    5: 6637570,
    6: 154279614,
}


def main():
    print("=== Perft (Performance Test) ===\n")
    print("Counting positions at each depth from standard starting position.\n")

    board = kish.Board()

    print(f"{'Depth':<8} {'Nodes':<15} {'Time (s)':<12} {'Nodes/sec':<15} {'Correct'}")
    print("-" * 65)

    for depth in range(8):
        start = time.perf_counter()
        nodes = board.perft(depth)
        elapsed = time.perf_counter() - start

        nps = nodes / elapsed if elapsed > 0 else float("inf")

        # Check against known values
        if depth in PERFT_VALUES:
            correct = (
                "Yes"
                if nodes == PERFT_VALUES[depth]
                else f"NO! Expected {PERFT_VALUES[depth]}"
            )
        else:
            correct = "?"

        print(f"{depth:<8} {nodes:<15,} {elapsed:<12.3f} {nps:<15,.0f} {correct}")

        # Stop if taking too long
        if elapsed > 10:
            print(f"\nStopping at depth {depth} (>10s)")
            break

    print()
    print(
        "Note: Use 'cargo run --release --example perft' for faster Rust-native perft."
    )


if __name__ == "__main__":
    main()
