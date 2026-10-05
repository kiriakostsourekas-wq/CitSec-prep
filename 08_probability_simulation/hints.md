# Hints · 08 Probability

### A1 `dice_sum_exact`
<details><summary>Hint 1</summary>`outcomes = list(itertools.product(range(1, 7), repeat=n_dice))` is a list of tuples like (3, 5).</details>
<details><summary>Hint 2</summary>Count the tuples whose `sum(o) == target`, then divide by `len(outcomes)`.</details>

### A2 `dice_sum_sim`
<details><summary>Hint 1</summary>`rolls = rng.integers(1, 7, size=(n_sims, n_dice))`; `rolls.sum(axis=1)` gives one sum per simulation.</details>
<details><summary>Hint 2</summary>`np.mean(rolls.sum(axis=1) == target)`</details>

### A3 `expected_flips_sim`
<details><summary>Hint 1</summary>Inside each simulation, build a string of flips and stop when it ends with the pattern: `seq[-len(pattern):] == pattern`.</details>
<details><summary>Hint 2</summary>

```python
seq = ""
while seq[-k:] != pattern:
    seq += "H" if rng.random() < 0.5 else "T"
total += len(seq)
```
(With an empty `seq`, `seq[-2:]` is `""`, so the loop starts correctly.)
</details>

### B1 `birthday_exact`
<details><summary>Hint 1</summary>Compute P(all different) as a running product over i = 0..n−1 of (365 − i)/365. Then the answer is 1 minus that.</details>

### B2 `birthday_sim`
<details><summary>Hint 1</summary>`days = rng.integers(0, 365, size=(n_sims, n))`; sort each row with `np.sort(days, axis=1)`.</details>
<details><summary>Hint 2</summary>After sorting, a repeat means two neighbours are equal: `(np.diff(days, axis=1) == 0).any(axis=1)`. Then take the mean of that.</details>

### B3 `estimate_pi`
<details><summary>Hint 1</summary>`x, y = rng.random(n), rng.random(n)`; inside = `x**2 + y**2 <= 1`; `4 * np.mean(inside)`.</details>

### C1 `gamblers_ruin_exact`
<details><summary>Hint 1</summary>Just the formula from the docstring with an `if p == 0.5:` branch.</details>

### C2 `gamblers_ruin_sim`
<details><summary>Hint 1</summary>For each simulation: `x = start`, then `while 0 < x < target:` step +1 with probability p, else −1.</details>
<details><summary>Hint 2</summary>Count how many simulations end with `x == target`; divide by `n_sims`.</details>

### D1 `bootstrap_ci`
<details><summary>Hint 1</summary>`samples = rng.choice(data, size=(n_boot, len(data)), replace=True)`; one mean per row: `samples.mean(axis=1)`.</details>
<details><summary>Hint 2</summary>`lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])`</details>

### D2 `coupon_collector_exact`
<details><summary>Hint 1</summary>`n * sum(1 / k for k in range(1, n + 1))`</details>

### D3 `coupon_collector_sim`
<details><summary>Hint 1</summary>Use a `set()`: keep drawing `int(rng.integers(n))` and adding it to the set until `len(seen) == n`, counting the draws.</details>
