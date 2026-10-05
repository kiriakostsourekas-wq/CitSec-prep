# 07 · Decision tree from scratch (≈ 2–2.5 hours)

**Goal:** implement a classification tree (CART with Gini) yourself, watch it **recover the hidden rule** in the data,
and see overfitting happen as depth grows. This is the most "algorithmic" ML exercise in the folder
(recursion, scanning thresholds), close to what a coding interviewer would ask.

**Dataset:** `data/churn.csv`, 320 customers, ≈ 27% churn.

| tenure_months | contract | monthly_charges | support_calls | churn |
|---|---|---|---|---|
| 37 | month-to-month | 79.06 | 1 | 0 |

The data was generated from an if/else rule with an **AND interaction** plus 7% random label noise (see
`tools/make_datasets.py`; try not to peek until your tree has found it).

## Concept notes

**How a tree is grown (greedy, top-down):**
```
build(node data, depth):
    if stop condition: return leaf(majority class)
    for every feature j, for every threshold t:
        score = weighted impurity of children {x_j <= t} and {x_j > t}
    pick the (j, t) with the lowest score
    return {split on (j,t), left: build(left data), right: build(right data)}
```
Greedy means it picks the best split *now*; finding the globally optimal tree is NP-hard.

**Impurity** (p_k = class proportions in the node):
- Gini = 1 − Σ p_k² (probability that two random samples from the node have different labels). Max 0.5 for 2 classes.
- Entropy = −Σ p_k log₂ p_k. Max 1 bit for 2 classes. *Information gain* = parent entropy − weighted child entropy.
- In practice they give almost the same trees. Gini is a bit cheaper (no log).
- For regression trees: impurity = variance (MSE) of y in the node, and a leaf predicts the mean.

**Candidate thresholds:** midpoints between consecutive distinct sorted values. Anything between two values gives the same split.

**Stopping / regularization ("pre-pruning"):** `max_depth`, `min_samples_split`, `min_samples_leaf`, minimum impurity decrease.
Post-pruning (cost-complexity, `ccp_alpha`) grows a full tree and then cuts weak branches back.

**Properties**
- ✅ No scaling needed (splits only depend on the order of values). Handles non-linearity and **interactions** automatically. Easy to interpret.
- ❌ High variance: a small change in the data can give a totally different tree. Axis-aligned, step-shaped boundaries. Overfits easily.
- Fix for the variance: **ensembles**. *Random forest* = many deep trees on bootstrap samples + random feature subsets, averaged (reduces variance).
  *Gradient boosting* = many shallow trees, each fitting the residual errors of the previous ones (reduces bias). You don't need to implement these,
  but know this one-line description of each.

**Feature importance (sklearn):** total impurity decrease contributed by each feature, weighted by node size. It is biased towards
features with many distinct values; permutation importance on a validation set is more reliable.

## Tasks
| ID | Function | Skill |
|---|---|---|
| A1 | `load_split` | `.map`, split |
| A2–A3 | `gini`, `entropy` | `np.bincount` |
| B1 | `weighted_impurity` | |
| B2 | `best_threshold` | scan midpoints for one feature |
| B3 | `best_split` | loop over features |
| C1 | `build_tree` | **recursion** + stopping rules |
| C2–C3 | `predict_one`, `predict_tree` | tree traversal |
| D1 | `depth_experiment` | the overfitting curve |
| D2 | `sklearn_tree` | the library way |

Use the given `print_tree(tree)` constantly while debugging. Then run `python solution.py`, which also compares with
logistic regression (worse here, because of the interaction) and a random forest.

## Interviewer follow-ups

<details><summary>1. Train accuracy hits 100% at depth 8 but test accuracy drops. Explain.</summary>

Deep trees keep splitting until every leaf is pure, so they memorize the 7% label noise. That is low bias and very high variance.
The test accuracy peaks at a moderate depth (≈3 here, matching the true rule's complexity). Choose depth by cross-validation.
</details>

<details><summary>2. Why can't logistic regression capture this rule well, and how could you help it?</summary>

The rule is "(month-to-month AND tenure < 24) OR (calls ≥ 3 AND charges > 70)". Logistic regression is linear in the features, so it can't express
AND/thresholds. You could engineer features by hand (indicator `tenure < 24`, the product `is_mtm × short_tenure`, …). Trees find them automatically.
</details>

<details><summary>3. Complexity of finding the best split? How do libraries make it fast?</summary>

Naively: for each of d features, ~n thresholds, each needing O(n) to compute the impurity, so O(d·n²) per node.
Smarter: sort each feature once (O(n log n)), then sweep left→right, updating class counts incrementally, so each threshold is O(1).
Histogram methods (LightGBM, XGBoost "hist") bucket values into ~256 bins for O(n) per feature.
</details>

<details><summary>4. Your tree split a node into two leaves that predict the same class. Is that a bug?</summary>

No. Gini decreased (one child got purer), so the split is "useful" for impurity even though accuracy is unchanged. The probabilities
in the leaves differ. Pruning would usually remove such splits. You can see this in the depth-3 tree in `solution.py`.
</details>

<details><summary>5. Gini vs entropy vs misclassification error as the split criterion?</summary>

Gini and entropy are strictly concave, so they reward splits that make children purer even when the majority class doesn't change.
Misclassification error is piecewise linear and often can't see any improvement, so greedy growth stalls. That's why it's not used for growing.
</details>

<details><summary>6. How does a tree handle a categorical feature like "contract"?</summary>

Here we mapped it to an ordered number (1, 12, 24 months), which works because the categories are naturally ordered.
For unordered categories: one-hot encoding, or (in CART for binary targets) sort the categories by their churn rate and split
as if ordered, which is provably optimal for Gini.
</details>

<details><summary>7. Random forest vs gradient boosting in one sentence each?</summary>

RF: average many decorrelated deep trees (bagging + random feature subsets), which reduces variance, is hard to overfit, and needs little tuning.
GBM: add shallow trees sequentially, each fitting the gradient of the loss (the residuals), which reduces bias, is usually the most accurate on tabular data, and needs careful tuning (learning rate, number of trees, early stopping).
</details>
