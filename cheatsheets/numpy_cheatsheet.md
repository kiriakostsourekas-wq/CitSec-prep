# numpy cheatsheet (offline)

`import numpy as np` · docs offline: `help(np.argsort)`, or `python -m pydoc -b`

## Creating arrays
```python
np.array([1, 2, 3])            # from a list
np.zeros(5), np.ones((3, 2)), np.full(4, 7.0), np.eye(3)
np.arange(0, 10, 2)            # [0 2 4 6 8]
np.linspace(0, 1, 5)           # [0. .25 .5 .75 1.]
a.shape, a.ndim, a.dtype, len(a)
a.reshape(2, 3), a.ravel(), a.T     # transpose
a.astype(float)
```

## Random (modern API)
```python
rng = np.random.default_rng(42)     # reproducible
rng.random(5)                       # uniform [0,1)
rng.normal(0, 1, size=(3, 2))
rng.integers(1, 7, size=10)         # 1..6 (high is EXCLUSIVE)
rng.choice(arr, size=5, replace=True)
rng.permutation(10)                 # shuffled 0..9
```

## Indexing
```python
a[0], a[-1], a[2:5], a[::-1]
X[i, j], X[i], X[:, j]          # element, row i, column j
X[:, [0, 2]]                    # columns 0 and 2
a[a > 0]                        # boolean mask
a[(a > 0) & (a < 5)]            # combine with & | ~ and BRACKETS
X[idx]                          # rows by an array of positions
np.where(a > 0, a, 0)           # element-wise if/else
```

## Math (vectorized: no loops!)
```python
a + b, a * b, a / b, a ** 2       # element-wise
np.exp(a), np.log(a), np.sqrt(a), np.abs(a), np.clip(a, 0, 1)
A @ B                              # matrix multiplication (also np.dot)
a @ b                              # dot product of 1-D arrays
```

## Aggregations & axis
```python
a.sum(), a.mean(), a.std(), a.var(), a.min(), a.max()
a.std(ddof=1)                      # SAMPLE std (numpy default is ddof=0!)
X.mean(axis=0)                     # one value per COLUMN  -> shape (d,)
X.sum(axis=1)                      # one value per ROW     -> shape (n,)
a.argmax(), a.argmin()             # position of max/min
np.argsort(a)                      # positions that would sort a
np.sort(a), np.unique(a), np.unique(a, return_counts=True)
np.cumsum(a), np.cumprod(a), np.diff(a)
np.maximum.accumulate(a)           # running max
np.quantile(a, [0.025, 0.975]), np.median(a), np.percentile(a, 90)
np.bincount([0, 1, 1, 0, 1])       # [2 3] counts of each integer
np.corrcoef(x, y)[0, 1], np.cov(x, y)
```

## Broadcasting
Shapes are compared from the right; a dimension of 1 (or a missing one) is stretched.
```python
X - X.mean(axis=0)           # (n,d) - (d,)  -> subtract column means from every row
(X - mu) / sd                # standardize
pos[:, None] > neg[None, :]  # (n_pos,1) vs (1,n_neg) -> (n_pos, n_neg) table
```

## Stacking
```python
np.column_stack([np.ones(n), X])   # add an intercept column
np.hstack([A, B]), np.vstack([A, B]), np.concatenate([a, b])
```

## Linear algebra
```python
np.linalg.solve(A, b)              # solve A x = b  (prefer over inv)
np.linalg.inv(A), np.linalg.det(A)
np.linalg.lstsq(X, y, rcond=None)[0]   # least squares
np.linalg.norm(v), np.linalg.norm(X - p, axis=1)
np.linalg.eigh(S)                  # eigen-decomposition of a symmetric matrix
U, s, Vt = np.linalg.svd(X, full_matrices=False)
```

## Checks
```python
np.isnan(a).any(), np.isfinite(a).all()
np.allclose(a, b)                  # compare floats
np.array_split(np.arange(10), 3)   # [0..3], [4..6], [7..9]  (for k-fold CV)
```
