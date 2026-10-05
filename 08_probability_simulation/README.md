# 08 · Probability: exact vs Monte Carlo (≈ 1–1.5 hours)

**Goal:** code classic probability problems quickly, two ways: an exact answer (enumeration or formula) and a simulation that checks it.
Being able to say *"my answer is 6, let me verify with a 5-line simulation"* is a strong signal in a quant interview, and these
loops/vectorized patterns are exactly what a coding interviewer wants to see.

If you have a strong math background, the math may feel easy. **The practice here is the Python.**

## Patterns you'll use
```python
rng = np.random.default_rng(seed)          # modern numpy RNG, reproducible
rng.integers(1, 7, size=(n, 2))            # n rolls of 2 dice (7 is EXCLUSIVE)
rng.random(n)                              # n uniforms in [0, 1)
rng.random() < p                           # one Bernoulli(p) trial
rng.choice(data, size=(B, n), replace=True)  # bootstrap resamples
itertools.product(range(1, 7), repeat=3)   # all 216 outcomes of 3 dice
np.mean(condition_array)                   # fraction of True = probability estimate
```
**Monte Carlo error** ≈ √(p(1−p)/N) for a probability, or σ/√N for a mean. To get one more decimal digit you need 100× more simulations.

## Tasks
| ID | Function | Paper answer |
|---|---|---|
| A1–A2 | `dice_sum_exact`, `dice_sum_sim` | P(sum of 2 dice = 7) = 1/6 |
| A3 | `expected_flips_sim` | E[flips until HH] = 6, HT = 4 |
| B1–B2 | `birthday_exact`, `birthday_sim` | n = 23 → ≈ 50.7% |
| B3 | `estimate_pi` | π |
| C1–C2 | `gamblers_ruin_exact`, `gamblers_ruin_sim` | fair game: start/target |
| D1 | `bootstrap_ci` | ≈ mean ± 1.96·SE |
| D2–D3 | `coupon_collector_exact`, `coupon_collector_sim` | n·H_n (n = 6 → 14.7) |

## More probability questions to practise on paper (answers folded)
These are in the style reported for Citadel / Citadel Securities. Time yourself: about 3–5 minutes each.

<details><summary>1. Roll a die; you may re-roll once and must keep the second roll. Optimal strategy and expected value?</summary>

The second roll is worth 3.5, so keep the first roll if it is ≥ 4. EV = (1/2)(4+5+6)/3 + (1/2)(3.5) = 2.5 + 1.75 = **4.25**.
Three rolls total: keep the first if ≥ 5 (since the 2-roll game is worth 4.25), EV = (1/3)(5.5) + (2/3)(4.25) = **4.667**.
</details>

<details><summary>2. A test is 99% accurate; 1% of people have the disease. You test positive. P(disease)?</summary>

Bayes: P(D|+) = 0.99·0.01 / (0.99·0.01 + 0.01·0.99) = **50%**. The base rate matters as much as accuracy.
</details>

<details><summary>3. Expected number of rolls of a die until you see a 6? Until you see all six faces?</summary>

Geometric(1/6): **6**. All six faces: coupon collector 6·(1 + 1/2 + … + 1/6) = **14.7**.
</details>

<details><summary>4. Break a stick at two uniform random points. P(the three pieces form a triangle)?</summary>

Each piece must be < 1/2, which gives **1/4**. (Good one to verify with a simulation: `rng.random((n,2))`, sort, check the three lengths.)
</details>

<details><summary>5. X, Y i.i.d. Uniform(0,1). E[max(X,Y)]? E[min]? E[|X−Y|]?</summary>

max: 2/3, min: 1/3, |X−Y|: 1/3. In general, for n uniforms, E[k-th smallest] = k/(n+1).
</details>

<details><summary>6. You flip a fair coin until you get heads. You win 2^k dollars if it takes k flips. Fair price?</summary>

E = Σ (1/2)^k · 2^k = ∞, the **St. Petersburg paradox**. In practice: finite bankroll of the counterparty, utility of money (log utility), and risk aversion make the fair price small.
A good opening for a market-making discussion: "I'd quote a narrow price and adjust with flow".
</details>

<details><summary>7. Linearity of expectation: n people throw hats in a box, each takes one at random. Expected number who get their own hat?</summary>

Indicator for each person: P = 1/n, so E = n · 1/n = **1**, for any n. (P(nobody) → 1/e.)
</details>

<details><summary>8. Two cards drawn from a deck. P(both aces)? P(second is ace | first is ace)? P(second is ace)?</summary>

(4/52)(3/51) = 1/221. Conditional: 3/51 = 1/17. Unconditional P(second is ace) = **4/52** by symmetry.
</details>

<details><summary>9. A random walk starts at 0, ±1 with prob 1/2. Expected time to hit +3 or −3?</summary>

E[T] = a·b for barriers −a, +b, so **9**. (Proof: X_t² − t is a martingale, so E[X_T²] = E[T] = 9.)
</details>

<details><summary>10. Correlation between X and Y is ρ. Can corr(X,Y) = 0.9, corr(Y,Z) = 0.9, corr(X,Z) = −0.5?</summary>

The correlation matrix must be positive semi-definite. The bound is corr(X,Z) ≥ ρ_xy·ρ_yz − √((1−ρ_xy²)(1−ρ_yz²)) = 0.81 − 0.19 = 0.62.
So **no**, −0.5 is impossible. (Python check: `np.linalg.eigvalsh(M)` gives a negative eigenvalue.)
</details>

<details><summary>11. Market-making warm-up: I'll pay you the outcome of a die roll. Make me a two-sided market.</summary>

The fair value is 3.5. Quote something like **3.3 bid / 3.7 offer**, which is symmetric around fair, and the width reflects your uncertainty and risk.
If they keep lifting your offer, ask what they know (adverse selection) and move your quotes up. Expect follow-ups such as "now it's the max of two dice" (EV = 161/36 ≈ 4.47).
</details>

<details><summary>12. You have a 52-card deck; cards are revealed one by one. You may say "stop" once, before any card; you win if the NEXT card is red. Best strategy?</summary>

Every strategy wins with probability **1/2**. The proportion of red cards among the remaining cards is a martingale, so no stopping rule beats it.
</details>
