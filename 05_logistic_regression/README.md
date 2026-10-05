# 05 · Logistic regression (≈ 2 hours)

**Goal:** build logistic regression from scratch, evaluate a classifier the way a professional does (not just accuracy),
and explain the model's probabilistic meaning.

**Dataset:** `data/loan_default.csv`, 400 borrowers, ≈ 25% defaulted.

| income_k | debt_to_income | credit_score | years_employed | late_payments | default |
|---|---|---|---|---|---|
| 44.1 | 0.637 | 690 | 0.7 | 1 | 1 |

## Concept notes

**Model.** We model the probability, not the label:
P(y=1 | x) = σ(β₀ + βᵀx), with σ(z) = 1/(1+e^{−z}).
Equivalently the **log-odds are linear**: log(p/(1−p)) = β₀ + βᵀx.
So a coefficient β_j means: +1 unit of x_j multiplies the **odds** by e^{β_j} (the odds ratio).

**Loss = negative log-likelihood (log-loss / cross-entropy).**
L(β) = −(1/n) Σ [ yᵢ log pᵢ + (1−yᵢ) log(1−pᵢ) ].
It comes from maximum likelihood with yᵢ ~ Bernoulli(pᵢ). It is **convex** in β, so gradient descent finds the global minimum.
Gradient: ∇L = (1/n) Xᵀ(p − y), the same form as linear regression with p in place of Xβ.
(Because σ'(z) = σ(z)(1−σ(z)), this cancels beautifully. Try deriving it once on paper.)

**Why not MSE + linear regression for a 0/1 target?** Predictions leave [0,1]; MSE with a sigmoid is non-convex;
log-loss punishes confident wrong answers heavily, which is what we want.

**Decision boundary:** predict 1 if p ≥ t. At t = 0.5 that's βᵀx + β₀ ≥ 0, a **hyperplane**, so logistic regression is a linear classifier.

**Perfect separation:** if a hyperplane separates the classes perfectly, the likelihood keeps increasing as ‖β‖ → ∞,
so the weights diverge. Regularization (L2) fixes it. sklearn regularizes by default (`C=1.0`, where C = 1/λ).

**Evaluation (positive = default)**
| | predicted 1 | predicted 0 |
|---|---|---|
| actual 1 | TP | FN |
| actual 0 | FP | TN |

- accuracy = (TP+TN)/n is misleading with imbalance: "always predict 0" scores 74% here!
- precision = TP/(TP+FP): of the loans I flagged, how many really defaulted?
- recall = TP/(TP+FN): of the real defaults, how many did I catch?
- F1 = harmonic mean of the two.
- ROC curve = TPR vs FPR over all thresholds; **AUC** = P(score of random positive > score of random negative).
  It is threshold-free, 0.5 = random, 1 = perfect.
- The threshold is a **business decision**: cost(FN = unpaid loan) vs cost(FP = rejected good customer).

## Tasks
| ID | Function | Skill |
|---|---|---|
| A1–A2 | `sigmoid`, `log_loss` | numerical stability |
| B1–B2 | `logistic_gradient`, `fit_logistic` | gradient descent |
| B3–B4 | `predict_proba`, `predict_labels` | |
| C1–C3 | `confusion_counts`, `classification_metrics`, `roc_auc` | evaluation from scratch |
| D1 | `baseline_accuracy` | always compare with a baseline |
| D2 | `odds_ratios` | interpretation |
| D3 | `sklearn_beta` | the library way |

Then run `python solution.py` and look at the threshold table: precision and recall move in opposite directions.

## Interviewer follow-ups

<details><summary>1. Your model has 77% accuracy. Good?</summary>

Compare with the baseline: always predicting "no default" gives 74%. So the model adds only 3 points of accuracy.
Accuracy is the wrong lens for imbalanced data. Look at recall/precision at a sensible threshold, AUC, and log-loss/calibration.
</details>

<details><summary>2. Interpret the credit_score odds ratio ≈ 0.28.</summary>

Features are standardized, so +1 standard deviation of credit score (≈ 60 points) multiplies the odds of default by ≈ 0.28,
a 72% reduction in the odds (not in the probability!). The change in probability depends on where you start, because the sigmoid is non-linear.
</details>

<details><summary>3. Derive the gradient of the log-loss.</summary>

For one sample: ℓ = −[y log σ(z) + (1−y) log(1−σ(z))], z = βᵀx.
dℓ/dz = −[y(1−σ) − (1−y)σ] = σ(z) − y. Chain rule: dℓ/dβ = (σ(z) − y)·x. Average over samples: (1/n)Xᵀ(p − y).
</details>

<details><summary>4. Classes are 1% positive (fraud). What changes?</summary>

Accuracy becomes useless (99% by predicting 0). Use precision-recall curves / PR-AUC, class weights
(`class_weight="balanced"`), resampling (over/under-sampling **only on the training set**), tune the threshold on validation data,
and use stratified splits so the test set contains positives at all.
</details>

<details><summary>5. What does it mean for the probabilities to be "calibrated"? Why do we care in trading/credit?</summary>

Among all cases where the model says 0.3, about 30% should actually be positive. In finance you price risk with the probability itself
(expected loss = PD × LGD × exposure; position sizing ∝ edge), so calibration matters more than ranking alone.
Check with a reliability plot; fix with Platt scaling or isotonic regression.
</details>

<details><summary>6. Logistic regression vs linear regression: what's the same, what's different?</summary>

Both are generalized linear models with a linear predictor βᵀx. Linear: identity link, Gaussian noise, MSE, closed form.
Logistic: logit link, Bernoulli noise, log-loss, no closed form (solved iteratively, by Newton/IRLS or GD), and the output is a probability.
</details>

<details><summary>7. How would you extend it to 3+ classes?</summary>

Softmax (multinomial) regression: p_k = e^{z_k}/Σ_j e^{z_j} with one weight vector per class and cross-entropy loss.
Or one-vs-rest: K binary classifiers.
</details>

<details><summary>8. Why standardize before logistic regression?</summary>

Faster, more stable gradient descent; the L2 penalty treats features fairly; coefficients become comparable ("per std").
The unregularized MLE predictions don't change, because it's just a reparametrization.
</details>
