"""Run:  python check.py   |  python check.py C3   |  python check.py solution
(Don't read below - it contains the answers.)"""
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from checker import Checks, close, equal  # noqa: E402

checks = Checks(__file__)


@checks.task("A1", "moving_average", "sliding window O(n)")
def _(f):
    close(f([1, 2, 3, 4, 5], 3), [2.0, 3.0, 4.0], what="moving_average([1..5], 3)")
    close(f([4.0, 8.0], 1), [4.0, 8.0], what="window 1")
    equal(f([1, 2], 3), [], "k > len(prices)")
    big = list(range(200_000))
    t0 = time.perf_counter()
    out = f(big, 5_000)
    if time.perf_counter() - t0 > 1.0:
        raise AssertionError("too slow for n=200k, k=5k: are you re-summing each window (O(n*k))?")
    close(out[0], 2499.5, what="first window of the big test")


@checks.task("A2", "max_profit", "track the minimum")
def _(f):
    equal(f([7, 1, 5, 3, 6, 4]), 5, "max_profit example")
    equal(f([7, 6, 4, 3, 1]), 0, "falling prices")
    equal(f([]), 0, "empty list")
    equal(f([2, 4, 1, 3]), 2, "[2,4,1,3]")


@checks.task("A3", "two_sum", "hash map")
def _(f):
    equal(f([2, 7, 11, 15], 9), (0, 1), "example")
    equal(f([3, 2, 4], 6), (1, 2), "[3,2,4] target 6 (don't use the same element twice)")
    equal(f([3, 3], 6), (0, 1), "[3,3]")
    equal(f([1, 2, 3], 100), None, "no solution")


@checks.task("B1", "vwap", "weighted average")
def _(f):
    close(f([(100.0, 10), (101.0, 30)]), 100.75, what="vwap")
    equal(f([]), None, "vwap of no trades")


@checks.task("B2", "max_drawdown", "running peak")
def _(f):
    close(f([100, 120, 90, 130, 117]), 0.25, what="max_drawdown")
    close(f([1, 2, 3]), 0.0, what="rising prices")
    close(f([50, 40, 30, 60, 20]), 2 / 3, what="[50,40,30,60,20]")


@checks.task("B3", "top_k_frequent", "Counter + sort key")
def _(f):
    equal(f(["AAA", "BBB", "AAA", "CCC", "BBB", "AAA"], 2), ["AAA", "BBB"], "top 2")
    equal(f(["b", "a", "c", "c"], 3), ["c", "a", "b"], "tie-break alphabetical")


@checks.task("C1", "merge_intervals", "sort then sweep")
def _(f):
    equal(f([[1, 3], [8, 10], [2, 6], [15, 18]]), [[1, 6], [8, 10], [15, 18]], "example")
    equal(f([[1, 4], [4, 5]]), [[1, 5]], "touching intervals")
    equal(f([[1, 10], [2, 3]]), [[1, 10]], "contained interval")
    equal(f([]), [], "empty")


@checks.task("C2", "integer_sqrt", "binary search")
def _(f):
    for n, r in [(0, 0), (1, 1), (8, 2), (9, 3), (17, 4), (10**12, 10**6), (10**12 - 1, 10**6 - 1)]:
        equal(f(n), r, f"integer_sqrt({n})")


@checks.task("C3", "coin_change_ways", "dynamic programming")
def _(f):
    equal(f(5, [1, 2, 5]), 4, "amount 5, coins [1,2,5]")
    equal(f(3, [2]), 0, "amount 3, coins [2]")
    equal(f(0, [7]), 1, "amount 0")
    equal(f(100, [1, 5, 10, 25, 50]), 292, "100 cents in US coins")


@checks.task("C4", "max_subarray_sum", "Kadane")
def _(f):
    equal(f([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6, "example")
    equal(f([-3, -1, -2]), -1, "all negative")
    equal(f([5]), 5, "single element")


@checks.task("D1", "running_median", "two heaps")
def _(f):
    close(f([5, 15, 1, 3]), [5, 10, 5, 4], what="running median")
    rng = random.Random(0)
    data = [rng.randint(0, 1000) for _ in range(300)]
    exp = [statistics.median(data[: i + 1]) for i in range(len(data))]
    close(f(data), exp, what="running median of 300 random numbers")


@checks.task("D2", "OrderBook", "matching engine")
def _(OrderBook):
    ob = OrderBook()
    equal(ob.add("sell", 101, 5), [], "fills of first resting sell")
    equal(ob.add("sell", 102, 5), [], "fills of second resting sell")
    equal(ob.add("buy", 100, 4), [], "a buy below the ask rests")
    equal((ob.best_bid(), ob.best_ask()), (100, 101), "(best_bid, best_ask)")
    equal(ob.add("buy", 102, 7), [(101, 5), (102, 2)], "fills of a crossing buy")
    equal((ob.best_bid(), ob.best_ask()), (100, 102), "(best_bid, best_ask) after the sweep")
    ob.add("buy", 100, 6)
    equal(ob.add("sell", 99, 12), [(100, 4), (100, 6)], "sell hits bids FIFO at 100")
    equal((ob.best_bid(), ob.best_ask()), (None, 99), "remaining 2 rest as the new best ask")


if __name__ == "__main__":
    checks.run()
