//! Perft example - performance testing for move generation.
//!
//! Run with: `cargo run --release --example perft`

use kish::Board;
use std::time::Instant;

/// Known perft values for the standard starting position.
const PERFT_VALUES: &[(u64, u64)] = &[
    (0, 1),
    (1, 23),
    (2, 529),
    (3, 12_283),
    (4, 285_476),
    (5, 6_637_570),
    (6, 154_279_614),
    (7, 3_588_645_578),
    (8, 83_439_556_456),
];

fn main() {
    println!("=== Perft (Performance Test) ===\n");
    println!("Counting positions at each depth from standard starting position.\n");

    let board = Board::new_default();

    println!(
        "{:<8} {:<18} {:<12} {:<18} Correct",
        "Depth", "Nodes", "Time (s)", "Nodes/sec"
    );
    println!("{}", "-".repeat(70));

    for &(depth, expected) in PERFT_VALUES {
        let start = Instant::now();
        let nodes = board.perft(depth);
        let elapsed = start.elapsed().as_secs_f64();

        let nps = if elapsed > 0.0 {
            nodes as f64 / elapsed
        } else {
            f64::INFINITY
        };

        let correct = if nodes == expected { "Yes" } else { "NO!" };

        println!(
            "{:<8} {:<18} {:<12.3} {:<18.0} {}",
            depth, nodes, elapsed, nps, correct
        );

        // Stop if taking too long
        if elapsed > 30.0 {
            println!("\nStopping at depth {depth} (>30s)");
            break;
        }
    }

    println!();
    println!("Tip: Run with --release for optimized performance.");
}
