"""Run:  python check.py   |  python check.py C4   |  python check.py solution
(Don't read below - it contains the answers.)"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from checker import Checks, between, close, equal, is_type  # noqa: E402
import numpy as np  # noqa: E402

checks = Checks(__file__)


# ---------------------------------------------------------------- PART A
@checks.task("A1", "absorbing_expected_steps", "solve (I - Q) t = 1")
def _(f):
    ruin = [[1, 0, 0, 0, 0],
            [.5, 0, .5, 0, 0],
            [0, .5, 0, .5, 0],
            [0, 0, .5, 0, .5],
            [0, 0, 0, 0, 1]]
    out = f(ruin, [1, 2, 3])
    is_type(out, np.ndarray)
    close(out, [3, 4, 3], what="fair walk on 0..4, E[steps] from 1, 2, 3 (should be k(4-k))")
    close(f(np.array([[0.5, 0.5], [0.0, 1.0]]), [0]), [2.0], what="geometric(1/2) wait")
    cube = [[0, 1, 0, 0],                      # distance from the target corner of a cube: 3, 2, 1, 0
            [1 / 3, 0, 2 / 3, 0],
            [0, 2 / 3, 0, 1 / 3],
            [0, 0, 0, 1]]
    close(f(cube, [0, 1, 2]), [10, 9, 7], what="random walk on a cube, steps to the opposite corner")


@checks.task("A2", "pattern_expected_flips", "pattern automaton")
def _(f):
    for pat, ev in [("H", 2), ("HH", 6), ("HT", 4), ("HHH", 14), ("HTH", 10), ("HHT", 8), ("HTHT", 20)]:
        close(f(pat), ev, what=f"E[flips until {pat}], fair coin")
    p = 0.3
    close(f("HH", p), (1 + p) / p ** 2, what="E[flips until HH] with P(H)=0.3")
    close(f("HT", p), 1 / (p * (1 - p)), what="E[flips until HT] with P(H)=0.3")


@checks.task("A3", "pattern_sim", "Monte Carlo of A2")
def _(f):
    between(f("HH", 0.5, n_sims=20_000, seed=1), 5.84, 6.16, "simulated E[flips until HH]")
    between(f("HTH", 0.5, n_sims=20_000, seed=1), 9.74, 10.26, "simulated E[flips until HTH]")
    between(f("HT", 0.3, n_sims=20_000, seed=1), 4.66, 4.87, "simulated E[flips until HT], P(H)=0.3")


# ---------------------------------------------------------------- PART B
@checks.task("B1", "reroll_value", "backward induction")
def _(f):
    close(f(1), 3.5, what="1 roll")
    close(f(2), 17 / 4, what="up to 2 rolls")
    close(f(3), 14 / 3, what="up to 3 rolls")
    close(f(4), 89 / 18, what="up to 4 rolls")
    close(f(2, sides=20), 13.0, what="d20, up to 2 rolls")


@checks.task("B2", "reflip_coins_value", "enumerate + threshold")
def _(f):
    close(f(4), 19 / 8, what="4 coins, may re-toss all once")
    close(f(1), 3 / 4, what="1 coin")
    close(f(2), 5 / 4, what="2 coins")
    close(f(5), 95 / 32, what="5 coins")


@checks.task("B3", "red_card_value", "DP over (red, black)")
def _(f):
    close(f(26, 26), 0.5, what="full deck")
    close(f(3, 1), 0.75, what="3 red, 1 black")
    close(f(1, 4), 0.2, what="1 red, 4 black")
    close(f(5, 0), 1.0, what="only red left")
    close(f(0, 3), 0.0, what="only black left")
    close(f(7, 12), 7 / 19, what="7 red, 12 black")


@checks.task("B4", "guess_sum_value", "maximise s * P(s)")
def _(f):
    out = f()
    is_type(out, tuple)
    equal(out[0], 11, "best guess for d6 + d10")
    close(out[1], 1.1, what="expected payout for d6 + d10")
    g, v = f(6, 6)
    equal(g, 7, "best guess for two d6")
    close(v, 7 / 6, what="expected payout for two d6")
    g, v = f(6, 20)
    equal(g, 21, "best guess for d6 + d20")
    close(v, 21 / 20, what="expected payout for d6 + d20")


# ---------------------------------------------------------------- PART C
@checks.task("C1", "extinction_probability", "smallest root of G(q) = q")
def _(f):
    close(f([0.25, 0.25, 0.25, 0.25]), math.sqrt(2) - 1, tol=1e-9, what="amoeba: die/stay/split 2/split 3")
    close(f([0.2, 0.3, 0.5]), 0.4, tol=1e-9, what="offspring [0.2, 0.3, 0.5]")
    close(f([0, 0, 1]), 0.0, tol=1e-9, what="always 2 children")
    close(f([1.0]), 1.0, tol=1e-9, what="always 0 children")
    close(f([0.5, 0, 0.5]), 1.0, tol=1e-2, what="critical case, mean offspring = 1")


@checks.task("C2", "posterior_biased", "Bayes")
def _(f):
    close(f(0.5, 0.75, 1, 0), 0.6, what="prior 1/2, P(H)=3/4, saw 1 head")
    close(f(0.5, 0.75, 0, 1), 1 / 3, what="prior 1/2, P(H)=3/4, saw 1 tail")
    close(f(1 / 1000, 1.0, 10, 0), 1024 / 2023, what="1 double-headed coin in 1000, 10 heads")
    close(f(1 / 1000, 1.0, 10, 1), 0.0, what="double-headed coin can't show tails")
    lb, lf = 0.6 ** 7 * 0.4 ** 3, 0.5 ** 10
    close(f(0.3, 0.6, 7, 3), 0.3 * lb / (0.3 * lb + 0.7 * lf), what="prior 0.3, P(H)=0.6, 7H 3T")


@checks.task("C3", "prob_next_heads", "predictive probability")
def _(f):
    close(f(0.5, 0.75, 1, 0), 13 / 20, what="prior 1/2, P(H)=3/4, saw 1 head")
    close(f(1 / 1000, 1.0, 10, 0), 3047 / 4046, what="1 double-headed coin in 1000, 10 heads")
    close(f(0.0, 0.9, 5, 0), 0.5, what="prior 0: the coin is fair")


@checks.task("C4", "bust_stop_game", "optimal stopping DP")
def _(f):
    out = f()
    is_type(out, tuple)
    equal(out[0], 20, "threshold, d6 with bust on 1")
    close(out[1], 8.141794893727031, what="value, d6 with bust on 1")
    t, v = f(6, 6)
    equal(t, 15, "threshold, d6 with bust on 6")
    close(v, 6.1537379284031894, what="value, d6 with bust on 6")
    t, v = f(4, 1)
    equal(t, 9, "threshold, d4 with bust on 1")
    close(v, 3.8564453125, what="value, d4 with bust on 1")


@checks.task("C5", "bust_stop_sim", "simulate a threshold rule")
def _(f):
    between(f(20, n_sims=50_000, seed=1), 7.91, 8.37, "simulated value, stop at 20")
    between(f(10, n_sims=50_000, seed=1), 6.74, 7.00, "simulated value, stop at 10")
    between(f(15, 6, 6, n_sims=50_000, seed=1), 5.98, 6.33, "simulated value, bust on 6, stop at 15")
    close(f(0, n_sims=1_000, seed=1), 0.0, what="threshold 0 means never roll")


# ---------------------------------------------------------------- PART D
@checks.task("D1", "penney_prob", "pattern a before pattern b")
def _(f):
    close(f("HH", "TH"), 1 / 4, what="P(HH before TH)")
    close(f("THH", "HHT"), 3 / 4, what="P(THH before HHT)")
    close(f("HTH", "HHT"), 1 / 3, what="P(HTH before HHT)")
    close(f("TTH", "HHH"), 0.7, what="P(TTH before HHH)")
    close(f("HHT", "HTT"), 2 / 3, what="P(HHT before HTT)")
    close(f("HH", "HT"), 1 / 2, what="P(HH before HT)")
    close(f("THTH", "HTHH"), 9 / 14, what="P(THTH before HTHH)")


@checks.task("D2", "expected_kth_order_stat", "tail-integral formula")
def _(f):
    close(f(2, 5), 1 / 3, what="E[2nd smallest of 5 uniforms]")
    close(f(5, 5), 5 / 6, what="E[max of 5 uniforms]")
    close(f(1, 10), 1 / 11, what="E[min of 10 uniforms]")
    close(f(1, 1), 1 / 2, what="E[one uniform]")
    close(f(3, 7), 3 / 8, what="E[3rd smallest of 7 uniforms]")


if __name__ == "__main__":
    checks.run()
