# 00 · Interview guide: what to expect in the Citadel final round

Read this first (≈ 20 minutes), then again the evening before the interview.

## 1. The format (from candidate reports, 2024–2026)

The final round ("superday") is usually **4–6 back-to-back interviews of 30–45 minutes**, often virtual, each run by a
different interviewer focusing on one area:

| Interview type | What it looks like | Where to practise here |
|---|---|---|
| **Probability / brainteasers** | expected value, conditional probability, Bayes, dice/coins/cards, sometimes Markov chains | `08_probability_simulation/README.md` (12 questions + code) |
| **Coding** | live editor (often CoderPad), Python; easy–medium LeetCode, e.g. "implement a moving average for a Python list", sometimes DP | `01_python_warmup`, `09_algorithms` |
| **ML / statistics** | mostly open-ended ML questions plus simple implementation: linear regression (very common), regularization, overfitting, evaluation | `03`–`07`, `ml_stats_questions.md` |
| **Resume deep dive / behavioural** | "walk me through your research", "why Citadel", teamwork, failure | `cv_and_behavioral.md` |
| **Market intuition** (more for trading roles / Citadel Securities) | market-making games, making a two-sided price, risk/reward | `08` questions 6 & 11, `cv_and_behavioral.md` §4 |

Things candidates repeatedly mention:
- **Linear regression comes up again and again**, including questions like *"What happens to the coefficients, R² and t-stats if you duplicate the data?"*
  (→ `04_linear_regression`, task D3 + follow-ups).
- Interviewers care about **how you think**: stating assumptions, explaining a trade-off precisely, staying calm when pushed.
- **Citadel** (the hedge fund, including GQS) leans more on stats/ML/research. **Citadel Securities** (the market maker) leans more on probability speed and market making.
  Check which entity and role your interview is for, and weight your last days accordingly.

**For an early-year undergrad (1st–3rd year)** the bar is: solid fundamentals, clean basic code, clear thinking, and real curiosity.
Nobody expects you to know transformers inside out. They *do* expect you to know everything on your own CV in depth.

## 2. Know your profile: strengths and risks (fill this in honestly)
Typical patterns for candidates who reach this round, and what to do about each:
- **Strong math / probability** (competitions, a math-heavy degree): interviewers notice quickly and may push you to harder questions.
  That's good, so stay structured and keep talking. Don't skip steps just because they feel obvious to you.
- **Research or trading experience on the CV** (a backtest, a paper, a trading competition): it's your best selling point and also your
  biggest risk, because they *will* dig into it. Prepare `cv_and_behavioral.md` §1–2 seriously.
- **Theory > coding** (you know the ML theory but haven't implemented much, or pandas is new): that's what folders 01–07 fix.
  In the interview, clean simple code that you explain beats clever code.
- **Little or no finance knowledge:** fine for most quant research roles. Be curious, and know the basics in `02` part D and `ml_stats_questions.md` §C.

> **Your notes:** my 2 strongest areas: … / my 2 weakest areas (and which folders target them): …

## 3. How to answer (all rounds)
1. **Clarify.** Restate the question and ask about assumptions ("is the coin fair?", "can the input be empty?").
2. **Structure out loud.** "I'll first do X, then Y." Silence is the enemy: the interviewer can't give credit for thoughts they can't hear.
3. **Start simple, then improve.** Brute force → optimized. Baseline → model.
4. **Sanity-check.** Extreme cases (n = 1, p = 0), units, "does this number make sense?".
5. **When stuck,** say what you know, what you're trying, and ask for a nudge. Taking a hint well is a positive signal.
6. **When wrong,** say so as soon as you notice: "Actually that's not right, because…". Correcting yourself is valued highly in trading.
7. **Finish** by summarizing the answer and its limitations.

## 4. Study plan (≈ 12–15 hours)
See the root `README.md` for the day-by-day plan. Short version:
`00 guide → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 mock`, then redo the parts you found hardest.

## 5. The day before / the day of
- [ ] Re-read: this file, `cv_and_behavioral.md`, all the folded "Interviewer follow-ups" in folders 04, 05 and 07
- [ ] Do 3–4 probability questions from `08` cold, out loud, timed
- [ ] Re-do `09_algorithms` A1–A3 from a blank file in < 15 minutes (`python tools/reset.py 09`)
- [ ] Prepare 2–3 questions to ask each interviewer (see `cv_and_behavioral.md` §5)
- [ ] Test camera, mic, internet; have paper + pen; close everything else
- [ ] Sleep. A rested brain is worth more than one more hour of cramming.

## Sources (for reference when you are online; everything you need is already summarized above)
- Interview Query, Citadel quantitative analyst guide: https://www.interviewquery.com/guides/citadel-quantitative-analyst
- QuantT, Citadel interview overview: https://www.quantt.co.uk/resources/citadel-interview
- Dataford, Citadel Securities quantitative analyst guide: https://dataford.io/interview-guides/citadel-securities/quantitative-analyst
- techinterview.org, Citadel Securities guide 2026: https://www.techinterview.org/companies/citadel-securities/
- The Wall Street Quants, "linear regression with duplicate data" (Citadel question): https://thewallstreetquants.com/solution/citadel/linear-regression-duplicate-data-effects
- Glassdoor, a Citadel interview review: https://www.glassdoor.ca/Interview/Citadel-Interview-E14937-RVW59473910.htm
