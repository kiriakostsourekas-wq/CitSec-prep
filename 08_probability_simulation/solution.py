"""
08 - PROBABILITY: EXACT vs MONTE CARLO - REFERENCE SOLUTION
"""
import itertools
import math

import numpy as np


# ======================= PART A =======================
def dice_sum_exact(target, n_dice=2):
    outcomes = list(itertools.product(range(1, 7), repeat=n_dice))
    hits = sum(1 for o in outcomes if sum(o) == target)
    return hits / len(outcomes)


def dice_sum_sim(target, n_dice=2, n_sims=200_000, seed=0):
    rng = np.random.default_rng(seed)
    rolls = rng.integers(1, 7, size=(n_sims, n_dice))   # upper bound 7 is EXCLUSIVE
    return float(np.mean(rolls.sum(axis=1) == target))


def expected_flips_sim(pattern="HH", n_sims=20_000, seed=0):
    rng = np.random.default_rng(seed)
    k = len(pattern)
    total = 0
    for _ in range(n_sims):
        seq = ""
        while seq[-k:] != pattern:
            seq += "H" if rng.random() < 0.5 else "T"
        total += len(seq)
    return total / n_sims
    # Why HH (6) > HT (4): after "H", a failure for HH ("HT") throws you back to the start,
    # while for HT a failure ("HH") still leaves you one H away. Markov-chain derivation for HH:
    #   E0 = 1 + (E1 + E0)/2 ,  E1 = 1 + (0 + E0)/2   ->   E0 = 6.


# ======================= PART B =======================
def birthday_exact(n):
    p_all_different = 1.0
    for i in range(n):
        p_all_different *= (365 - i) / 365
    return 1 - p_all_different


def birthday_sim(n, n_sims=50_000, seed=0):
    rng = np.random.default_rng(seed)
    days = np.sort(rng.integers(0, 365, size=(n_sims, n)), axis=1)
    has_repeat = (np.diff(days, axis=1) == 0).any(axis=1)   # equal neighbours after sorting
    return float(has_repeat.mean())


def estimate_pi(n_points=1_000_000, seed=0):
    rng = np.random.default_rng(seed)
    x, y = rng.random(n_points), rng.random(n_points)
    return float(4 * np.mean(x ** 2 + y ** 2 <= 1))
    # Monte Carlo error shrinks like 1/sqrt(N): 100x more points -> 10x more accuracy.


# ======================= PART C =======================
def gamblers_ruin_exact(start, target, p=0.5):
    if p == 0.5:
        return start / target
    r = (1 - p) / p
    return (1 - r ** start) / (1 - r ** target)
    # For p = 0.5 the wealth is a martingale: E[final] = start = target * P(win) -> P = start/target.


def gamblers_ruin_sim(start, target, p=0.5, n_sims=20_000, seed=0):
    rng = np.random.default_rng(seed)
    wins = 0
    for _ in range(n_sims):
        x = start
        while 0 < x < target:
            x += 1 if rng.random() < p else -1
        wins += x == target
    return wins / n_sims


# ======================= PART D =======================
def bootstrap_ci(data, n_boot=5_000, alpha=0.05, seed=0):
    rng = np.random.default_rng(seed)
    data = np.asarray(data)
    samples = rng.choice(data, size=(n_boot, len(data)), replace=True)
    means = samples.mean(axis=1)
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return float(lo), float(hi)


def coupon_collector_exact(n):
    return n * sum(1 / k for k in range(1, n + 1))


def coupon_collector_sim(n, n_sims=5_000, seed=0):
    rng = np.random.default_rng(seed)
    total = 0
    for _ in range(n_sims):
        seen, draws = set(), 0
        while len(seen) < n:
            seen.add(int(rng.integers(n)))
            draws += 1
        total += draws
    return total / n_sims


if __name__ == "__main__":
    print("P(sum=7):", dice_sum_exact(7), "~", dice_sum_sim(7))
    print("E[flips] HH ~", expected_flips_sim("HH"), " HT ~", expected_flips_sim("HT"))
    print("Birthday n=23:", round(birthday_exact(23), 4), "~", birthday_sim(23))
    print("pi ~", estimate_pi())
    print("Ruin 3->10 p=.5:", gamblers_ruin_exact(3, 10), "~", gamblers_ruin_sim(3, 10))
    print("Ruin 3->10 p=.45:", round(gamblers_ruin_exact(3, 10, 0.45), 4), "~", gamblers_ruin_sim(3, 10, 0.45))
    data = np.random.default_rng(1).exponential(2.0, 50)
    print("Bootstrap 95% CI for the mean:", np.round(bootstrap_ci(data), 3), " sample mean", round(data.mean(), 3))
    print("Coupon n=6:", round(coupon_collector_exact(6), 3), "~", coupon_collector_sim(6))
