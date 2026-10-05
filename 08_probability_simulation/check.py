"""Run:  python check.py   |  python check.py C2   |  python check.py solution
(Don't read below - it contains the answers.)"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from checker import Checks, between, close  # noqa: E402
import numpy as np  # noqa: E402

checks = Checks(__file__)


@checks.task("A1", "dice_sum_exact", "enumeration")
def _(f):
    close(f(7), 6 / 36, what="P(sum of 2 dice = 7)")
    close(f(2), 1 / 36, what="P(sum of 2 dice = 2)")
    close(f(10, n_dice=3), 27 / 216, what="P(sum of 3 dice = 10)")
    close(f(13), 0.0, what="P(sum of 2 dice = 13)")


@checks.task("A2", "dice_sum_sim", "vectorized Monte Carlo")
def _(f):
    between(f(7), 0.160, 0.173, "simulated P(sum = 7)")
    between(f(10, n_dice=3), 0.118, 0.132, "simulated P(3 dice sum = 10)")


@checks.task("A3", "expected_flips_sim", "simulate until pattern")
def _(f):
    between(f("HH"), 5.85, 6.15, "E[flips until HH]")
    between(f("HT"), 3.9, 4.1, "E[flips until HT]")


@checks.task("B1", "birthday_exact", "complement trick")
def _(f):
    close(f(23), 0.507297234, what="birthday n=23")
    close(f(1), 0.0, what="birthday n=1")
    close(f(366), 1.0, what="birthday n=366")


@checks.task("B2", "birthday_sim", "detect repeats")
def _(f):
    between(f(23), 0.495, 0.52, "simulated birthday n=23")
    between(f(50), 0.96, 0.975, "simulated birthday n=50")


@checks.task("B3", "estimate_pi", "points in a circle")
def _(f):
    between(f(), 3.13, 3.153, "pi estimate")


@checks.task("C1", "gamblers_ruin_exact", "closed form")
def _(f):
    close(f(3, 10), 0.3, what="fair game 3 -> 10")
    r = 0.55 / 0.45
    close(f(3, 10, 0.45), (1 - r ** 3) / (1 - r ** 10), what="p=0.45, 3 -> 10")


@checks.task("C2", "gamblers_ruin_sim", "simulate the walk")
def _(f):
    between(f(3, 10), 0.285, 0.315, "simulated fair game 3 -> 10")
    between(f(3, 10, 0.45), 0.115, 0.141, "simulated p=0.45, 3 -> 10")


@checks.task("D1", "bootstrap_ci", "resampling")
def _(f):
    data = np.random.default_rng(1).exponential(2.0, 50)
    lo, hi = f(data)
    m, se = data.mean(), data.std(ddof=1) / math.sqrt(50)
    if not lo < m < hi:
        raise AssertionError(f"the CI ({lo:.3f}, {hi:.3f}) should contain the sample mean {m:.3f}")
    between(hi - lo, 3.0 * se, 4.8 * se, "CI width (should be about 2 * 1.96 * standard error)")


@checks.task("D2", "coupon_collector_exact", "sum of geometrics")
def _(f):
    close(f(6), 14.7, what="coupon collector n=6")
    close(f(1), 1.0, what="coupon collector n=1")


@checks.task("D3", "coupon_collector_sim", "simulate")
def _(f):
    between(f(6), 14.3, 15.1, "simulated coupon collector n=6")


if __name__ == "__main__":
    checks.run()
