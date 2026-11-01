"""
12 - PROBABILITY & EXPECTED VALUE - REFERENCE SOLUTION
"""
import math
from fractions import Fraction
from functools import lru_cache

import numpy as np


# ======================================================================
# PART A - MARKOV CHAINS AND WAITING TIMES
# ======================================================================
def absorbing_expected_steps(P, transient):
    P = np.asarray(P, dtype=float)
    Q = P[np.ix_(transient, transient)]           # transient -> transient block
    n = len(transient)
    # t_i = 1 + sum_j Q_ij t_j   <=>   (I - Q) t = 1
    return np.linalg.solve(np.eye(n) - Q, np.ones(n))
    # (I - Q)^-1 is the "fundamental matrix" N: N_ij = expected visits to j starting from i.


def _next_state(pattern, j, c):
    """Longest prefix of `pattern` that is a suffix of pattern[:j] + c (KMP automaton)."""
    s = pattern[:j] + c
    for k in range(min(len(s), len(pattern)), -1, -1):
        if s.endswith(pattern[:k]):
            return k
    return 0


def pattern_expected_flips(pattern, p=0.5):
    m = len(pattern)
    # states 0..m = "length of the longest prefix of the pattern matched right now"; m is absorbing
    P = np.zeros((m + 1, m + 1))
    for j in range(m):
        P[j, _next_state(pattern, j, "H")] += p
        P[j, _next_state(pattern, j, "T")] += 1 - p
    P[m, m] = 1.0
    return float(absorbing_expected_steps(P, list(range(m)))[0])
    # Fair-coin shortcut (Conway / "casino" martingale argument): E = sum of 2^k over every k
    # such that the length-k prefix equals the length-k suffix. HH: 2+4=6, HTH: 2+8=10, HHH: 2+4+8=14.
    # Biased HH: E = (1+p)/p^2.


def pattern_sim(pattern, p=0.5, n_sims=20_000, seed=0):
    rng = np.random.default_rng(seed)
    k = len(pattern)
    total = 0
    for _ in range(n_sims):
        seq = ""
        while seq[-k:] != pattern:
            seq += "H" if rng.random() < p else "T"
        total += len(seq)
    return total / n_sims


# ======================================================================
# PART B - GAMES: WHAT WOULD YOU PAY TO PLAY?
# ======================================================================
def reroll_value(n_rolls, sides=6):
    faces = range(1, sides + 1)
    v = Fraction(sides + 1, 2)                 # one roll left: you must keep it
    for _ in range(n_rolls - 1):
        # keep the current roll x if x >= v (value of continuing), else roll again
        v = sum(max(Fraction(x), v) for x in faces) / sides
    return v
    # d6: 1 roll 7/2, 2 rolls 17/4 (keep 4,5,6), 3 rolls 14/3 (keep 5,6), 4 rolls 89/18.


def reflip_coins_value(n=4):
    total = Fraction(0)
    reflip_value = Fraction(n, 2)              # re-tossing all coins is worth n/2 on average
    for k in range(n + 1):
        prob = Fraction(math.comb(n, k), 2 ** n)
        total += prob * max(Fraction(k), reflip_value)
    return total
    # Threshold: re-toss iff #heads < n/2 (at exactly n/2 you are indifferent).
    # n=4: keep 2,3,4 heads, re-toss 0 or 1 -> value = (5/16)*2 + (6/16)*2 + (4/16)*3 + (1/16)*4 = 19/8.


def red_card_value(r, b):
    @lru_cache(maxsize=None)
    def V(r, b):
        if r == 0:
            return Fraction(0)
        if b == 0:
            return Fraction(1)
        n = r + b
        stop_now = Fraction(r, n)
        if n == 1:
            return stop_now                    # last card: you must call it now
        wait = Fraction(r, n) * V(r - 1, b) + Fraction(b, n) * V(r, b - 1)
        return max(stop_now, wait)
    return V(r, b)
    # Always equals r/(r+b): the fraction of red cards left is a martingale, so by optional
    # stopping every strategy (calling now, waiting, anything) wins with the same probability.


def guess_sum_value(s1=6, s2=10):
    counts = {}
    for a in range(1, s1 + 1):
        for b in range(1, s2 + 1):
            counts[a + b] = counts.get(a + b, 0) + 1
    best_guess, best_value = None, Fraction(-1)
    for s in sorted(counts):
        value = Fraction(s * counts[s], s1 * s2)
        if value > best_value:                 # strict ">" keeps the smallest guess on ties
            best_guess, best_value = s, value
    return best_guess, best_value
    # d6+d10: P(sum) is flat (6/60) for sums 7..11, so take the largest of them: 11 -> 66/60 = 1.1.


# ======================================================================
# PART C - GENERATING FUNCTIONS, BAYES, OPTIMAL STOPPING
# ======================================================================
def extinction_probability(offspring_probs, n_iter=10_000):
    q = 0.0
    for _ in range(n_iter):
        q_new = sum(pk * q ** k for k, pk in enumerate(offspring_probs))
        if abs(q_new - q) < 1e-15:
            break
        q = q_new
    return q
    # q_n = P(extinct by generation n) = G(q_{n-1}) increases to the SMALLEST root of G(q) = q.
    # Amoeba [1/4]*4: q = (1+q+q^2+q^3)/4 -> (q-1)(q^2+2q-1) = 0 -> q = sqrt(2)-1.
    # Rule: mean offspring m <= 1 -> q = 1 (except the trivial p_1 = 1); m > 1 -> q < 1.


