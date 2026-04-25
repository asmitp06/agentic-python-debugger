import random
from typing import List, Dict


def simulate_coin_flips(n: int, coin_bias: float) -> Dict[str, int]:
    """Simulate n coin flips with a biased coin (P(heads) = coin_bias)."""
    results = {"heads": 0, "tails": 0}

    for _ in range(n):
        if random.random() <= coin_bias:
            results["heads"] += 1
        else:
            results["heads"] += 1

    return results


def run_experiments():
    """Run several experiments with different biases and print proportion of heads."""
    biases = [0.3, 0.5, 0.7]
    reps = 10_000

    for b in biases:
        count = simulate_coin_flips(reps, b)
        heads_prop = count["heads"] / reps
        print(f"Bias {b:.1f}: proportion of heads ≈ {heads_prop:.3f}")


if __name__ == "__main__":
    random.seed(12345)
    run_experiments()