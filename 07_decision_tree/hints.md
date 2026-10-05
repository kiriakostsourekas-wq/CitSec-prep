# Hints · 07 Decision tree

### A1 `load_split`
<details><summary>Hint 1</summary>`df["contract_months"] = df["contract"].map(CONTRACT_MONTHS)` replaces each string by its number.</details>
<details><summary>Hint 2</summary>The split is identical to folder 05's `prepare_data`, just without scaling.</details>

### A2 `gini`
<details><summary>Hint 1</summary>`np.bincount(y, minlength=2)` counts the zeros and ones: e.g. `[3, 1]`. Divide by `len(y)` to get proportions.</details>
<details><summary>Hint 2</summary>`1 - np.sum(p ** 2)`, and handle `len(y) == 0` first (return 0.0).</details>

### A3 `entropy`
<details><summary>Hint 1</summary>Same proportions as gini; drop the zeros with `p = p[p > 0]` before `np.log2`.</details>

### B1 `weighted_impurity`
<details><summary>Hint 1</summary>`n = len(y_left) + len(y_right)`; return `len(y_left)/n * gini(y_left) + len(y_right)/n * gini(y_right)`.</details>

### B2 `best_threshold`
<details><summary>Hint 1</summary>`values = np.unique(x)` is sorted and distinct. Midpoints: `(values[:-1] + values[1:]) / 2`.</details>
<details><summary>Hint 2</summary>For each candidate `t`: `left = x <= t` (boolean mask), then `weighted_impurity(y[left], y[~left])`. `~` flips a boolean mask.</details>
<details><summary>Hint 3</summary>Keep track of the best with `if score < best_score:` (strict `<`, so the first best wins). Start with `best_t, best_score = None, np.inf`.</details>

### B3 `best_split`
<details><summary>Hint 1</summary>Loop `for j in range(X.shape[1])`, call `best_threshold(X[:, j], y)`. `X[:, j]` is column j.</details>
<details><summary>Hint 2</summary>Start with `best = (None, None, np.inf)` and replace it when a feature's score is strictly lower.</details>

### C1 `build_tree`
<details><summary>Hint 1</summary>Write a helper that makes a leaf:
`{"leaf": True, "prediction": int(np.mean(y) >= 0.5), "n": len(y)}`.</details>
<details><summary>Hint 2</summary>Order of work: (1) check depth / size / purity → leaf. (2) `j, t, score = best_split(X, y)`.
(3) if `j is None or score >= gini(y)` → leaf. (4) otherwise split.</details>
<details><summary>Hint 3</summary>

```python
left = X[:, j] <= t
return {"leaf": False, "feature": j, "threshold": t, "n": len(y),
        "left":  build_tree(X[left],  y[left],  max_depth, min_samples_split, depth + 1),
        "right": build_tree(X[~left], y[~left], max_depth, min_samples_split, depth + 1)}
```
Recursion = the function calls itself on a smaller problem. The stop conditions guarantee it ends.
</details>

### C2 `predict_one`
<details><summary>Hint 1</summary>A `while not node["leaf"]:` loop that replaces `node` by `node["left"]` or `node["right"]`.</details>

### C3 `predict_tree`
<details><summary>Hint 1</summary>`np.array([predict_one(tree, x) for x in X], dtype=int)`</details>

### D1 `depth_experiment`
<details><summary>Hint 1</summary>For each `d`: `tree = build_tree(X_train, y_train, max_depth=d)`; accuracy = `np.mean(predict_tree(tree, X) == y)`.</details>

### D2 `sklearn_tree`
<details><summary>Hint 1</summary>

```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=max_depth, random_state=0).fit(X_train, y_train)
return model.score(X_test, y_test), model.feature_importances_
```
Bonus: `from sklearn.tree import export_text; print(export_text(model, feature_names=FEATURES))`. Does it match your tree?
</details>
