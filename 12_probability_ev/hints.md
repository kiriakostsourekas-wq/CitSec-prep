# Hints · 12 Probability & expected value

### A1 `absorbing_expected_steps`
<details><summary>Hint 1</summary>Convert first: `P = np.asarray(P, dtype=float)`. The transient block is `Q = P[np.ix_(transient, transient)]`, a k×k matrix.</details>
<details><summary>Hint 2</summary>The equations t_i = 1 + Σ_j Q_ij t_j are (I − Q) t = 1, so `np.linalg.solve(np.eye(k) - Q, np.ones(k))`.</details>
<details><summary>Hint 3</summary>Why is I − Q invertible? Every transient state can eventually reach an absorbing one, so Qⁿ → 0 and (I − Q)⁻¹ = I + Q + Q² + … converges. Its (i, j) entry is the expected number of visits to j starting from i.</details>

### A2 `pattern_expected_flips`
<details><summary>Hint 1</summary>Write a helper `next_state(j, c)`: let `s = pattern[:j] + c`; try k = min(len(s), m) down to 0 and return the first k with `s.endswith(pattern[:k])`. (Note `s.endswith("")` is True, so it always returns.)</details>
<details><summary>Hint 2</summary>

```python
P = np.zeros((m + 1, m + 1))
for j in range(m):
    P[j, next_state(j, "H")] += p        # += because both letters can lead to the same state
    P[j, next_state(j, "T")] += 1 - p
P[m, m] = 1.0
```
</details>
<details><summary>Hint 3</summary>`absorbing_expected_steps(P, list(range(m)))[0]` is the answer from the start state 0. Return it as a float.</details>

### A3 `pattern_sim`
<details><summary>Hint 1</summary>Same loop as in folder 08: `seq = ""`, then `while seq[-k:] != pattern: seq += "H" if rng.random() < p else "T"`.</details>
<details><summary>Hint 2</summary>Add `len(seq)` to a running total each simulation and return `total / n_sims`.</details>

### B1 `reroll_value`
<details><summary>Hint 1</summary>Start with `v = Fraction(sides + 1, 2)`, the value with exactly one roll left.</details>
<details><summary>Hint 2</summary>Repeat `n_rolls - 1` times: `v = sum(max(Fraction(x), v) for x in range(1, sides + 1)) / sides`.</details>
<details><summary>Hint 3</summary>Say the strategy out loud: "with 2 rolls left I keep anything ≥ 4.25, i.e. 5 or 6; with 1 roll left I keep anything ≥ 3.5, i.e. 4, 5, 6".</details>

### B2 `reflip_coins_value`
<details><summary>Hint 1</summary>P(k heads) = `Fraction(math.comb(n, k), 2 ** n)`. Re-tossing is worth n/2 on average.</details>
<details><summary>Hint 2</summary>Value = Σ_k P(k) · max(k, n/2). You re-toss exactly when k < n/2.</details>

### B3 `red_card_value`
<details><summary>Hint 1</summary>Define `@lru_cache(maxsize=None) def V(r, b):` inside the function and return `V(r, b)`. Base cases first: r == 0 → 0, b == 0 → 1.</details>
<details><summary>Hint 2</summary>If r + b == 1 you must say it now: return r/(r+b). Otherwise return `max(stop_now, wait)` with `wait = r/n * V(r-1, b) + b/n * V(r, b-1)`. Use `Fraction(r, n)` to keep it exact.</details>
<details><summary>Hint 3</summary>Print V for a few (r, b). It is always r/(r+b): waiting is never better or worse than calling now. That is the optional stopping theorem in action (README).</details>

### B4 `guess_sum_value`
<details><summary>Hint 1</summary>Count how many (a, b) pairs give each sum with two nested loops and a dict.</details>
<details><summary>Hint 2</summary>Loop over the sums in increasing order; value = `Fraction(s * count[s], s1 * s2)`. Replace the best only on a STRICT improvement, so ties keep the smaller guess.</details>

