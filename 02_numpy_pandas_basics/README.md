# 02 · numpy & pandas basics (≈ 1.5–2 hours)

**Goal:** become fluent with the two libraries you'll use in every ML folder after this one.
If pandas is new for you, this is the most important "tooling" folder. Go slowly, use the
cheatsheets (`../cheatsheets/numpy_cheatsheet.md`, `../cheatsheets/pandas_cheatsheet.md`), and experiment
in the playground at the bottom of `exercise.py`.

**Dataset:** `data/stock_prices.csv`, 60 business days × 4 fictional tickers, in **long format**
(one row per date per ticker; the tickers' rows are interleaved):

| date | ticker | close | volume |
|---|---|---|---|
| 2026-01-05 | AAA | 98.46 | 172604 |
| 2026-01-05 | BBB | 48.61 | 375750 |

## Core mental models (read first!)

**numpy: shapes and axes.** A dataset `X` has shape `(n, d)`: n rows (samples) and d columns (features).
- `X.mean(axis=0)` → collapses rows → one number **per column** → shape `(d,)`
- `X.sum(axis=1)` → collapses columns → one number **per row** → shape `(n,)`
- **Broadcasting:** `X - X.mean(axis=0)` subtracts the column-mean vector from *every row*. Shapes are
  compared from the right: `(n, d)` and `(d,)` are compatible.
- **Boolean mask:** `x[x > 0]` keeps the entries where the condition is True.
- `A @ B` is matrix multiplication; `A * B` is element-wise.

**pandas: a DataFrame is a table of named columns (Series) with an index.**
- `df["close"]` → a Series. `df[["close", "volume"]]` → a DataFrame.
- Filter rows: `df[(df["ticker"] == "AAA") & (df["volume"] > 1e5)]` (use `&`/`|`, and **brackets around each condition**)
- **split-apply-combine:** `df.groupby("ticker")["close"].mean()`, which means "for each ticker, average the close"
- Long → wide: `df.pivot(index="date", columns="ticker", values="close")`
- Time series: `.pct_change()`, `.rolling(5).mean()`, `.cummax()`, `.shift(1)`

## Tasks
| ID | Function | Skill |
|---|---|---|
| A1–A5 | `filter_positive`, `standardize`, `add_intercept`, `solve_linear_system`, `distances_to_point` | numpy, no loops |
| B1 | `load_prices` | `read_csv`, datetimes |
| B2 | `average_close_by_ticker` | `groupby` |
| B3 | `add_daily_returns` | `groupby` + `pct_change` (classic bug: computing a return *across* two tickers) |
| B4 | `to_wide` | `pivot` |
| C1–C4 | `rolling_mean`, `high_volume_days`, `best_day_per_ticker`, `return_correlation` | rolling, filtering, `idxmax`, `corr` |
| D1 | `annualized_sharpe` | the formula behind every "Sharpe of X" claim |
| D2 | `max_drawdown` | `cummax` |

## Interviewer follow-ups

<details><summary>1. Why correlate returns and not prices?</summary>

Prices are non-stationary (they trend). Two completely unrelated trending series can have a price correlation
near ±1 ("spurious correlation"). Returns are much closer to stationary, so their correlation means something.
</details>

<details><summary>2. Why multiply by √252 to annualize Sharpe?</summary>

If daily returns are i.i.d., the mean scales with time (×252) and the variance scales with time (×252), so the std scales
with √252. Sharpe = mean/std therefore scales with 252/√252 = √252. This assumes no autocorrelation; with
autocorrelated returns the annualization is wrong (Lo, 2002).
</details>

<details><summary>3. These tickers show Sharpe 2–4 over 60 days. Impressive?</summary>

No. The standard error of an annualized Sharpe estimated from T daily observations is roughly
√(252/T) ≈ √(252/60) ≈ 2. So a Sharpe of 2 over 60 days is statistically indistinguishable from 0.
**If your CV quotes a Sharpe ratio, be ready to discuss this:** over how many years? out-of-sample?
after transaction costs? how many signals were tried before picking the best (multiple testing)?
</details>

<details><summary>4. Simple returns vs log returns?</summary>

Simple: r = P_t/P_{t-1} − 1, which aggregates across **assets** (portfolio return = weighted sum).
Log: ℓ = ln(P_t/P_{t-1}), which aggregates across **time** (multi-day log return = sum of daily log returns).
For small returns they are almost equal (ln(1+r) ≈ r).
</details>

<details><summary>5. What does `.shift(1)` do and why does it matter for backtests?</summary>

It moves the values down one row, so row t holds the value from t−1. When you build a signal from data at
time t, you can only trade on it at t+1, so you compare `signal.shift(1)` with `returns`. Forgetting this is
**look-ahead bias**, the #1 backtest bug.
</details>
