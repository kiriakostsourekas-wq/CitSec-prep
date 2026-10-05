# 10 · Mock interview: forecasting bike rentals (60 minutes, timed)

Do this **last**, after folders 03–07. Treat it like the real thing:
- set a 60-minute timer
- **talk out loud the whole time** (record yourself on your phone, then listen back: are you explaining your reasoning or just typing?)
- only open `hints.md` / the folded answers when the "interviewer" below would have helped you anyway

You can redo it a second time a few days later (`python ../tools/reset.py 10`). The second run should take about 35 minutes.

---

## The interviewer's script

> **Interviewer:** "Here's a year of daily bike-rental data for a city. We want to forecast daily rentals for the
> next quarter so operations can plan staffing. Walk me through how you'd approach it. Feel free to code."

### Stage 1: explore & clean (≈ 10 min) → `load_and_clean`
What a strong candidate says *before* touching a model:
- "Let me look at the shape, the dtypes, the missing values and the ranges." (`df.describe()`, `df.isna().sum()`)
- "What's the target's distribution? Is there seasonality or a trend?" (`df.groupby(df.date.dt.month).rentals.mean()`)
- "There are a few missing temperatures. Because it's a time series, I'll interpolate from the neighbouring days rather than use a global mean
  (a January gap filled with the annual mean would be about 15°C, which is absurd)."

<details><summary>Interviewer probe: "Is interpolation leakage?"</summary>

Slightly: it uses the next day's value. For a live forecasting system you'd forward-fill (or use the weather *forecast*, which is what you'd
actually have at prediction time). Saying this unprompted is a very good signal.
</details>

### Stage 2: split (≈ 5 min) → `time_split`
> **Interviewer:** "How will you evaluate?"

"We're forecasting the future, so the test set must be the **last** part of the data: train on Jan–Sep, test on Oct–Dec. A random split
would let the model train on days surrounding each test day, which is look-ahead."

### Stage 3: baseline (≈ 5 min) → `baseline_rmse`
"Before any model: predict the training mean. That's the number to beat." (≈ 1168 RMSE)

### Stage 4: linear regression (≈ 10 min) → `linear_fit_eval`
Fit with `FEATURES + ["t"]` (the day index, to capture growth) and with `FEATURES` alone.

> **Interviewer:** "Your model with the time trend is *worse than the baseline*. What happened?"

<details><summary>Answer (try first!)</summary>

Look at the **bias**: on test the model over-predicts by ≈ 1450 rentals per day. In Jan–Sep rentals rise mostly because of the
**season** (warmer weather), and the linear trend `t` absorbs part of that seasonal rise (coefficient ≈ 7.7/day while the true trend is 2.5/day).
In Oct–Dec the season reverses but `t` keeps going up, so the model extrapolates a line that is no longer true.
Lessons: (1) always inspect residuals and bias, not just one score; (2) trend features extrapolate dangerously; (3) with less than one full seasonal cycle,
trend and seasonality are confounded. With several years of data you could add month / day-of-year features (sin/cos encoding) to separate them.
(4) A random split would have hidden all of this: `python solution.py` shows it.
</details>

### Stage 5: feature engineering (≈ 5 min) → `add_temp_squared`
> **Interviewer:** "Is the effect of temperature linear?"

"Probably not. People cycle less when it's freezing *and* when it's very hot, so it's an inverted U. A linear model can capture that with a temp² term."
Then **test it**: here temp² helps in-sample but not on the Oct–Dec test set (temperatures there never reach the hot range).
"Feature engineering has to be validated, not assumed" is a great sentence to say.

### Stage 6: a tree (≈ 10 min) → `tree_rmse`
> **Interviewer:** "Would a tree do better?"

Trees capture the non-linearity automatically without temp², and depth acts as a regularizer. But a tree **cannot extrapolate**:
it predicts constants learned from the training range. That's harmless for temperature here, and it would be a problem for a growing trend.
Here the best linear model (≈ 500) beats the tree (≈ 640–910): with little data and a mostly additive structure, simple models win.

### Stage 7: classification twist (≈ 10 min) → `busy_day_auc`
> **Interviewer:** "Ops says they only need to know if tomorrow is a *busy* day. Change your approach."

Define busy = rentals > **train** median (computing the threshold on test data would be leakage). Logistic regression gives AUC ≈ 0.95.
Then discuss the threshold: missing a busy day (understaffing) vs overstaffing costs → choose the probability cut-off on validation data.

### Wrap-up questions (answer out loud, ≈ 5 min)
<details><summary>"How would you put this in production?"</summary>

Retrain on a rolling window, validate walk-forward (train up to month m, test month m+1, repeat), use weather **forecasts** as inputs,
monitor errors and input drift, and keep a simple fallback model (e.g. same weekday last week, adjusted by the forecast temperature).
</details>

<details><summary>"How confident are you in your forecast? Give me an interval."</summary>

Use the residual standard deviation on the validation period: roughly ± 1.96·RMSE for a 95% interval. Better: quantile regression or
bootstrapping residuals. Note the errors are probably larger on rainy days (heteroskedastic).
</details>

<details><summary>"What other data would you want?"</summary>

Several years (to separate trend from seasonality), holidays and events, the hourly pattern, station-level data, the number of bikes available
(rentals are capped by supply, so observed demand is *censored*), and weather forecasts as actually issued.
</details>

---

## How to score yourself
| | ✅ |
|---|---|
| Looked at the data before modelling | |
| Chose a time-based split and explained why | |
| Computed a baseline before any model | |
| Diagnosed the `t` problem from the bias / residuals | |
| Validated temp² instead of assuming it helps | |
| Knew a tree can't extrapolate | |
| Used the **train** median for the classification threshold | |
| Talked continuously, stated assumptions, and finished on time | |
