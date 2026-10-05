# Hints · 10 Mock interview
(In the real interview, the interviewer would give you these nudges if you asked. Asking good questions is fine!)

### S1 `load_and_clean`
<details><summary>Hint 1</summary>`pd.read_csv(path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)`</details>
<details><summary>Hint 2</summary>`df["temp_c"] = df["temp_c"].interpolate()` (same for humidity).
`df["t"] = (df["date"] - df["date"].iloc[0]).dt.days`.
`pd.get_dummies(df, columns=["weather"], drop_first=True, dtype=int)`.</details>

### S2 `time_split`
<details><summary>Hint 1</summary>`n_train = round(train_frac * len(df))`; `df.iloc[:n_train]`, `df.iloc[n_train:]`.</details>

### S3 `baseline_rmse`
<details><summary>Hint 1</summary>`pred = np.full(len(test), train["rentals"].mean())`, then `rmse(test["rentals"], pred)`.</details>

### S4 `linear_fit_eval`
<details><summary>Hint 1</summary>

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(train[features], train["rentals"])
pred = model.predict(test[features])
```
</details>
<details><summary>Hint 2</summary>`bias = float(np.mean(pred - test["rentals"]))`. Look at `model.coef_` for `t` too.</details>

### S6 `tree_rmse`
<details><summary>Hint 1</summary>`from sklearn.tree import DecisionTreeRegressor`, the same fit/predict pattern as S4.</details>

### S7 `busy_day_auc`
<details><summary>Hint 1</summary>`threshold = train["rentals"].median()`; `y_tr = (train["rentals"] > threshold).astype(int)`, and the same threshold for test.</details>
<details><summary>Hint 2</summary>

```python
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(train[features], y_tr)
p = model.predict_proba(test[features])[:, 1]      # column 1 = P(busy)
return roc_auc_score(y_te, p)
```
</details>
