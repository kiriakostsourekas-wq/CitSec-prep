# Hints · 02 numpy & pandas
Open one hint at a time.

### A1 `filter_positive`
<details><summary>Hint 1</summary>`x > 0` gives an array of booleans. Indexing an array with booleans keeps the True positions.</details>
<details><summary>Hint 2</summary>`return x[x > 0]`</details>

### A2 `standardize`
<details><summary>Hint 1</summary>`X.mean(axis=0)` gives one mean per column. Same for `X.std(axis=0)`.</details>
<details><summary>Hint 2</summary>Broadcasting lets you write `(X - mu) / sd` directly. No loop needed.</details>

### A3 `add_intercept`
<details><summary>Hint 1</summary>`np.ones((n, 1))` is a column of ones. `n = X.shape[0]`.</details>
<details><summary>Hint 2</summary>`np.hstack([ones, X])` glues arrays side by side (`np.column_stack` also works).</details>

### A4 `solve_linear_system`
<details><summary>Hint 1</summary>Look in `np.linalg`. In the REPL: `help(np.linalg.solve)`.</details>

### A5 `distances_to_point`
<details><summary>Hint 1</summary>`X - p` subtracts p from every row (broadcasting). Then square, sum across columns, square root.</details>
<details><summary>Hint 2</summary>"Across columns" = `axis=1`. Or use `np.linalg.norm(X - p, axis=1)`.</details>

### B1 `load_prices`
<details><summary>Hint 1</summary>`pd.read_csv(path)` reads it; dates come in as strings by default.</details>
<details><summary>Hint 2</summary>`pd.read_csv(path, parse_dates=["date"])` or afterwards `df["date"] = pd.to_datetime(df["date"])`.</details>

### B2 `average_close_by_ticker`
<details><summary>Hint 1</summary>Pattern: `df.groupby(KEY)[COLUMN].AGGREGATION()`.</details>
<details><summary>Hint 2</summary>`df.groupby("ticker")["close"].mean()`</details>

### B3 `add_daily_returns`
<details><summary>Hint 1</summary>`series.pct_change()` computes x_t/x_{t-1} − 1. But if you call it on the whole column, the
first AAA row would be compared with the previous row, which is a DDD price!</details>
<details><summary>Hint 2</summary>Make a copy, sort by `["ticker", "date"]`, then `out.groupby("ticker")["close"].pct_change()`.
The groupby makes pct_change restart for every ticker.</details>
<details><summary>Hint 3</summary>

```python
out = df.sort_values(["ticker", "date"]).copy()
out["return"] = out.groupby("ticker")["close"].pct_change()
return out
```
</details>

### B4 `to_wide`
<details><summary>Hint 1</summary>`df.pivot(index=..., columns=..., values=...)`, then `.sort_index()`.</details>

### C1 `rolling_mean`
<details><summary>Hint 1</summary>`wide.rolling(window).mean()` applies to every column at once.</details>

### C2 `high_volume_days`
<details><summary>Hint 1</summary>Build a mask with two conditions: `(df["ticker"] == ticker) & (df["volume"] >= min_volume)`. The brackets are required.</details>
<details><summary>Hint 2</summary>`df[mask].sort_values("volume", ascending=False)`</details>

### C3 `best_day_per_ticker`
<details><summary>Hint 1</summary>Call `add_daily_returns(df)` first. Then for each ticker find the row label of the max return: `groupby(...)["return"].idxmax()`.</details>
<details><summary>Hint 2</summary>`r.loc[idx]` selects those rows. A date `d` becomes a string with `d.strftime("%Y-%m-%d")`.</details>
<details><summary>Hint 3 (alternative, simpler)</summary>`rets = wide.pct_change()`, then `rets[t].idxmax()` is the date of the max for ticker t
(the index of the wide table is the date). You can build `wide` with your `to_wide`.</details>

### C4 `return_correlation`
<details><summary>Hint 1</summary>Returns first: `wide.pct_change()`. Then `.corr()`.</details>

### D1 `annualized_sharpe`
<details><summary>Hint 1</summary>`r = wide.pct_change().dropna()`; `r.mean()` and `r.std()` give one value per column.</details>
<details><summary>Hint 2</summary>`r.mean() / r.std() * np.sqrt(periods_per_year)`</details>

### D2 `max_drawdown`
<details><summary>Hint 1</summary>`prices.cummax()` is the running maximum so far.</details>
<details><summary>Hint 2</summary>`dd = prices / prices.cummax() - 1`; the answer is `float(dd.min())`.</details>
