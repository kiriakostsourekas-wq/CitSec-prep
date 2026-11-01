"""
12 - PROBABILITY & EXPECTED VALUE  (about 3 hours)
==================================================
Quant trading and research final rounds are heavy on "what would you pay to play this game?",
expected values, optimal stopping and Markov chains, answered OUT LOUD.
The goal here is to turn the standard techniques (first-step analysis, backward induction,
Bayes, generating functions) into small exact solvers, and to check them with simulation.

For each task: solve the small case on paper FIRST (the README has the theory),
then code the general solver, then compare with the paper answer.

Exact answers: use fractions.Fraction where it is natural (games, coins); np.linalg.solve
for linear systems. Floats are accepted everywhere (the checker compares numerically).
Randomness: rng = np.random.default_rng(seed). Simulations are checked with wide tolerances.

Run `python check.py` to test, `python check.py B2` for one task, `python exercise.py` for the playground.
"""
import math
from fractions import Fraction
from functools import lru_cache

import numpy as np


# ======================================================================
# PART A - MARKOV CHAINS AND WAITING TIMES
# ======================================================================
def absorbing_expected_steps(P, transient):
    """P: square transition matrix (list of lists or np.array), P[i][j] = P(next = j | now = i).
    transient: list of the indices of the transient (non-absorbing) states.
    Return an np.array t with t[k] = expected number of steps until absorption when starting
    from state transient[k].

    First-step analysis: t_i = 1 + sum_j Q[i][j] * t_j, where Q is P restricted to the
    transient rows/columns. In matrix form (I - Q) t = 1  ->  np.linalg.solve.
    Example: fair walk on 0..4 with 0 and 4 absorbing -> from 1, 2, 3: [3, 4, 3]."""
    raise NotImplementedError


def pattern_expected_flips(pattern, p=0.5):
    """Exact expected number of flips of a coin with P(H) = p until `pattern` (e.g. "HTH")
    first appears.

    States 0..m (m = len(pattern)): "the longest prefix of the pattern that the last flips
    match". State m is absorbing. From state j, flipping c in {"H", "T"} moves you to the
    LONGEST k such that pattern[:k] is a suffix of pattern[:j] + c (KMP idea: after "HT" in
    "HTH", a T sends you to 0, but after "HH" in "HHT" another H keeps you at 2).
    Build the (m+1)x(m+1) transition matrix and reuse absorbing_expected_steps.
    Paper answers: HH 6, HT 4, HHH 14, HTH 10."""
    raise NotImplementedError


def pattern_sim(pattern, p=0.5, n_sims=20_000, seed=0):
    """Monte Carlo estimate of the same expectation: flip until the sequence ends with
    `pattern`, record the number of flips, average over n_sims runs."""
    raise NotImplementedError


# ======================================================================
# PART B - GAMES: WHAT WOULD YOU PAY TO PLAY?
# ======================================================================
def reroll_value(n_rolls, sides=6):
    """Roll a fair die with `sides` faces. After each roll you may stop and be paid the face
    value, or roll again; you have at most n_rolls rolls in total and must accept the last.
    Return the value of the game under optimal play (a Fraction is ideal).

    Backward induction: with 1 roll left the game is worth v1 = (sides+1)/2.
    With k rolls left: v_k = E[max(X, v_{k-1})]  (keep X if it beats the value of continuing).
    d6: 1 -> 7/2, 2 -> 17/4, 3 -> 14/3."""
    raise NotImplementedError


def reflip_coins_value(n=4):
    """Toss n fair coins; you are paid $1 per head. Once, you may re-toss ALL n coins and
    then you must keep the second result. Return the value of the game with optimal play
    (Fraction). Enumerate k = number of heads (Binomial(n, 1/2)) and compare k with the value
    of re-tossing. Which k make you re-toss?"""
    raise NotImplementedError


def red_card_value(r, b):
    """A shuffled deck has r red and b black cards, revealed one at a time. At any moment
    before the deck runs out (at the latest, before the last card) you must say
    "the next card is red" exactly once; you win $1 if it is.
    Return the optimal win probability via DP over (reds left, blacks left):
        V(r, b) = max( r/(r+b)                                   <- say it now
                       r/(r+b) * V(r-1, b) + b/(r+b) * V(r, b-1) )  <- watch one more card
    Use @lru_cache on an inner function. Base cases: V(0, b) = 0, V(r, 0) = 1, and with one
    card left you must say it now. (Surprise: the answer is always r/(r+b). README: why.)"""
    raise NotImplementedError


def guess_sum_value(s1=6, s2=10):
    """Roll a fair s1-sided die and a fair s2-sided die. BEFORE the roll you name a number;
    if the sum equals it you are paid that number (in $), otherwise nothing.
    Return (best_guess, expected_payout), maximising guess * P(sum == guess).
    Ties: return the smallest guess. d6 + d10 -> (11, 1.1)."""
    raise NotImplementedError


