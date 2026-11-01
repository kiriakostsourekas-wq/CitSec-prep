# 12 · Probability & expected value (≈ 3 hours)

**Goal:** be fast and reliable on the questions that dominate quant trading and research finals (the probability round at Citadel Securities, for example):
*"what would you pay to play this game?"*, expected values, waiting times, optimal stopping, Bayes updates.
You answer them **out loud**, usually without a computer, so the code here is a training aid: each task turns one
paper technique into a small exact solver, and simulations confirm the answers. If a solver and your paper answer
disagree, one of them is wrong. Finding out which is the practice.

Suggested order: read the concept notes (15 min), do tasks A→D (≈ 2 hours), then the problem bank with a timer
(3–5 minutes per problem, talking out loud).

## Concept notes

**Conditioning / total expectation.** E[X] = Σ E[X | Aᵢ] P(Aᵢ) for any partition Aᵢ. Pick the partition that makes
each piece easy, usually "what happens first". Bayes is the same thing read backwards:
P(H | data) ∝ P(data | H) · P(H).

**Linearity of expectation + indicators.** E[X₁ + … + Xₙ] = Σ E[Xᵢ] *even when the Xᵢ are dependent*. To count
things (fixed points, adjacent couples, runs, distinct values), write the count as a sum of indicators and add up
their probabilities. If a count question looks hard, try this first.

**First-step analysis / recursion.** Name an unknown for every state (Eₛ = expected remaining time from s), condition
on the next step, get linear equations, solve. Example HH: E₀ = 1 + ½E₁ + ½E₀, E₁ = 1 + ½·0 + ½E₀, so E₀ = 6.

**Markov chains (absorbing).** With Q = transitions among transient states, expected steps to absorption solve
(I − Q)t = **1**, and absorption probabilities solve (I − Q)x = R·(indicator of target). N = (I − Q)⁻¹ counts the
expected visits to each state.

**Optimal stopping & backward induction.** Value = max(stop now, expected value of continuing). With a finite
horizon, go backwards from the last decision (re-roll games). With no horizon, try the **one-step look-ahead** rule:
stop when stopping beats exactly one more step. It is optimal when the problem is *monotone* (once that rule says
stop, it keeps saying stop), as in the bust-on-1 dice game.

**Martingales & optional stopping.** If Mₜ is a fair game (E[Mₜ₊₁ | past] = Mₜ) and the stopping time T is bounded
(or Mₜ stays bounded up to T), then E[M_T] = M₀. Consequences: gambler's ruin P(hit b before 0 | start a) = a/b;
Xₜ² − t is a martingale for a ±1 walk, so E[T] = a·b for barriers −a, +b; no strategy beats a fair game.

**Generating functions & branching.** G(s) = E[sˣ] = Σ pₖsᵏ. For a branching process the extinction probability is
the **smallest** root of G(q) = q in [0, 1]. It is < 1 exactly when the mean number of offspring G′(1) > 1.

**Symmetry & exchangeability.** In a shuffled deck every position is "the same" a priori. The 4 aces cut the 48
other cards into 5 gaps of equal expected size 48/5. Uniform order statistics: n points cut [0,1] into n + 1
exchangeable pieces, so E[k-th smallest] = k/(n+1). Use symmetry before computing anything.

## How to answer out loud (do this every time)
1. **Restate and define the random variable**: "Let V be my payout under optimal play; I want E[V]."
2. **Give a quick bound or guess first**: "it's at least 3.5, the no-re-roll value, and at most 6."
3. **Condition on the first step / the first decision**, and say the equation before solving it.
4. **Solve, then check extremes**: p = 0 or 1, n = 1, a symmetric case. Does the answer move in the right direction?
5. **State the strategy, not just the number**: "re-roll on 1–3, keep 4–6".
6. **Offer a sanity simulation**: "I'd verify with a 10-line Monte Carlo: about 10⁵ runs gives ±0.01 here."
7. If you get stuck, **say what you know**: an approach that works but is slow is worth more than silence.