### C1 `extinction_probability`
<details><summary>Hint 1</summary>`G = lambda q: sum(pk * q ** k for k, pk in enumerate(offspring_probs))`.</details>
<details><summary>Hint 2</summary>Start at `q = 0.0` and repeat `q = G(q)`; stop when the change is below ~1e-15 or after n_iter steps. Starting at 0 (not 1!) is what makes you converge to the SMALLEST root.</details>
<details><summary>Hint 3</summary>Check on paper for the amoeba: q = (1 + q + q² + q³)/4 factors as (q − 1)(q² + 2q − 1) = 0.</details>

### C2 `posterior_biased`
<details><summary>Hint 1</summary>Likelihoods: `L_b = p_biased**heads * (1 - p_biased)**tails`, `L_f = 0.5**(heads + tails)`. The binomial coefficient cancels, so the order of the flips doesn't matter.</details>
<details><summary>Hint 2</summary>`prior * L_b / (prior * L_b + (1 - prior) * L_f)`.</details>

### C3 `prob_next_heads`
<details><summary>Hint 1</summary>`post = posterior_biased(...)`; answer = `post * p_biased + (1 - post) * 0.5`.</details>

### C4 `bust_stop_game`
<details><summary>Hint 1</summary>`good = [f for f in range(1, sides + 1) if f != bust]`. Fill a dict `V` for s = cap, cap−1, …, 0. If `s + max(good) > cap`, set `V[s] = s` (you would stop there anyway).</details>
<details><summary>Hint 2</summary>Otherwise `cont = sum(V[s + f] for f in good) / sides` (the bust face contributes 0) and `V[s] = max(s, cont)`. Whenever `s >= cont`, record `threshold = s`; since you go downwards, the last one recorded is the smallest.</details>
<details><summary>Hint 3</summary>Paper check: one more roll changes your expected total by −s/6 + (2+3+4+5+6)/6 = (20 − s)/6, so you should stop at 20. Return `(threshold, float(V[0]))`.</details>

### C5 `bust_stop_sim`
<details><summary>Hint 1</summary>For each simulation: `s = 0`; `while s < threshold:` roll `int(rng.integers(1, sides + 1))`; if it equals `bust`, set `s = 0` and `break`; else `s += roll`.</details>
<details><summary>Hint 2</summary>Add the final `s` to a total and return `total / n_sims`. Try a few thresholds around 20 and see how flat the value is near the optimum.</details>

### D1 `penney_prob`
<details><summary>Hint 1</summary>States = all proper prefixes of a and of b: `{a[:k] for k in range(len(a))} | {b[:k] for k in range(len(b))}` (includes ""). Give each an index.</details>
<details><summary>Hint 2</summary>Transition from state s on letter c: `t = s + c`; if `t.endswith(a)` → "A wins"; if `t.endswith(b)` → "B wins"; else drop letters from the front (`t = t[1:]`) until t is one of the states.</details>
<details><summary>Hint 3</summary>Build `M = np.eye(n)` and `rhs = np.zeros(n)`. For each state i and letter c: A wins → `rhs[i] += 0.5`; B wins → nothing; otherwise `M[i, j] -= 0.5`. Then `x = np.linalg.solve(M, rhs)` and return `x[index[""]]`.</details>

### D2 `expected_kth_order_stat`
<details><summary>Hint 1</summary>`x = np.linspace(0, 1, grid)`; `tail = sum(math.comb(n, j) * x**j * (1 - x)**(n - j) for j in range(k))` is a whole array.</details>
<details><summary>Hint 2</summary>Trapezoid rule: `dx * (tail.sum() - 0.5 * (tail[0] + tail[-1]))` with `dx = x[1] - x[0]` (or `np.trapezoid(tail, x)`).</details>
<details><summary>Hint 3</summary>Why k/(n+1)? ∫₀¹ xʲ(1−x)ⁿ⁻ʲ dx = j!(n−j)!/(n+1)!, so each of the k terms integrates to exactly 1/(n+1).</details>
