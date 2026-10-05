"""
09 - CODING-INTERVIEW ALGORITHMS (finance flavoured)  (about 1.5-2 hours)
==========================================================================
Pure Python (no numpy). These are the kind of short coding questions reported
for Citadel phone screens / superdays: "implement a moving average for a
Python list", easy-to-medium LeetCode, a little dynamic programming.

For EVERY problem, before coding, say out loud (as in the interview):
  1. the brute-force idea and its complexity
  2. the better idea and its complexity
  3. edge cases (empty list, k > n, all equal values, negative numbers...)

Difficulty:  A = easy,  B = easy/medium,  C = medium,  D = medium/hard (bonus)
Run `python check.py` to test, `python exercise.py` for the playground.
"""
import heapq
from collections import Counter, defaultdict, deque


# ======================================================================
# PART A - EASY
# ======================================================================
def moving_average(prices, k):
    """Simple moving average with window k. Return a list of length len(prices) - k + 1
    where element i is the mean of prices[i : i+k]. If k > len(prices) return [].
    Target: O(n) time - do NOT re-sum every window (that is O(n*k)).

    >>> moving_average([1, 2, 3, 4, 5], 3)
    [2.0, 3.0, 4.0]
    """
    raise NotImplementedError


def max_profit(prices):
    """You may buy once and sell once later. Return the maximum profit (0 if you can't profit).
    Target: one pass, O(n) time, O(1) memory.

    >>> max_profit([7, 1, 5, 3, 6, 4])
    5
    """
    raise NotImplementedError


def two_sum(nums, target):
    """Return a tuple (i, j) with i < j and nums[i] + nums[j] == target, or None.
    If several pairs exist, return the one with the smallest j.
    Target: O(n) with a dict (value -> index seen so far).

    >>> two_sum([2, 7, 11, 15], 9)
    (0, 1)
    """
    raise NotImplementedError


# ======================================================================
# PART B - EASY / MEDIUM
# ======================================================================
def vwap(trades):
    """Volume-weighted average price of a list of (price, qty) tuples:
    sum(price*qty) / sum(qty). Return None for an empty list.

    >>> vwap([(100.0, 10), (101.0, 30)])
    100.75
    """
    raise NotImplementedError


def max_drawdown(prices):
    """Largest peak-to-trough fall as a POSITIVE fraction, in one pass:
    max over t of (running_peak - price_t) / running_peak. 0.0 if prices only go up.

    >>> max_drawdown([100, 120, 90, 130, 117])
    0.25
    """
    raise NotImplementedError


def top_k_frequent(items, k):
    """Return the k most frequent items, most frequent first.
    Ties: the smaller item (normal sort order) comes first.

    >>> top_k_frequent(["AAA", "BBB", "AAA", "CCC", "BBB", "AAA"], 2)
    ['AAA', 'BBB']
    """
    raise NotImplementedError


# ======================================================================
# PART C - MEDIUM
# ======================================================================
def merge_intervals(intervals):
    """Merge overlapping [start, end] intervals (touching ones like [1,3],[3,5] merge too).
    Return the merged list sorted by start.  (Think: trading sessions, order lifetimes...)

    >>> merge_intervals([[1, 3], [8, 10], [2, 6], [15, 18]])
    [[1, 6], [8, 10], [15, 18]]
    """
    raise NotImplementedError


def integer_sqrt(n):
    """floor(sqrt(n)) for an integer n >= 0 WITHOUT math.sqrt / ** 0.5, using binary search.
    O(log n).

    >>> integer_sqrt(17)
    4
    """
    raise NotImplementedError


def coin_change_ways(amount, coins):
    """Number of different COMBINATIONS (order doesn't matter) of coins that sum to amount,
    with unlimited coins of each type. Classic dynamic programming, O(amount * len(coins)).

    >>> coin_change_ways(5, [1, 2, 5])
    4
    """
    raise NotImplementedError


def max_subarray_sum(pnl):
    """Best total P&L over a CONTIGUOUS period of days (at least one day).
    Kadane's algorithm, O(n).

    >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    """
    raise NotImplementedError


# ======================================================================
# PART D - MEDIUM / HARD (bonus)
# ======================================================================
def running_median(stream):
    """After each new number, report the median of all numbers seen so far.
    Target: O(log n) per number using TWO HEAPS
      - `low`: a max-heap of the smaller half (store negatives, since heapq is a min-heap)
      - `high`: a min-heap of the larger half
    keep len(low) == len(high) or len(low) == len(high) + 1.

    >>> running_median([5, 15, 1, 3])
    [5, 10.0, 5, 4.0]
    """
    raise NotImplementedError


class OrderBook:
    """A minimal limit order book for ONE stock (the classic market-maker exercise).

    add(side, price, qty) -> list of fills [(price, qty), ...]
      side is "buy" or "sell".
      An incoming BUY matches resting SELLS with price <= its limit, best (lowest) price first;
      an incoming SELL matches resting BUYS with price >= its limit, best (highest) price first.
      At the same price, older orders fill first (FIFO).
      Fills happen at the RESTING order's price. Any unfilled quantity rests in the book.
    best_bid() -> highest resting buy price, or None
    best_ask() -> lowest resting sell price, or None

    ob = OrderBook()
    ob.add("sell", 101, 5); ob.add("sell", 102, 5)
    ob.add("buy", 102, 7)       # -> [(101, 5), (102, 2)]
    ob.best_ask()               # -> 102 (3 left)
    ob.best_bid()               # -> None (the buy was fully filled)

    Suggested structure: two heaps of [price_key, sequence_number, qty]
    (price_key = -price for bids so the highest bid pops first).
    """

    def __init__(self):
        raise NotImplementedError

    def add(self, side, price, qty):
        raise NotImplementedError

    def best_bid(self):
        raise NotImplementedError

    def best_ask(self):
        raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Try your functions by hand here once you've written them, e.g.:
    # print(moving_average([1, 2, 3, 4, 5], 3))
    # print(max_profit([7, 1, 5, 3, 6, 4]))
    print("Playground: uncomment the lines above (or add your own) to try your functions.")