# ======================================================================
# PART C - GENERATING FUNCTIONS, BAYES, OPTIMAL STOPPING
# ======================================================================
def extinction_probability(offspring_probs, n_iter=10_000):
    """Branching process: every individual independently has k children with probability
    offspring_probs[k]. Starting from one individual, return P(the family eventually dies out).

    With G(q) = sum_k p_k q^k, q_n = P(extinct by generation n) satisfies q_n = G(q_{n-1}),
    q_0 = 0, and increases to the SMALLEST fixed point of G in [0, 1]. Iterate until it stops
    changing (or n_iter times). Amoeba [1/4, 1/4, 1/4, 1/4] -> sqrt(2) - 1."""
    raise NotImplementedError


def posterior_biased(prior, p_biased, heads, tails):
    """A coin is either fair, or biased with P(H) = p_biased. P(biased) = prior before any flips.
    You observe `heads` heads and `tails` tails (in some order). Return P(biased | data).
    Bayes: prior * L_biased / (prior * L_biased + (1 - prior) * L_fair)."""
    raise NotImplementedError


def prob_next_heads(prior, p_biased, heads, tails):
    """Same setup. Return P(the NEXT flip is heads | data): average the two hypotheses'
    P(H), weighted by their posterior probabilities (use posterior_biased)."""
    raise NotImplementedError


def bust_stop_game(sides=6, bust=1, cap=2_000):
    """Roll a fair die repeatedly, adding the faces to a running total. After any roll you may
    stop and collect the total. If you ever roll the `bust` face, you lose everything (get 0)
    and the game ends. Return (threshold, value):
        threshold = the smallest total s at which stopping is optimal (ties: stop),
        value     = the expected payout from total 0 under optimal play (float).
    DP over the current total s, from a large cap downwards:
        V(s) = max( s,  (1/sides) * sum over non-bust faces f of V(s + f) )   (bust gives 0)
    with V(s) = s once s is so large that you would certainly stop (s near `cap`)."""
    raise NotImplementedError


def bust_stop_sim(threshold, sides=6, bust=1, n_sims=50_000, seed=0):
    """Simulate the strategy "keep rolling while the total is < threshold" for the game above.
    Return the average payout (a bust pays 0)."""
    raise NotImplementedError


# ======================================================================
# PART D - HARDER
# ======================================================================
def penney_prob(a, b):
    """Fair coin flipped until pattern a or pattern b appears (equal lengths, a != b).
    Return P(a appears first).
    States: the longest suffix of the flips so far that is a prefix of a or of b (start: "").
    Let x_s = P(a wins | state s). First-step analysis:
        x_s = 1/2 * x_next(s, "H") + 1/2 * x_next(s, "T"),  with x = 1 if the next flip
        completes a, x = 0 if it completes b.
    That is a linear system M x = rhs; solve it and return x[""].
    P(HH before TH) = 1/4, P(THH before HHT) = 3/4."""
    raise NotImplementedError


def expected_kth_order_stat(k, n, grid=200_001):
    """E[k-th smallest of n i.i.d. Uniform(0,1)] computed NUMERICALLY from the tail formula
        E[Y] = integral_0^1 P(Y > x) dx        (for Y in [0, 1])
    where P(X_(k) > x) = P(fewer than k of the n uniforms are below x)
                       = sum_{j=0}^{k-1} C(n, j) x^j (1 - x)^(n - j).
    Use a grid np.linspace(0, 1, grid) and the trapezoid rule. Compare with k/(n+1)."""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Playground: the tools you will need (nothing here calls your functions).
    print(Fraction(1, 6) + Fraction(1, 3), "|", float(Fraction(14, 3)))  # exact arithmetic
    print("C(4, 2) =", math.comb(4, 2))

    # Solving a linear system: x + y = 3, x - y = 1
    A = np.array([[1.0, 1.0], [1.0, -1.0]])
    print("solve:", np.linalg.solve(A, np.array([3.0, 1.0])))

    # Selecting a sub-matrix by row/column indices
    P = np.arange(16).reshape(4, 4)
    print("P[np.ix_([1, 2], [1, 2])] =\n", P[np.ix_([1, 2], [1, 2])])

    # Memoised recursion
    @lru_cache(maxsize=None)
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)
    print("fib(50) =", fib(50))

    rng = np.random.default_rng(0)
    print("five d6 rolls:", rng.integers(1, 7, size=5), " a coin flip:", "H" if rng.random() < 0.5 else "T")
    print("'HTH'.endswith('TH'):", "HTH".endswith("TH"), "  'HTHH'[:2] =", "HTHH"[:2])
