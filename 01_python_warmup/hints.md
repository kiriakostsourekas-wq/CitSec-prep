# Hints · 01 Python warm-up
Open **one hint at a time**. Try again after each one.

### A1 `sum_of_squares`
<details><summary>Hint 1</summary>Start a running total at 0, loop over the numbers, add x*x each time.</details>
<details><summary>Hint 2</summary>The one-liner: `sum(...)` accepts a generator expression like `(x * x for x in nums)`.</details>

### A2 `evens_squared`
<details><summary>Hint 1</summary>Even means `x % 2 == 0`.</details>
<details><summary>Hint 2</summary>Comprehension pattern: `[EXPRESSION for x in nums if CONDITION]`.</details>

### A3 `count_words`
<details><summary>Hint 1</summary>`text.split()` gives a list of words. Clean each one with `.lower()` and `.strip(".,!?")`.</details>
<details><summary>Hint 2</summary>`counts[word] = counts.get(word, 0) + 1` adds one, starting from 0 if the word is new.</details>
<details><summary>Hint 3</summary>

```python
counts = {}
for raw in text.split():
    w = raw.lower().strip(".,!?")
    if w:
        counts[w] = counts.get(w, 0) + 1
return counts
```
</details>

### B1–B2 `mean`, `variance`
<details><summary>Hint 1</summary>mean = sum / length. Variance = average of (x − mean)².</details>
<details><summary>Hint 2</summary>Compute the sum of squared deviations once, then divide by `n` or `n - 1` depending on `sample`.
A conditional expression is handy: `d = n - 1 if sample else n`.</details>

### B3 `median`
<details><summary>Hint 1</summary>Use `sorted(xs)`, which returns a new list. `xs.sort()` would modify the caller's list, which the checker forbids.</details>
<details><summary>Hint 2</summary>With `n = len(s)` and `mid = n // 2`: odd n → `s[mid]`; even n → `(s[mid-1] + s[mid]) / 2`.</details>

### C1 `total_quantity_by_ticker`
<details><summary>Hint 1</summary>Same pattern as count_words, but add `t["qty"]` instead of 1.</details>
<details><summary>Hint 2</summary>`from collections import defaultdict` then `totals = defaultdict(int)`; at the end `return dict(totals)`.</details>

### C2 `sort_trades_by_value`
<details><summary>Hint 1</summary>`sorted(iterable, key=some_function, reverse=True)`.</details>
<details><summary>Hint 2</summary>`key=lambda t: t["price"] * t["qty"]`.</details>

### C3 `is_palindrome`
<details><summary>Hint 1</summary>First build the cleaned sequence: keep only characters where `ch.isalnum()` is True, lower-cased.</details>
<details><summary>Hint 2</summary>Compare it with its reverse: `cleaned == cleaned[::-1]`.</details>

### D1 `Portfolio`
<details><summary>Hint 1</summary>In `__init__` store `self.cash = cash` and an empty dict `self.holdings = {}` (ticker → qty).</details>
<details><summary>Hint 2</summary>`position` = `self.holdings.get(ticker, 0)`. In `buy`, compute `cost = qty*price` and
`raise ValueError(...)` if `cost > self.cash` **before** changing anything.</details>
<details><summary>Hint 3</summary>`value(prices)` = cash + Σ qty × prices[ticker] over your holdings.
`for ticker, qty in self.holdings.items(): ...`</details>

### D2 `read_closes`
<details><summary>Hint 1</summary>

```python
with open(path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:      # row is a dict: {"date": ..., "ticker": ..., "close": "98.46", ...}
        ...
```
</details>
<details><summary>Hint 2</summary>Everything from csv is a **string**, so convert with `float(row["close"])`. Use a `defaultdict(list)` and `.append`.</details>
