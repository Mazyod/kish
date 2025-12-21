"""Custom position example - set up specific board states."""

import kish


def main():
    # Create a custom position with specific pieces
    # White king on D4, white pawn on E3
    # Black pawns on D5 and F6
    board = kish.Board.from_squares(
        turn=kish.Team.White,
        white_squares=[kish.Square.D4, kish.Square.E3],
        black_squares=[kish.Square.D5, kish.Square.F6],
        king_squares=[kish.Square.D4],  # D4 is a king
    )

    print("Custom position:")
    print(board)
    print()

    # Query pieces
    print(f"White pieces: {[sq.notation() for sq in board.white_pieces()]}")
    print(f"Black pieces: {[sq.notation() for sq in board.black_pieces()]}")
    print(f"Kings: {[sq.notation() for sq in board.kings()]}")
    print()

    # Get legal moves
    actions = board.actions()
    print(f"Legal moves for {board.turn}:")
    for action in actions:
        details = []
        if action.is_capture():
            details.append(f"captures {action.capture_count()}")
        if action.is_promotion():
            details.append("promotes")
        suffix = f" ({', '.join(details)})" if details else ""
        print(f"  {action.notation()}{suffix}")
    print()

    # Create position from bitboards (useful for ML)
    white_bb = 0x0000_0000_0000_FF00  # Row 2
    black_bb = 0x00FF_0000_0000_0000  # Row 7
    kings_bb = 0x0000_0000_0000_0000  # No kings

    board2 = kish.Board.from_bitboards(
        turn=0,  # White
        white=white_bb,
        black=black_bb,
        kings=kings_bb,
    )

    print("Position from bitboards:")
    print(board2)


if __name__ == "__main__":
    main()
