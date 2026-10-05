# 09 · Coding-interview algorithms, finance flavoured (≈ 1.5–2 hours)

**Goal:** the short "can you code?" questions. A candidate reported being asked at Citadel to
*"implement a function to calculate moving average for a Python list"*; others report LeetCode-medium problems, sometimes with DP.
All pure Python, no numpy.

## How to behave in a live coding round (this matters as much as the code)
1. **Restate the problem** and ask about edge cases ("can the list be empty? integers or floats? is k ≤ n?").
2. **Say the brute force** and its complexity first ("O(n·k) by summing each window").
3. **Improve** ("but consecutive windows share k−1 elements, so I can slide: O(n)").
4. **Code cleanly**, talking as you go. Good names, no clever one-liners you can't explain.
5. **Test by hand** on a tiny example, then edge cases.
6. **State the final complexity** (time and memory) without being asked.

## Complexity cheat table
| Operation | Cost |
|---|---|
| list index / append / pop() | O(1) |
| list insert(0, x) / pop(0) / `x in list` | O(n), so use `collections.deque` for queues |
| dict / set lookup, insert | O(1) average |
| `sorted()` | O(n log n) |
| `heapq.heappush` / `heappop` | O(log n); `heap[0]` is the min in O(1) |
| binary search (`bisect`) | O(log n) on a sorted list |

## Tasks
| ID | Function | Idea | Target |
|---|---|---|---|
| A1 | `moving_average` | sliding window | O(n) |
| A2 | `max_profit` | running minimum | O(n), O(1) |
| A3 | `two_sum` | dict of seen values | O(n) |
| B1 | `vwap` | weighted mean | O(n) |
| B2 | `max_drawdown` | running peak | O(n), O(1) |
| B3 | `top_k_frequent` | Counter + sort key | O(n + m log m) |
| C1 | `merge_intervals` | sort, then sweep | O(n log n) |
| C2 | `integer_sqrt` | binary search on the answer | O(log n) |
| C3 | `coin_change_ways` | DP over amounts | O(amount · coins) |
| C4 | `max_subarray_sum` | Kadane | O(n) |
| D1 | `running_median` | two heaps | O(log n) per item |
| D2 | `OrderBook` | heaps + FIFO matching | O(log n) per order |

## Interviewer follow-ups

<details><summary>1. moving_average: the data arrives as a live stream. Change your design.</summary>

Keep a `deque(maxlen=k)` and a running sum. On each new price: if the deque is full, subtract the element that will fall out, then append the new one and add it.
That's O(1) per update and O(k) memory. For an *exponential* moving average you don't even need the window: ema = α·x + (1−α)·ema.
</details>

<details><summary>2. max_profit: now you can do unlimited transactions (but hold at most one share).</summary>

Sum every positive day-to-day increase: Σ max(0, p[i] − p[i−1]). With a fee per trade or at most k trades it becomes a DP with states (day, holding?, trades used).
</details>

<details><summary>3. two_sum: the list is sorted. Can you use O(1) extra memory?</summary>

Two pointers: i at the start and j at the end. If the sum is too small, i += 1; if it's too big, j −= 1. O(n) time, O(1) memory.
</details>

<details><summary>4. coin_change_ways: why does swapping the two loops change the answer?</summary>

Coins outer: each combination is built in a fixed coin order, so {1,2,2} is counted once. Amount outer: every ordering (1,2,2), (2,1,2), (2,2,1)
is counted separately, which gives compositions/permutations. Related question: "minimum number of coins" uses `dp[a] = min(dp[a], dp[a−c] + 1)`.
</details>

<details><summary>5. running_median: why two heaps and not a sorted list?</summary>

Inserting into a sorted Python list is O(n) (elements shift), even with `bisect` to find the position. Heaps give O(log n) insert and O(1) access to the two middle elements.
</details>

<details><summary>6. OrderBook: what features would a real exchange need?</summary>

Order IDs and **cancel/modify** (needs a dict id → order, often with "lazy deletion" in heaps), market orders, price levels stored as dict price → deque (O(1) at a level),
partial fills reporting both sides, timestamps, and, for low latency, avoiding Python entirely (C++, preallocated arrays indexed by price tick).
</details>
