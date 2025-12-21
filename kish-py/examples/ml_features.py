"""Machine learning features example - bitboard access and tensor conversion."""

import kish

# Optional: numpy for tensor operations
try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("Note: numpy not installed, skipping tensor examples\n")


def board_to_bitplanes(board: kish.Board) -> "np.ndarray":
    """Convert board to 4x8x8 tensor for CNN input.

    Planes:
    - 0: White pieces (1 where white piece exists)
    - 1: Black pieces (1 where black piece exists)
    - 2: Kings (1 where king exists)
    - 3: Turn (all 1s if black to move, all 0s if white)
    """
    w, b, k, turn = board.bitboards()

    planes = np.zeros((4, 8, 8), dtype=np.float32)
    for i in range(64):
        row, col = i // 8, i % 8
        planes[0, row, col] = (w >> i) & 1
        planes[1, row, col] = (b >> i) & 1
        planes[2, row, col] = (k >> i) & 1
    planes[3, :, :] = turn

    return planes


def board_to_bitplanes_fast(board: kish.Board) -> "np.ndarray":
    """Optimized version using numpy bit unpacking."""
    w, b, k, turn = board.bitboards()

    def unpack(bb: int) -> np.ndarray:
        """Unpack u64 bitboard to 64 floats."""
        bytes_arr = np.array([bb], dtype=">u8").view(np.uint8)
        bits = np.unpackbits(bytes_arr)[::-1]  # Reverse for correct order
        return bits.astype(np.float32)

    planes = np.zeros((4, 64), dtype=np.float32)
    planes[0] = unpack(w)
    planes[1] = unpack(b)
    planes[2] = unpack(k)
    planes[3] = turn

    return planes.reshape(4, 8, 8)


def action_to_features(action: kish.Action) -> dict:
    """Extract features from an action for policy network training."""
    return {
        "source": action.source(),
        "destination": action.destination(),
        "source_idx": int(action.source()),
        "dest_idx": int(action.destination()),
        "is_capture": action.is_capture(),
        "is_promotion": action.is_promotion(),
        "capture_count": action.capture_count(),
        "captured_bitboard": action.captured_bitboard(),
        "delta": action.delta_array(),
    }


def main():
    board = kish.Board()

    # === Bitboard Access ===
    print("=== Bitboard Access ===")
    print(f"White bitboard: 0x{board.white_bitboard():016X}")
    print(f"Black bitboard: 0x{board.black_bitboard():016X}")
    print(f"Kings bitboard: 0x{board.kings_bitboard():016X}")
    print()

    # All at once (most efficient)
    white, black, kings, turn = board.bitboards()
    print(f"Turn: {'White' if turn == 0 else 'Black'}")
    print()

    # As array for numpy
    arr = board.to_array()
    print(f"Board array: {arr}")
    print()

    # === Action Features ===
    print("=== Action Features ===")
    actions = board.actions()
    action = actions[0]

    print(f"Action: {action.notation()}")
    print(f"  Source: {action.source()} (index {int(action.source())})")
    print(f"  Destination: {action.destination()} (index {int(action.destination())})")
    print(f"  Is capture: {action.is_capture()}")
    print(f"  Delta: {action.delta()}")
    print()

    # === Distance Heuristics ===
    print("=== Distance Heuristics ===")
    sq1 = kish.Square.D4
    sq2 = kish.Square.H8
    print(f"Manhattan distance {sq1} to {sq2}: {sq1.manhattan(sq2)}")

    # Distance to promotion row
    for sq in [kish.Square.A3, kish.Square.D5, kish.Square.H7]:
        white_dist = 7 - sq.row()  # White promotes on row 7 (rank 8)
        black_dist = sq.row()  # Black promotes on row 0 (rank 1)
        print(f"  {sq}: White promotion dist={white_dist}, Black={black_dist}")
    print()

    # === Numpy Tensor Conversion ===
    if HAS_NUMPY:
        print("=== Numpy Tensor Conversion ===")

        # Convert to bit planes
        planes = board_to_bitplanes(board)
        print(f"Bit planes shape: {planes.shape}")
        print(f"White pieces plane:\n{planes[0]}")
        print()

        # Fast version
        planes_fast = board_to_bitplanes_fast(board)
        assert np.allclose(planes, planes_fast), "Mismatch!"
        print("Fast conversion matches standard conversion")
        print()

        # Action features as dict
        features = action_to_features(action)
        print(f"Action features: {features}")


if __name__ == "__main__":
    main()
