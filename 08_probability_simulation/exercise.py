"""
08 - PROBABILITY WITH PYTHON: EXACT vs MONTE CARLO  (about 1-1.5 hours)
========================================================================
Citadel loves probability. If you have a strong math background you can probably solve
these on paper - the point here is to CODE them fluently and to verify a
paper answer with a quick simulation (a very good habit to show in interviews:
"I think it's 6 - let me sanity-check with a simulation").

For each problem: solve it on paper first, then write the exact function, then the
simulation, and check they agree.

Use rng = np.random.default_rng(seed) for all randomness.
Simulations are checked with tolerances, so any correct approach passes.

Run `python check.py` to test, `python exercise.py` for the playground.
"""
import itertools
import math

import numpy as np


# ======================================================================
# PART A - DICE AND COINS
# ======================================================================
def dice_sum_exact(target, n_dice=2):
    """Exact P(sum of n_dice fair six-sided dice == target), by enumerating all
    6**n_dice outcomes (itertools.product(range(1, 7), repeat=n_dice))."""
    raise NotImplementedError


def dice_sum_sim(target, n_dice=2, n_sims=200_000, seed=0):
    """Monte Carlo estimate of the same probability. Vectorize:
    rng.integers(1, 7, size=(n_sims, n_dice)) gives all the rolls at once."""
    raise NotImplementedError


def expected_flips_sim(pattern="HH", n_sims=20_000, seed=0):
    """Average number of fair-coin flips needed until `pattern` (e.g. "HH" or "HT")
    first appears. (A plain Python loop per simulation is fine here.)
    Paper answers to check against: HH -> 6, HT -> 4. Why are they different?!"""
    raise NotImplementedError


# ======================================================================
# PART B - CLASSICS
# ======================================================================
def birthday_exact(n):
    """P(at least two of n people share a birthday), 365 equally likely days.
    = 1 - (365/365)(364/365)...((365-n+1)/365)"""
    raise NotImplementedError


def birthday_sim(n, n_sims=50_000, seed=0):
    """Simulate: draw n birthdays per trial, check for a repeat.
    (Hint: sort each row, then check whether any neighbours are equal.)"""
    raise NotImplementedError


def estimate_pi(n_points=1_000_000, seed=0):
    """Throw uniform points into the square [0,1]^2; the fraction inside the quarter
    circle x^2 + y^2 <= 1 estimates pi/4. Return the estimate of pi."""
    raise NotImplementedError


# ======================================================================
# PART C - RANDOM WALKS (Gambler's ruin)
# ======================================================================
def gamblers_ruin_exact(start, target, p=0.5):
    """You have `start` dollars and bet $1 each round, winning with prob p.
    Return P(reach `target` before 0).
        p == 0.5:  start / target
        otherwise: (1 - r**start) / (1 - r**target)  with r = (1-p)/p"""
    raise NotImplementedError


def gamblers_ruin_sim(start, target, p=0.5, n_sims=20_000, seed=0):
    """Simulate the walk until it hits 0 or target. Return the fraction that hit target."""
    raise NotImplementedError


# ======================================================================
# PART D - STATISTICS BY SIMULATION
# ======================================================================
def bootstrap_ci(data, n_boot=5_000, alpha=0.05, seed=0):
    """Percentile bootstrap confidence interval for the MEAN of `data`:
      repeat n_boot times: resample len(data) points WITH replacement, record the mean
      return (lower, upper) = the alpha/2 and 1-alpha/2 quantiles of those means
    (np.quantile). Vectorized version: rng.choice(data, size=(n_boot, n), replace=True)."""
    raise NotImplementedError


def coupon_collector_exact(n):
    """Expected number of draws (uniform with replacement) to see all n distinct coupons:
    n * (1 + 1/2 + ... + 1/n). Derive it: after collecting k coupons, the wait for a new one
    is Geometric with success prob (n-k)/n, so its mean is n/(n-k)."""
    raise NotImplementedError


def coupon_collector_sim(n, n_sims=5_000, seed=0):
    """Simulate drawing until all n coupons are seen; return the average number of draws."""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    print(rng.integers(1, 7, size=(3, 2)))     # 3 trials of 2 dice
    print(rng.random(5))                       # 5 uniforms in [0,1)
    print(rng.choice([10, 20, 30], size=4))    # sampling with replacement
