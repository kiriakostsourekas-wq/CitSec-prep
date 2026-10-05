# Hints · 04 Linear regression

### A1 `simple_fit`
<details><summary>Hint 1</summary>Compute `x_bar = x.mean()` and `y_bar = y.mean()` first.</details>
<details><summary>Hint 2</summary>`b = np.sum((x - x_bar) * (y - y_bar)) / np.sum((x - x_bar) ** 2)`, then `a = y_bar - b * x_bar`. Return `a, b`.</details>

### A2 `mse`, A3 `r2_score`
<details><summary>Hint 1</summary>`np.mean((y - y_hat) ** 2)`.</details>
<details><summary>Hint 2</summary>`ss_res = np.sum((y - y_hat)**2)`, `ss_tot = np.sum((y - y.mean())**2)`, `return 1 - ss_res/ss_tot`.</details>

### B1 `load_design`
<details><summary>Hint 1</summary>`df = pd.read_csv(path)`, then `pd.get_dummies(df, columns=["neighborhood"], drop_first=True, dtype=int)`.</details>
<details><summary>Hint 2</summary>`X = df[FEATURES].to_numpy(dtype=float)`, `y = df["rent"].to_numpy(dtype=float)`.</details>

### B2 `fit_ols`
<details><summary>Hint 1</summary>`Xb = add_intercept(X)`. The equation is A β = b with A = `Xb.T @ Xb` and b = `Xb.T @ y`.</details>
<details><summary>Hint 2</summary>`return np.linalg.solve(Xb.T @ Xb, Xb.T @ y)`</details>

### B3 `predict`
<details><summary>Hint 1</summary>`add_intercept(X) @ beta`</details>

### B4 `train_test_r2`
<details><summary>Hint 1</summary>`idx = np.random.default_rng(seed).permutation(len(y))`, `n_test = round(test_frac * len(y))`, `te, tr = idx[:n_test], idx[n_test:]`.</details>
<details><summary>Hint 2</summary>numpy arrays can be indexed with an array of positions: `X[tr]`, `y[tr]`.
Fit on `X[tr], y[tr]`; compute `r2_score` on train and on test with that same beta.</details>

### C1 `mse_gradient`
<details><summary>Hint 1</summary>Residual vector: `r = Xb @ beta - y` (shape (n,)).</details>
<details><summary>Hint 2</summary>`return (2 / len(y)) * Xb.T @ r`</details>

### C2 `fit_gd`
<details><summary>Hint 1</summary>`Xb = add_intercept(X)`; `beta = np.zeros(Xb.shape[1])`.</details>
<details><summary>Hint 2</summary>

```python
for _ in range(n_iters):
    beta = beta - lr * mse_gradient(Xb, y, beta)
return beta
```
If it diverges (numbers become `nan`/`inf`), your learning rate is too large or X isn't standardized.
</details>

### D1 `fit_ridge`
<details><summary>Hint 1</summary>Follow the 3 steps in the docstring literally. Identity matrix: `np.eye(d)` with `d = X.shape[1]`.</details>
<details><summary>Hint 2</summary>

```python
xm, ym = X.mean(axis=0), y.mean()
Xc, yc = X - xm, y - ym
b = np.linalg.solve(Xc.T @ Xc + lam * np.eye(X.shape[1]), Xc.T @ yc)
a = ym - xm @ b
return np.concatenate([[a], b])
```
</details>

### D2 `coef_standard_errors`
<details><summary>Hint 1</summary>`Xb = add_intercept(X)`; `n, p = Xb.shape`; get beta with your `fit_ols(X, y)`.</details>
<details><summary>Hint 2</summary>`e = y - Xb @ beta`; `sigma2 = e @ e / (n - p)`; `cov = sigma2 * np.linalg.inv(Xb.T @ Xb)`; `np.sqrt(np.diag(cov))`.</details>

### D3 `duplicate_data_experiment`
<details><summary>Hint 1</summary>`X2 = np.vstack([X, X])`, `y2 = np.concatenate([y, y])`.</details>
<details><summary>Hint 2</summary>Fit both with `fit_ols`; R² with `r2_score(y, predict(X, beta))` (and the same for the doubled data); SEs with `coef_standard_errors`. Return the dict with the 6 keys.</details>
