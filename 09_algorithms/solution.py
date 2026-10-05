"""
09 - ALGORITHMS - REFERENCE SOLUTION (with the complexity you should state out loud)
"""
import heapq
from collections import Counter, defaultdict, deque


# ======================= PART A =======================
def moving_average(prices, k):
    # O(n) time, O(n) output. Sliding window: add the new element, drop the old one.
    if k <= 0 or k > len(prices):
        return []
    window = sum(prices[:k])
    out = [window / k]
    for i in range(k, len(prices)):
        window += prices[i] - prices[i - k]
        out.append(window / k)
    return out
    # Follow-up "floating-point drift over millions of updates?": recompute the sum from scratch
    # every so often, or use integer ticks / math.fsum. Streaming version: keep a deque of size k.


def max_profit(prices):
    # O(n) time, O(1) memory: track the cheapest price so far.
    best, min_price = 0, float("inf")
    for p in prices:
        min_price = min(min_price, p)
        best = max(best, p - min_price)
    return best


def two_sum(nums, target):
    # O(n) time and memory: for each x, check whether its complement was already seen.
    seen = {}                                   # value -> index
    for j, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], j)
        seen.setdefault(x, j)                   # keep the first index of each value
    return None


# ======================= PART B =======================
def vwap(trades):
    total_qty = sum(q for _, q in trades)
    if total_qty == 0:
        return None
    return sum(p * q for p, q in trades) / total_qty


def max_drawdown(prices):
    # O(n), O(1): running peak.
    peak, worst = float("-inf"), 0.0
    for p in prices:
        peak = max(peak, p)
        worst = max(worst, (peak - p) / peak)
    return worst


def top_k_frequent(items, k):
    # O(n + m log m) with m distinct items. (heapq.nsmallest with the same key -> O(n + m log k))
    counts = Counter(items)
    return sorted(counts, key=lambda x: (-counts[x], x))[:k]


# ======================= PART C =======================
def merge_intervals(intervals):
    # O(n log n) for the sort, then one pass.
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:      # overlaps (or touches) the last one
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def integer_sqrt(n):
    # Find the largest m with m*m <= n. Invariant: lo*lo <= n < (hi+1)*(hi+1)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2                   # round UP to avoid an infinite loop
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def coin_change_ways(amount, coins):
    # ways[a] = number of combinations making amount a, using the coins processed so far.
    # Looping over coins in the OUTER loop counts combinations (not orderings).
    ways = [0] * (amount + 1)
    ways[0] = 1                                    # one way to make 0: take nothing
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]
    # Swap the loops (amount outer, coins inner) and you count ORDERED sequences instead.


def max_subarray_sum(pnl):
    # Kadane: best sum of a subarray ENDING here = max(x, best_ending_previous + x)
    best = cur = pnl[0]
    for x in pnl[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


# ======================= PART D =======================
def running_median(stream):
    low, high, out = [], [], []                    # low: max-heap via negatives
    for x in stream:
        if not low or x <= -low[0]:
            heapq.heappush(low, -x)
        else:
            heapq.heappush(high, x)
        # rebalance so that len(low) == len(high) or len(high) + 1
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        out.append(-low[0] if len(low) > len(high) else (-low[0] + high[0]) / 2)
    return out


class OrderBook:
    def __init__(self):
        self.bids = []          # heap of [-price, seq, qty]  -> highest price first, then oldest
        self.asks = []          # heap of [ price, seq, qty]  -> lowest price first, then oldest
        self.seq = 0            # arrival counter = time priority

    def add(self, side, price, qty):
        fills = []
        if side == "buy":
            book, crosses = self.asks, lambda best: best <= price
        else:
            book, crosses = self.bids, lambda best: best >= price
        while qty > 0 and book:
            top = book[0]
            best_price = top[0] if side == "buy" else -top[0]
            if not crosses(best_price):
                break
            traded = min(qty, top[2])
            fills.append((best_price, traded))
            qty -= traded
            top[2] -= traded                       # mutate in place: heap order is unchanged
            if top[2] == 0:
                heapq.heappop(book)
        if qty > 0:                                # rest the remainder
            key = -price if side == "buy" else price
            heapq.heappush(self.bids if side == "buy" else self.asks, [key, self.seq, qty])
            self.seq += 1
        return fills
        # Complexity: O(log n) per resting order, plus O(log n) per fill.
        # Real books: dict price -> deque of orders + sorted price levels; support cancel by id.

    def best_bid(self):
        return -self.bids[0][0] if self.bids else None

    def best_ask(self):
        return self.asks[0][0] if self.asks else None


if __name__ == "__main__":
    print(moving_average([1, 2, 3, 4, 5], 3))
    print(running_median([5, 15, 1, 3]))
    ob = OrderBook()
    ob.add("sell", 101, 5)
    ob.add("sell", 102, 5)
    print(ob.add("buy", 102, 7), ob.best_bid(), ob.best_ask())
