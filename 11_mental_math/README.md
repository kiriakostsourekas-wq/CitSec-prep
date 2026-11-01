# 11 · Mental math (15 minutes a day, every day until the interview)

Some quant trading firms screen with a timed arithmetic test (reported: about 60–80 questions in 8 minutes, no paper), and in
probability rounds and market-making games **fast, reliable arithmetic is what lets you talk while you think**. Slow arithmetic isn't judged harshly
on its own, but it eats the time you need for reasoning.

```bash
cd 11_mental_math
python drill.py                     # 8 min / 80 questions, all topics
python drill.py --minutes 3 --topics frac pct ev
python drill.py --history           # your progress
```
Topics: `mul` (2×1, 2×2, 3×1 digits), `div`, `add` (decimals), `pct`, `frac` (fraction → decimal), `sq` (squares), `ev` (quick expected values).
**Plan:** one full 8-minute run per day + 3 minutes on your weakest topic. Track accuracy first, then speed.

## Tricks worth knowing cold
| Trick | Example |
|---|---|
| ×5 = ×10 ÷ 2 | 68 × 5 = 680 ÷ 2 = 340 |
| ×25 = ×100 ÷ 4 | 36 × 25 = 3600 ÷ 4 = 900 |
| ×11: add neighbours | 47 × 11 = 4 (4+7) 7 = 517 |
| ×9 = ×10 − x | 76 × 9 = 760 − 76 = 684 |
| split one factor | 37 × 24 = 37 × 25 − 37 = 925 − 37 = 888 |
| difference of squares | 47 × 53 = 50² − 3² = 2491 |
| squares ending in 5 | 75² = 7×8 → 56, then 25 → 5625 |
| squares near 50 | 48² = 2500 − 2·2·50 + 4 = 2304 (i.e. (50−2)²) |
| percent swap | 16% of 25 = 25% of 16 = 4 |
| divide by 5 / 25 / 125 | ×2 ÷10, ×4 ÷100, ×8 ÷1000 |
| round then fix | 398 × 7 = 2800 − 14 = 2786 |

## Fraction ↔ decimal table (memorise)
| 1/2 = .5 | 1/3 = .333 | 1/4 = .25 | 1/5 = .2 | 1/6 = .1667 | 1/7 = .142857 |
|---|---|---|---|---|---|
| **1/8 = .125** | **1/9 = .111** | **1/11 = .0909** | **1/12 = .0833** | **1/16 = .0625** | **1/20 = .05** |

Multiples: 3/8 = .375, 5/8 = .625, 7/8 = .875, 2/7 = .2857, 3/7 = .4286, 5/6 = .8333, 5/12 = .4167, 7/16 = .4375.

## Numbers that show up in probability/market games
- Dice: E = 3.5, Var = 35/12 ≈ 2.92, sd ≈ 1.71. Sum of n dice: sd ≈ 1.71·√n (2 dice 2.42, 3 dice 2.96, 4 dice 3.42).
- Sum of 2 dice: P(7) = 6/36, P(6) = P(8) = 5/36, P(2) = 1/36. E[max of 2] = 161/36 ≈ 4.47, E[min of 2] = 91/36 ≈ 2.53.
- Coin: n flips → mean n/2, sd √n / 2 (100 flips: sd 5).
- Uniform(0,1): mean 1/2, Var 1/12, sd ≈ 0.289. Max of n uniforms: n/(n+1).
- Card deck: 52 cards, 4 aces: P(ace) = 1/13 ≈ .077; C(52,5) = 2,598,960.
- e ≈ 2.718, ln 2 ≈ 0.693, ln 10 ≈ 2.303, √2 ≈ 1.414, √3 ≈ 1.732, 1/e ≈ 0.368, 2^10 = 1024.
- Normal: ±1σ = 68%, ±1.645σ = 90%, ±1.96σ = 95%, ±2.58σ = 99%.