## Tasks
| ID | Function | Technique | Paper answer |
|---|---|---|---|
| A1 | `absorbing_expected_steps` | (I − Q)t = 1 | walk on 0..4: [3, 4, 3] |
| A2 | `pattern_expected_flips` | KMP automaton + A1 | HH 6, HT 4, HTH 10, HHH 14 |
| A3 | `pattern_sim` | Monte Carlo | ≈ A2 |
| B1 | `reroll_value` | backward induction | 7/2, 17/4, 14/3 |
| B2 | `reflip_coins_value` | enumerate + threshold | 4 coins: 19/8 |
| B3 | `red_card_value` | DP over (r, b) | always r/(r+b) |
| B4 | `guess_sum_value` | maximise s·P(s) | d6 + d10: guess 11, EV 1.1 |
| C1 | `extinction_probability` | iterate q ← G(q) | amoeba: √2 − 1 |
| C2 | `posterior_biased` | Bayes | 1 head, prior ½, p = ¾: 3/5 |
| C3 | `prob_next_heads` | predictive probability | 13/20 |
| C4 | `bust_stop_game` | optimal stopping DP | stop at 20, EV ≈ 8.142 |
| C5 | `bust_stop_sim` | simulate a strategy | ≈ C4 |
| D1 | `penney_prob` | absorbing chain on two patterns | P(THH before HHT) = 3/4 |
| D2 | `expected_kth_order_stat` | E[Y] = ∫P(Y > x)dx | k/(n+1) |

## Problem bank (answers folded: try first, out loud, 3–5 minutes each)
These are classics of the kind reported for quant trading and research interviews. Every numeric answer below was checked by an exact
calculation and a simulation.

### 1. Games: what would you pay to play?

<details><summary>1.1 Roll a die and be paid the face value. You may re-roll, up to 3 rolls in total, and must keep the last. Fair price?</summary>

Backward: the last roll is worth 3.5, so with 2 rolls left keep 4, 5, 6: (4+5+6)/6 + (3/6)(3.5) = **17/4**.
With 3 rolls left keep only 5, 6 (since 4 < 4.25): (5+6)/6 + (4/6)(17/4) = **14/3 ≈ 4.67**. Strategy: keep ≥ 5, then ≥ 4, then anything.
</details>

<details><summary>1.2 Same die, unlimited re-rolls, but each re-roll costs $1. Value and strategy?</summary>

