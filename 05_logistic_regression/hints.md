# Hints · 05 Logistic regression

### A1 `sigmoid`
<details><summary>Hint 1</summary>`1 / (1 + np.exp(-z))` works element-wise on arrays.</details>
<details><summary>Hint 2</summary>For huge |z|, `np.exp` overflows. Clip first: `z = np.clip(z, -500, 500)`.</details>

### A2 `log_loss`
<details><summary>Hint 1</summary>`p = np.clip(p, eps, 1 - eps)` before any `np.log`.</details>
<details><summary>Hint 2</summary>`-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))`</details>

### B1 `logistic_gradient`
<details><summary>Hint 1</summary>`p = sigmoid(Xb @ beta)`. Then the formula is one line.</details>
<details><summary>Hint 2</summary>`return Xb.T @ (p - y) / len(y)`</details>

### B2 `fit_logistic`
<details><summary>Hint 1</summary>Copy the structure of `fit_gd` from folder 04: intercept column, zeros, loop.</details>
<details><summary>Hint 2</summary>

```python
Xb = add_intercept(X)
beta = np.zeros(Xb.shape[1])
for _ in range(n_iters):
    beta = beta - lr * logistic_gradient(Xb, y, beta)
return beta
```
</details>

### B3 / B4
<details><summary>Hint 1</summary>`predict_proba` = `sigmoid(add_intercept(X) @ beta)`.</details>
<details><summary>Hint 2</summary>`(predict_proba(X, beta) >= threshold).astype(int)`</details>

### C1 `confusion_counts`
<details><summary>Hint 1</summary>TP = positions where y is 1 AND y_hat is 1: `np.sum((y == 1) & (y_hat == 1))`.</details>
<details><summary>Hint 2</summary>Wrap with `int(...)` so you return plain Python ints.</details>

### C2 `classification_metrics`
<details><summary>Hint 1</summary>Call `confusion_counts` first and unpack the four numbers.</details>
<details><summary>Hint 2</summary>Guard divisions: `precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0`. Same for recall and f1.</details>

### C3 `roc_auc`
<details><summary>Hint 1</summary>`pos = p[y == 1]`, `neg = p[y == 0]`.</details>
<details><summary>Hint 2</summary>`pos[:, None] > neg[None, :]` is a (n_pos, n_neg) boolean table. `.sum()` counts the pairs where the positive wins.
Do the same with `==` for ties.</details>
<details><summary>Hint 3</summary>`(greater + 0.5 * ties) / (len(pos) * len(neg))`</details>

### D1 `baseline_accuracy`
<details><summary>Hint 1</summary>The mean of a 0/1 array is the fraction of ones. Return the larger of rate and 1 − rate.</details>

### D2 `odds_ratios`
<details><summary>Hint 1</summary>Skip the intercept: weights are `beta[1:]`. `zip(feature_names, beta[1:])`.</details>
<details><summary>Hint 2</summary>`{name: float(np.exp(w)) for name, w in zip(feature_names, beta[1:])}`</details>

### D3 `sklearn_beta`
<details><summary>Hint 1</summary>

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1e6, max_iter=5000).fit(X, y)
```
</details>
<details><summary>Hint 2</summary>`model.intercept_` is an array of length 1; `model.coef_` has shape (1, d). `np.concatenate([model.intercept_, model.coef_[0]])`.</details>
