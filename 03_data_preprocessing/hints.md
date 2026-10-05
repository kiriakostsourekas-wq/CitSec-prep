# Hints · 03 Data pre-processing
Every B/C function should start with `out = df.copy()` and end with `return out`.

### A2 `missing_report`
<details><summary>Hint 1</summary>`df.isna()` is a table of True/False. Summing it counts the Trues per column.</details>
<details><summary>Hint 2</summary>`counts = df.isna().sum()`; keep `counts[counts > 0]`; then `.sort_values(ascending=False)`.</details>

### A3 `drop_duplicate_rows`
<details><summary>Hint 1</summary>`df.drop_duplicates()` then `.reset_index(drop=True)` (drop=True means "don't keep the old index as a column").</details>

### B1 `clean_income`
<details><summary>Hint 1</summary>String methods on a column live under `.str`: `out["income"].str.replace(",", "")`.</details>
<details><summary>Hint 2</summary>Then `.astype(float)`. NaN values pass through `.str` methods untouched, so they stay NaN.</details>

### B2 `clean_city`
<details><summary>Hint 1</summary>Chain two string methods: one removes spaces at both ends, one makes "lONDON" → "London".</details>
<details><summary>Hint 2</summary>`out["city"] = out["city"].str.strip().str.title()`</details>

### B3 `fix_age`
<details><summary>Hint 1</summary>Build a mask of bad rows: `(out["age"] < 18) | (out["age"] > 100)`.</details>
<details><summary>Hint 2</summary>Assign with `.loc`: `out.loc[bad, "age"] = np.nan`. (Writing `out["age"][bad] = ...` is "chained assignment" and does **not** work in modern pandas.)</details>

### B4 `add_tenure_days`
<details><summary>Hint 1</summary>`pd.to_datetime(out["signup_date"])` gives datetimes. Subtracting two datetimes gives a "timedelta".</details>
<details><summary>Hint 2</summary>`(pd.Timestamp(reference_date) - signup).dt.days` turns timedeltas into integers. Then `out.drop(columns=["signup_date"])`.</details>

### C1 `one_hot`
<details><summary>Hint 1</summary>`out["plan"] = out["plan"].fillna("unknown")`</details>
<details><summary>Hint 2</summary>`pd.get_dummies(out, columns=["city", "plan"], drop_first=True, dtype=int)`</details>

### C2 `train_test_split_df`
<details><summary>Hint 1</summary>`rng = np.random.default_rng(seed)`; `idx = rng.permutation(len(df))` is a shuffled array of 0..n−1.</details>
<details><summary>Hint 2</summary>`n_test = round(test_frac * len(df))`; test positions = `idx[:n_test]`, train positions = `idx[n_test:]`.</details>
<details><summary>Hint 3</summary>Select rows by **position** with `.iloc`: `df.iloc[idx[n_test:]]`. Return `(train, test)` in that order.</details>

### C3 `fit_preprocessor`
<details><summary>Hint 1</summary>Loop over the column names; build a dict of dicts.</details>
<details><summary>Hint 2</summary>

```python
params = {}
for col in numeric_cols:
    med = train_df[col].median()
    filled = train_df[col].fillna(med)
    params[col] = {"median": med, "mean": filled.mean(), "std": filled.std()}
return params
```
</details>

### C4 `apply_preprocessor`
<details><summary>Hint 1</summary>For each `col, p in params.items()`: fill NaN with `p["median"]`, subtract `p["mean"]`, divide by `p["std"]`.</details>

### D1 `build_dataset`
<details><summary>Hint 1</summary>Just call your functions in the order of the docstring. Re-assign `df = step(df)` each time.</details>
<details><summary>Hint 2</summary>Column selection in a fixed order: `train[FEATURES].to_numpy(dtype=float)` with
`FEATURES = ["age", "income", "monthly_spend", "tenure_days", "city_London", "city_Paris", "plan_premium", "plan_unknown"]`.</details>