The value V solves V = E[max(X, V − 1)] (keep X if it beats rolling again, which is worth V − 1).
Try V = 4: E[max(X, 3)] = (3+3+3+4+5+6)/6 = 4. ✓ **V = 4**: keep 4, 5, 6 (at 3 you're indifferent).
Check by thresholds: keep ≥ 4 gives E[X | X ≥ 4] − (expected re-rolls = 1) = 5 − 1 = 4.
</details>

<details><summary>1.3 A d20 pays its face value; you may re-roll once (keep the second). Value?</summary>

The second roll is worth 10.5, so keep 11–20. Value = ½ · 15.5 + ½ · 10.5 = **13**.
</details>

<details><summary>1.4 We roll a d6 and a d10. Before the roll you name a number; if the sum equals it, you get that many dollars. What do you name and what is the game worth?</summary>

P(sum = s) = 6/60 for every s from 7 to 11 (the flat part of the distribution), and smaller outside.
You maximise s · P(s), so take the largest of the flat ones: **11**, worth 11 · 6/60 = **$1.10**. (12 gives 12 · 5/60 = 1.0.)
Follow-up: "paid a flat $10 if right": any of 7..11, worth $1.
</details>

<details><summary>1.5 Toss 4 fair coins, paid $1 per head. Once, you may re-toss ALL of them (and keep the result). Value?</summary>

Re-tossing is worth 2. Re-toss on 0 or 1 head, keep 2, 3, 4 (indifferent at 2).
Value = (1/16 + 4/16) · 2 + (6/16) · 2 + (4/16) · 3 + (1/16) · 4 = 38/16 = **19/8 = 2.375**.
Follow-up: "you may re-toss any subset once": re-toss every tail; each coin ends up heads with prob ¾, so **3**.
</details>

<details><summary>1.6 Roll a die repeatedly, adding the faces. You may stop any time and collect the total, but rolling a 1 loses everything. Strategy and value?</summary>

At total s, one more roll changes the expected total by −s/6 (bust) + (2+3+4+5+6)/6 = (20 − s)/6.
So **roll while s < 20, stop at ≥ 20** (indifferent at exactly 20). The problem is monotone, so this one-step rule is
optimal. Value ≈ **8.14** (task C4). Follow-up "fix the number of rolls n in advance": 4n(5/6)ⁿ, maximised at
n = 5 or 6 (equal), ≈ 8.04, which is lower because you can't react to the total.
</details>

<details><summary>1.7 Paid the product of two dice, or the square of one die. Which do you prefer?</summary>

Product: E[X]E[Y] = 3.5² = **49/4 = 12.25** (independence). Square: E[X²] = 91/6 ≈ **15.17**.
E[X²] − E[X]² = Var(X) = 35/12 > 0, so the square is better (Jensen).
</details>

<details><summary>1.8 Flip a coin until the first tail; you're paid $1 per head. Fair price?</summary>

Number of heads ~ Geometric starting at 0 with p = ½: mean (1 − p)/p = **$1**. (Paying 2^heads instead is St. Petersburg: infinite EV.)
</details>

### 2. Waiting times and first-step analysis

<details><summary>2.1 Expected number of coin flips until HH? HT? HTH? HHH? HHT?</summary>

**6, 4, 10, 14, 8.** HH: E₀ = 1 + ½E₀ + ½E₁, E₁ = 1 + ½E₀, so E₀ = 6.
Shortcut for a fair coin: E = Σ 2ᵏ over every k where the first k letters equal the last k letters.
HTH: 2 + 8 = 10 (it overlaps itself); HHT: 8 (no overlap). Self-overlap makes a pattern *slower* to appear.
</details>

<details><summary>2.2 Expected number of rolls of a die until two 6s in a row?</summary>

E₀ = 1 + (5/6)E₀ + (1/6)E₁ and E₁ = 1 + (5/6)E₀. Substituting: E₀/36 = 7/6, so **E₀ = 42** (= 6 + 6²).
</details>

<details><summary>2.3 Roll a die until the first 6. Expected sum of all rolls, including the 6?</summary>

Wald: E[sum] = E[N] · E[X] = 6 · 3.5 = **21**. (Check: 5 non-sixes on average, each uniform on 1–5 with mean 3, plus the 6: 15 + 6 = 21.)
</details>

<details><summary>2.4 Roll a die until the first 6. Given that every roll was even, what is the expected number of rolls?</summary>

Not 3! "All rolls even up to the first 6" means "the first roll that lands in {1, 3, 5, 6} is a 6".
The time N until the first roll in {1, 3, 5, 6} is Geometric(4/6) and independent of *which* of the four it is.
So E[N | it was 6] = E[N] = **3/2**.
</details>

<details><summary>2.5 A bug walks randomly on the edges of a cube (each of 3 neighbours with prob ⅓). Expected steps from a corner to the opposite corner?</summary>

Group by distance d to the target. E₃ = 1 + E₂, E₂ = 1 + ⅓E₃ + ⅔E₁, E₁ = 1 + ⅔E₂ + ⅓ · 0.
Solve: E₁ = 7, E₂ = 9, **E₃ = 10**.
</details>

<details><summary>2.6 Fair ±1 random walk from 2, absorbed at 0 and 5. P(reach 5)? Expected duration?</summary>

Xₜ is a martingale: 5p = 2, so **p = 2/5**. Xₜ² − t is a martingale: E[T] = E[X_T²] − 4 = 25 · (2/5) − 4 = **6** (= a(N − a) = 2 · 3).
</details>

<details><summary>2.7 Penney's game: I pick HHT, you then pick a pattern of length 3. What do you pick?</summary>

**THH**, which wins with prob **3/4**: unless the first two flips are HH (prob ¼, and then HHT must win), a T has
appeared before the first HH, so THH is completed first. In general, against x₁x₂x₃ pick (not x₂)x₁x₂: the second player always
has a pattern that wins with probability ≥ 2/3. "Beats" is not transitive (task D1).
</details>

<details><summary>2.8 Keep adding Uniform(0,1) numbers until the sum exceeds 1. Expected count?</summary>

P(N > n) = P(U₁ + … + Uₙ ≤ 1) = 1/n! (volume of a simplex). E[N] = Σₙ≥₀ P(N > n) = Σ 1/n! = **e ≈ 2.718**.
</details>

### 3. Conditioning and Bayes

<details><summary>3.1 Two dice. Given at least one is a 6, P(both are 6)? Given the first one is a 6?</summary>

At least one 6: 11 equally likely outcomes, one of them (6,6): **1/11**. Given the first die is 6: **1/6**.
The information "at least one" is weaker than "this specific one", so the conditional is different.
</details>

<details><summary>3.2 Two dice sum to 8. P(at least one is a 6)?</summary>

Outcomes: (2,6), (3,5), (4,4), (5,3), (6,2), so **2/5**.
</details>

<details><summary>3.3 One of 1000 coins is double-headed. You pick one at random and flip 10 heads in a row. P(double-headed)? P(next flip heads)?</summary>

Odds = prior odds × likelihood ratio = (1/999) · 2¹⁰ = 1024/999, so P = 1024/2023 ≈ **0.506**.
Next flip: 0.506 · 1 + 0.494 · ½ ≈ **0.753** (task C3).
</details>

<details><summary>3.4 A coin is fair or has P(H) = ¾, 50/50. You see one head. P(biased)? P(next is heads)? Would you take an even-money $1 bet on heads?</summary>

Posterior: (½ · ¾)/(½ · ¾ + ½ · ½) = **3/5**. Next heads: (3/5)(3/4) + (2/5)(1/2) = **13/20**.
Even-money bet on heads: EV = 13/20 − 7/20 = **+$0.30**, so yes. A fair price for "pays $1 on heads" is $0.65.
</details>

<details><summary>3.5 A coin's P(H) is unknown, uniform on [0,1]. You see 7 heads in 10 flips. P(next flip heads)?</summary>

Laplace's rule of succession: posterior is Beta(8, 4), mean (k+1)/(n+2) = **8/12 = 2/3**.
</details>

<details><summary>3.6 Russian roulette: 6 chambers, 2 bullets in ADJACENT chambers, cylinder spun once. The first trigger pull clicks (empty). Do you want it spun again before your pull?</summary>

Without spinning: you're in one of the 4 empty chambers; only the one just before the bullets leads to a bullet, so survive **3/4**.
Spinning: survive 4/6 = 2/3. **Don't spin.**
</details>

### 4. Linearity, indicators, symmetry

<details><summary>4.1 n couples sit at random around a round table of 2n seats. Expected number of couples sitting together?</summary>

For one couple: fix one partner; the other is uniform over the other 2n − 1 seats, 2 of them adjacent. So the answer is n · 2/(2n − 1) = **2n/(2n − 1)**.
</details>

<details><summary>4.2 Expected number of runs in n fair coin flips (HHTHH has 3 runs)?</summary>

Runs = 1 + #{i : flip i ≠ flip i−1}; each of the n − 1 indicators has prob ½. **E = (n + 1)/2.**
</details>

<details><summary>4.3 Roll a die 6 times. Expected number of distinct faces seen?</summary>

Face j is missed with prob (5/6)⁶. E = 6(1 − (5/6)⁶) ≈ **3.99**.
</details>

<details><summary>4.4 Birthdays: how many people until the EXPECTED number of shared-birthday pairs is ≥ 1? Until P(someone shares MY birthday) ≥ ½?</summary>

Expected pairs = C(n,2)/365 ≥ 1 at **n = 28** (C(27,2) = 351, C(28,2) = 378).
"Shares my birthday" needs 1 − (364/365)ⁿ ≥ ½, so n ≥ ln 2 / ln(365/364) ≈ 252.7, i.e. **253** other people. Compare 23 for "any pair".
</details>

<details><summary>4.5 Random permutation of 1..n (n ≥ 2). Expected number of local maxima (bigger than every neighbour, ends count)?</summary>

Interior position: the max of 3 with prob ⅓. Each end: the max of 2 with prob ½.
E = (n − 2)/3 + 1 = **(n + 1)/3**.
</details>

<details><summary>4.6 Shuffled deck. Expected position of the first ace? Of the second ace?</summary>

Each of the 48 non-aces is before all 4 aces with prob 1/5, so 48/5 of them precede the first ace on average.
First ace: 48/5 + 1 = **53/5 = 10.6**. Second ace: 2 · 48/5 + 2 = **106/5 = 21.2**.
</details>

<details><summary>4.7 Turn cards over until the first ace. Is the next card more likely to be the ace of spades or the 2 of clubs?</summary>

**Equal, both 1/52.** Take any order of the other 51 cards and insert the A♠ right after their first ace. This
gives every deck in which A♠ immediately follows the first ace exactly once, so there are 51! such decks out of 52!.
The same argument works word for word for the 2♣.
</details>

### 5. Optimal stopping and martingales

<details><summary>5.1 A deck of 26 red and 26 black is turned over one card at a time. Once, before the deck runs out, you say "next is red"; you win if it is. Best strategy? Prove it.</summary>

**Every strategy wins with probability exactly ½.** Proof: let Rₜ = fraction of red among the cards still in the deck.
Given the past, the next card is red with prob Rₜ, and E[Rₜ₊₁ | past] = Rₜ (it's a martingale).
If you call at stopping time τ, you win with prob E[R_τ] = R₀ = ½ by optional stopping (τ ≤ 51 is bounded).
Slicker: "the next card is red" has the same probability as "the LAST card is red" given anything you've seen,
so every strategy is equivalent to betting on the last card. Task B3 confirms with a DP: V(r, b) = r/(r + b).
</details>

<details><summary>5.2 Secretary problem: n candidates in random order, you must accept/reject each on the spot, and you only win if you pick the best. Strategy?</summary>

Reject the first ≈ n/e, then accept the first candidate better than all seen so far. P(win) → **1/e ≈ 0.368**.
</details>

<details><summary>5.3 Pólya urn: 1 red, 1 blue. Draw a ball, return it with another of the same colour; repeat 100 times. Distribution of the number of reds? P(the 101st draw is red)?</summary>

The number of reds is **uniform on {1, …, 101}**. The red fraction is a martingale, so P(red on any draw) = **½** unconditionally.
</details>

<details><summary>5.4 Amoeba: each minute it dies, stays, splits into 2 or splits into 3, each with prob ¼. Starting from one, P(the population dies out)?</summary>

q = ¼(1 + q + q² + q³), so (q − 1)(q² + 2q − 1) = 0. The extinction probability is the smallest root in [0,1]:
**q = √2 − 1 ≈ 0.414**. (Mean offspring 1.5 > 1, so q < 1 as expected.)
</details>

### 6. Continuous and geometric

<details><summary>6.1 n i.i.d. Uniform(0,1). E[max]? E[min]? E[k-th smallest]?</summary>

**n/(n+1), 1/(n+1), k/(n+1)**: the n points cut [0,1] into n + 1 pieces of equal expected length (symmetry), or use
E[Y] = ∫P(Y > x)dx, e.g. E[max] = ∫(1 − xⁿ)dx = n/(n+1) (task D2).
</details>

<details><summary>6.2 Break a stick at two uniform points. Expected length of the longest piece? The shortest?</summary>

For n pieces: E[k-th largest] = (1/n)(1/k + … + 1/n). With n = 3: longest = ⅓(1 + ½ + ⅓) = **11/18**, shortest = **1/9**.
</details>

<details><summary>6.3 Break a stick at a uniform point, then break the LONGER piece at a uniform point. P(the three pieces form a triangle)?</summary>

Longer piece L ~ Uniform(½, 1). Break it at V ~ Uniform(0, L). Need all pieces < ½: V ∈ (L − ½, ½), prob (1 − L)/L.
E = 2∫_{½}^{1} (1 − L)/L dL = **2 ln 2 − 1 ≈ 0.386** (vs ¼ for two independent breaks).
</details>

<details><summary>6.4 Two people arrive uniformly between 12:00 and 13:00 and each waits 15 minutes. P(they meet)?</summary>

Complement: two corner triangles of the unit square with total area (45/60)² = 9/16. P = **7/16**.
</details>

<details><summary>6.5 Three uniform random points on a circle. P(the triangle contains the centre)?</summary>

Contains the centre iff the points are NOT all in one semicircle. P(all in a semicircle) = n/2ⁿ⁻¹ = 3/4, so **1/4**.
</details>

## Interviewer follow-ups

<details><summary>1. (A2) Why does HTH take longer than HHT when both have probability 1/8 per position?</summary>

The occurrences of HTH can overlap (HTHTH contains two), so they come in clumps. The long-run frequency is the same, so the
gaps between clumps must be longer. Formally, by the "casino" martingale: E[T] = Σ 2ᵏ over self-overlaps k.
</details>

<details><summary>2. (B1) Make me a market on the 3-roll re-roll game.</summary>

Fair value 14/3 ≈ 4.67. Quote around it, e.g. **4.5 bid / 4.85 offer**. Width reflects the payout's variance and your risk.
If someone lifts your offer repeatedly, ask whether they know something (are the dice loaded?) and move up.
</details>

<details><summary>3. (B3) Now you start with $1 and may bet any fraction of your wealth, at even money, on the colour of EVERY card. How do you bet?</summary>

Bet on the majority colour among the remaining cards, a fraction |r − b|/(r + b) of your wealth (the Kelly fraction 2p − 1),
and nothing when r = b. Remarkably your final wealth is then **deterministic**: 2⁵²/C(52, 26) ≈ **9.08** whatever the order.
Unlike the one-shot game, repeated betting lets you exploit the known composition.
</details>

<details><summary>4. (C1) Without solving, when is the extinction probability 1?</summary>

When the mean number of children m = Σ k pₖ ≤ 1 (excluding the trivial "always exactly 1 child"). G is convex with
G(1) = 1 and G′(1) = m; if m ≤ 1 the curve stays above the diagonal on [0, 1), so the only fixed point is 1.
</details>

<details><summary>5. (C4) Your simulation says 8.11 and your DP says 8.142. Bug?</summary>

Not necessarily: the payout's standard deviation is ≈ 10.5, so 50 000 runs give a standard error of ≈ 0.047, and 8.11 is
within 1σ. Always quote the error bar with a simulation: σ/√N.
</details>

<details><summary>6. (C2/C3) The coin showed 10 heads. You're offered a bet: pay $0.70 to win $1 if the next flip is heads. Take it?</summary>

With the 1-in-1000 double-headed prior, P(next heads) ≈ 0.753 > 0.70, so yes (EV ≈ +$0.05), but it is sensitive to the prior.
Say so, and ask how the coin was chosen.
</details>

<details><summary>7. (D1) Is there a pattern of length 3 that beats every other one?</summary>

No. Penney's game is non-transitive: HHT is beaten by THH (3:1), which is beaten by TTH (2:1), which is beaten by HTT (3:1), which is beaten by HHT (2:1).
</details>

<details><summary>8. General: how many simulations do you need to distinguish 8.14 from 8.09?</summary>

Difference 0.05; with σ ≈ 10.5 you want σ/√N ≲ 0.05/3, so N ≈ (3 · 10.5 / 0.05)² ≈ 400 000 runs. Variance, not the mean, sets the cost.
</details>
