# 06 · k-nearest neighbours (+ bonus Naive Bayes) (≈ 1–1.5 hours)

**Goal:** a second classifier that works completely differently from logistic regression: it is non-parametric, makes no
assumption about the shape of the boundary, and needs no training. Along the way you'll see the most convincing demo
of **why feature scaling matters** (accuracy jumps from ~35% to ~90%) and write cross-validation by hand.

**Dataset:** `data/fruits.csv`, 180 fruits, 3 balanced classes.

| weight_g | width_cm | height_cm | color_score | fruit |
|---|---|---|---|---|
| 179 | 7.06 | 6.81 | 0.826 | apple |

Look at the playground output first: `weight_g` has a huge spread but is nearly the same across fruits;
`color_score` is tiny in magnitude but separates them very well.

## Concept notes

**kNN algorithm** (to classify x):
1. compute the distance from x to every training point
2. take the k nearest
3. majority vote (regression version: average their y)

- **k small** → very flexible, low bias, high variance (k = 1 memorizes the training set: training accuracy = 100%).
- **k large** → smooth, high bias (k = n always predicts the majority class).
- Choose k by **cross-validation**, never on the test set.
- Distances need **scaled features**; otherwise the feature with the largest units dominates.
- **Curse of dimensionality:** in high dimensions all points are almost equally far apart, so "nearest" loses meaning.
- Cost: no training, but O(n·d) per prediction and you must store all the data.

**k-fold cross-validation**
```
data → split into K folds
for each fold i:  train on the other K−1 folds, evaluate on fold i
score = average of the K evaluations
```
It uses every point for validation exactly once, so it's less noisy than a single split. The test set stays untouched
until the very end. For time series use **walk-forward** (expanding window) instead of random folds.

**Gaussian Naive Bayes (bonus)**: a *generative* classifier. Bayes' rule
P(c | x) ∝ P(c) · P(x | c), with the "naive" assumption that the features are independent given the class:
P(x | c) = Π_j N(x_j; μ_cj, σ²_cj). Work with logs to avoid underflow.
It's fast, needs little data, and doesn't care about scaling. Here it wins because the data really *is* Gaussian
with independent features (see `tools/make_datasets.py`); it struggles when features are strongly correlated.

| | Logistic regression | kNN | Naive Bayes |
|---|---|---|---|
| type | discriminative, parametric | non-parametric, "lazy" | generative, parametric |
| boundary | linear | any shape | quadratic (Gaussian) |
| needs scaling | yes (for GD/regularization) | **yes, critical** | no |
| training cost | iterative | none | one pass |
| prediction cost | O(d) | O(n·d) | O(K·d) |

## Tasks
| ID | Function | Skill |
|---|---|---|
| A1–A3 | `euclidean`, `knn_predict_one`, `knn_predict` | argsort, Counter |
| B1–B3 | `accuracy`, `scale_train_test`, `scaling_experiment` | the scaling lesson |
| C1–C2 | `cross_val_accuracy`, `best_k` | K-fold CV by hand |
| C3 | `confusion_matrix` | multi-class evaluation |
| D1 | `sklearn_knn_accuracy` | `Pipeline` (scaler is fitted inside!) |
| D2–D3 | `fit_gaussian_nb`, `predict_gaussian_nb` | **bonus**, if you have time |

## Interviewer follow-ups

<details><summary>1. What's the training error of 1-NN? Is that good?</summary>

0% (each point is its own nearest neighbour), assuming no duplicate points with different labels. It says nothing about generalization:
it is pure memorization. That's why you evaluate on held-out data.
</details>

<details><summary>2. How does kNN behave as k goes from 1 to n?</summary>

Variance falls and bias rises. k = 1 gives a jagged boundary that follows the noise. k = n gives a constant prediction (the majority class).
The CV curve is usually U-shaped in error, which you can see in `python solution.py`.
</details>

<details><summary>3. Why use a Pipeline in sklearn?</summary>

So that `fit` learns the scaler's mean/std on the training data only, and cross-validation (`cross_val_score`) refits the scaler
inside each fold. Scaling the whole dataset first and then cross-validating leaks information from the validation folds.
</details>

<details><summary>4. You have 10 million rows and need fast predictions. What do you do?</summary>

Use spatial indexes (KD-tree, ball tree) when d is small, approximate nearest neighbour (LSH, HNSW / FAISS) when d is large,
reduce dimension (PCA), or switch to a parametric model that is cheap at prediction time.
</details>

<details><summary>5. Why is Naive Bayes "naive" and why does it still work?</summary>

It assumes conditional independence of the features, which is rarely true. The probabilities it outputs are often badly calibrated
(overconfident), but classification only needs the **argmax** to be right, and that is surprisingly robust. Classic use: spam filtering on word counts.
</details>

<details><summary>6. Generative vs discriminative?</summary>

Generative models P(x, y) = P(y)P(x|y) (Naive Bayes, LDA) and can generate data. Discriminative models P(y|x) directly
(logistic regression). With lots of data, discriminative models usually win. With little data, generative ones often win because their stronger assumptions act as regularization.
</details>