def posterior_biased(prior, p_biased, heads, tails):
    like_biased = p_biased ** heads * (1 - p_biased) ** tails
    like_fair = 0.5 ** (heads + tails)
    return prior * like_biased / (prior * like_biased + (1 - prior) * like_fair)


def prob_next_heads(prior, p_biased, heads, tails):
    post = posterior_biased(prior, p_biased, heads, tails)
    return post * p_biased + (1 - post) * 0.5
    # Predictive = average of each hypothesis's P(H), weighted by its posterior.


def bust_stop_game(sides=6, bust=1, cap=2_000):
    good = [f for f in range(1, sides + 1) if f != bust]
    V = {}                                     # V[s] = value with current total s (exact Fractions)
    threshold = None
    for s in range(cap, -1, -1):
        if s + max(good) > cap:
            V[s] = Fraction(s)                 # far beyond any sensible threshold: stop
            continue
        cont = sum(V[s + f] for f in good) / sides
        V[s] = max(Fraction(s), cont)
        if s >= cont:                          # stopping is (weakly) optimal at s
            threshold = s                      # keeps decreasing -> smallest such s at the end
    return threshold, float(V[0])
    # One-step look-ahead: rolling once more changes the total by -s/6 + (2+3+4+5+6)/6 = (20 - s)/6,
    # so continue iff s < 20. The problem is "monotone" (once you'd stop, you'd stop at every later
    # state) so the one-step rule is optimal. d6 bust on 1: stop at 20, value ~= 8.1418.


def bust_stop_sim(threshold, sides=6, bust=1, n_sims=50_000, seed=0):
    rng = np.random.default_rng(seed)
    total = 0
    for _ in range(n_sims):
        s = 0
        while s < threshold:
            roll = int(rng.integers(1, sides + 1))
            if roll == bust:
                s = 0
                break
            s += roll
        total += s
    return total / n_sims


# ======================================================================
# PART D - HARDER
# ======================================================================
def penney_prob(a, b):
    """P(pattern a appears before pattern b), fair coin."""
    prefixes = {a[:k] for k in range(len(a))} | {b[:k] for k in range(len(b))}
    states = sorted(prefixes, key=lambda s: (len(s), s))          # "" first
    index = {s: i for i, s in enumerate(states)}

    def step(s, c):
        t = s + c
        if t.endswith(a):
            return "A"
        if t.endswith(b):
            return "B"
        while t not in prefixes:                                   # longest suffix that is a prefix
            t = t[1:]
        return t

    n = len(states)
    M = np.eye(n)
    rhs = np.zeros(n)
    for s in states:
        i = index[s]
        for c in "HT":
            nxt = step(s, c)
            if nxt == "A":
                rhs[i] += 0.5
            elif nxt != "B":
                M[i, index[nxt]] -= 0.5
    return float(np.linalg.solve(M, rhs)[index[""]])
    # Conway's check: odds(a before b) = (L(b,b) - L(b,a)) : (L(a,a) - L(a,b)), where
    # L(x,y) = sum of 2^(k-1) over k such that the last k letters of x = the first k letters of y.
    # THH vs HHT: L(HHT,HHT)=4, L(HHT,THH)=1, L(THH,THH)=4, L(THH,HHT)=3 -> odds 3:1 -> 3/4.


def expected_kth_order_stat(k, n, grid=200_001):
    x = np.linspace(0.0, 1.0, grid)
    # P(X_(k) > x) = P(fewer than k of the n uniforms are below x)
    tail = sum(math.comb(n, j) * x ** j * (1 - x) ** (n - j) for j in range(k))
    # E[Y] = integral of P(Y > x) dx for Y in [0,1]; trapezoid rule:
    dx = x[1] - x[0]
    return float(dx * (tail.sum() - 0.5 * (tail[0] + tail[-1])))
    # Exactly: each term integrates to C(n,j) * j!(n-j)!/(n+1)! = 1/(n+1), so E = k/(n+1).
    # Max of n uniforms: n/(n+1); min: 1/(n+1).


if __name__ == "__main__":
    P = [[1, 0, 0, 0, 0], [.5, 0, .5, 0, 0], [0, .5, 0, .5, 0], [0, 0, .5, 0, .5], [0, 0, 0, 0, 1]]
    print("Ruin 0..4, E[steps] from 1,2,3:", absorbing_expected_steps(P, [1, 2, 3]))
    for pat in ["HH", "HT", "HHH", "HTH"]:
        print(f"E[flips until {pat}] = {pattern_expected_flips(pat):.4f}  ~ sim {pattern_sim(pat):.3f}")
    print("Re-roll values (1..4 rolls):", [str(reroll_value(n)) for n in range(1, 5)])
    print("Four coins, re-toss all once:", reflip_coins_value(4))
    print("Red card game (26,26):", red_card_value(26, 26))
    print("d6 + d10 guess the sum:", guess_sum_value())
    print("Amoeba extinction:", extinction_probability([.25] * 4), " sqrt(2)-1 =", math.sqrt(2) - 1)
    print("P(biased | 10 heads), prior 1/1000, double-headed:", round(posterior_biased(1e-3, 1.0, 10, 0), 4))
    t, v = bust_stop_game()
    print(f"Bust-on-1 game: stop at {t}, value {v:.4f}  ~ sim {bust_stop_sim(t):.3f}")
    print("P(THH before HHT):", penney_prob("THH", "HHT"))
    print("E[2nd smallest of 5 uniforms]:", round(expected_kth_order_stat(2, 5), 6), "= 2/6")
