# Hints · 09 Algorithms

### A1 `moving_average`
<details><summary>Hint 1</summary>Compute the first window's sum once: `window = sum(prices[:k])`.</details>
<details><summary>Hint 2</summary>When the window slides right by one: add `prices[i]` and subtract `prices[i - k]`.</details>
<details><summary>Hint 3</summary>

```python
out = [window / k]
for i in range(k, len(prices)):
    window += prices[i] - prices[i - k]
    out.append(window / k)
```
</details>

### A2 `max_profit`
<details><summary>Hint 1</summary>For each day, the best sale today = today's price − the minimum price seen before today.</details>
<details><summary>Hint 2</summary>Keep two variables: `min_price` (start `float("inf")`) and `best` (start 0). Update both in one loop.</details>

### A3 `two_sum`
<details><summary>Hint 1</summary>For element x at index j, you need `target - x`. Was it already seen? A dict `value -> index` answers that in O(1).</details>
<details><summary>Hint 2</summary>Check **before** inserting x itself, so you don't pair an element with itself. Use `seen.setdefault(x, j)` to keep the first index.</details>

### B1 `vwap`
<details><summary>Hint 1</summary>Two sums: `sum(p * q for p, q in trades)` and `sum(q for _, q in trades)`. Guard against a total of 0.</details>

### B2 `max_drawdown`
<details><summary>Hint 1</summary>Track `peak = max(peak, p)` as you go. The drawdown now is `(peak - p) / peak`; keep the largest one.</details>

### B3 `top_k_frequent`
<details><summary>Hint 1</summary>`counts = Counter(items)`.</details>
<details><summary>Hint 2</summary>Sort the distinct items with a TUPLE key: `key=lambda x: (-counts[x], x)`. The minus sign makes high counts come first, and `x` breaks ties.</details>

### C1 `merge_intervals`
<details><summary>Hint 1</summary>Sort by start. Then an interval either overlaps the LAST merged interval or starts a new one.</details>
<details><summary>Hint 2</summary>Overlap test: `start <= merged[-1][1]`. If it overlaps: `merged[-1][1] = max(merged[-1][1], end)`.</details>

### C2 `integer_sqrt`
<details><summary>Hint 1</summary>You are looking for the largest m with m*m <= n. The answer is between 0 and n.</details>
<details><summary>Hint 2</summary>Binary search with `lo, hi = 0, n`. If `mid*mid <= n`, then mid is feasible (`lo = mid`), otherwise `hi = mid - 1`.</details>
<details><summary>Hint 3</summary>Use `mid = (lo + hi + 1) // 2` (rounding up). With rounding down, `lo = mid` can loop forever when `hi = lo + 1`.</details>

### C3 `coin_change_ways`
<details><summary>Hint 1</summary>`ways[a]` = number of ways to make amount a. `ways[0] = 1`.</details>
<details><summary>Hint 2</summary>For each coin c (outer loop), for each amount a from c to amount (inner loop): `ways[a] += ways[a - c]`.</details>

### C4 `max_subarray_sum`
<details><summary>Hint 1</summary>Let `cur` = best sum of a subarray that ENDS at the current element. Either extend the previous one or start fresh: `cur = max(x, cur + x)`.</details>
<details><summary>Hint 2</summary>Initialize `best = cur = pnl[0]` (not 0! think about all-negative inputs).</details>

### D1 `running_median`
<details><summary>Hint 1</summary>`heapq` only does min-heaps. For a max-heap, push `-x` and negate when reading: the max of `low` is `-low[0]`.</details>
<details><summary>Hint 2</summary>Insert: if `low` is empty or `x <= -low[0]`, push to low, else push to high. Then rebalance: if `len(low) > len(high) + 1`, move the top of low to high; if `len(high) > len(low)`, move the top of high to low.</details>
<details><summary>Hint 3</summary>Median: if `len(low) > len(high)` it is `-low[0]`, otherwise `(-low[0] + high[0]) / 2`.</details>

### D2 `OrderBook`
<details><summary>Hint 1</summary>`self.bids` and `self.asks` are lists used as heaps; `self.seq = 0` is a counter so older orders win ties.
Store entries as lists `[key, seq, qty]` (lists, so you can change qty in place). For bids `key = -price`.</details>
<details><summary>Hint 2</summary>An incoming buy looks at `self.asks[0]`: while qty remains and the ask price ≤ limit, trade `min(qty, resting_qty)`, record `(ask_price, traded)`,
reduce both, and `heappop` the resting order if it reaches 0.</details>
<details><summary>Hint 3</summary>After matching, if `qty > 0`, push `[key, self.seq, qty]` onto your own side and increment `self.seq`. The sell case is the mirror image (compare with `-bids[0][0]`).</details>
