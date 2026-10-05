# Hints · 06 kNN

### A1 `euclidean`
<details><summary>Hint 1</summary>`np.sqrt(np.sum((a - b) ** 2))`, or `np.linalg.norm(a - b)`.</details>

### A2 `knn_predict_one`
<details><summary>Hint 1</summary>Distances to all rows at once: `np.sqrt(((X_train - x) ** 2).sum(axis=1))` (same as folder 02, A5).</details>
<details><summary>Hint 2</summary>`np.argsort(dists)` returns the positions that would sort the array. Take the first k: `[:k]`.
Their labels: `y_train[nearest]`.</details>
<details><summary>Hint 3</summary>

```python
nearest = np.argsort(dists, kind="stable")[:k]
return Counter(y_train[nearest]).most_common(1)[0][0]
```
`most_common(1)` returns a list like `[("apple", 3)]`, hence the `[0][0]`.
</details>

### A3 `knn_predict`
<details><summary>Hint 1</summary>A list comprehension over the rows of X_test, wrapped in `np.array(...)`.</details>

### B1 `accuracy`
<details><summary>Hint 1</summary>`y == y_hat` is a boolean array, and its mean is the fraction of True values.</details>

### B2 `scale_train_test`
<details><summary>Hint 1</summary>`mu, sd = X_train.mean(axis=0), X_train.std(axis=0)`, then apply the same mu and sd to both arrays.</details>

### B3 `scaling_experiment`
<details><summary>Hint 1</summary>Call `knn_predict` twice: once with raw arrays, once with the output of `scale_train_test`. Compute `accuracy` for both.</details>

### C1 `cross_val_accuracy`
<details><summary>Hint 1</summary>`folds = np.array_split(np.arange(len(y)), n_folds)` gives a list of index arrays.</details>
<details><summary>Hint 2</summary>For a fold `val_idx`, the training rows are all the others. A boolean mask is easiest:
```python
train_mask = np.ones(len(y), dtype=bool)
train_mask[val_idx] = False
```
</details>
<details><summary>Hint 3</summary>Predict `X[val_idx]` using `X[train_mask], y[train_mask]`, append the accuracy to a list, return `np.mean(list)`.</details>

### C2 `best_k`
<details><summary>Hint 1</summary>Compute a dict `{k: cross_val_accuracy(X, y, k, n_folds) for k in ks}`.</details>
<details><summary>Hint 2</summary>`max(ks, key=lambda k: scores[k])` returns the first k with the highest score.</details>

### C3 `confusion_matrix`
<details><summary>Hint 1</summary>Map label → row/column number: `pos = {lab: i for i, lab in enumerate(labels)}`.</details>
<details><summary>Hint 2</summary>Start with `M = np.zeros((K, K), dtype=int)`, loop over `zip(y, y_hat)`, and do `M[pos[t], pos[p]] += 1`.</details>

### D1 `sklearn_knn_accuracy`
<details><summary>Hint 1</summary>

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
return model.fit(X_train, y_train).score(X_test, y_test)
```
</details>

### D2 `fit_gaussian_nb`
<details><summary>Hint 1</summary>Loop over `np.unique(y)`; `Xc = X[y == c]`.</details>
<details><summary>Hint 2</summary>`{"prior": len(Xc) / len(X), "mean": Xc.mean(axis=0), "var": Xc.var(axis=0)}`</details>

### D3 `predict_gaussian_nb`
<details><summary>Hint 1</summary>For each class, compute a vector of scores for **all rows at once** (shape (n,)) using broadcasting `(X - m) ** 2 / (2 * v)`, then `.sum(axis=1)`.</details>
<details><summary>Hint 2</summary>Stack the per-class score vectors into an (n, K) array with `np.column_stack`, then use `argmax(axis=1)` to get the index of the best class, and
`np.array(classes)[best_idx]` to convert it to labels.</details>
