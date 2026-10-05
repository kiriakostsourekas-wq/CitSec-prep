# ML & statistics: rapid-fire questions (with folded answers)

Use this like flashcards: read the question, **answer out loud in ≤ 60 seconds**, then open the answer.
The model-specific deep questions are in the README "Interviewer follow-ups" of folders 04–07. This file covers the general ones.

---

## A. Core ML concepts

<details><summary>A1. Explain the bias–variance trade-off.</summary>

Expected test error = bias² + variance + irreducible noise. Bias is error from wrong assumptions (a model too simple to capture the truth),
and variance is sensitivity to the particular training sample (a model too flexible, fitting noise). More complexity → lower bias and higher variance.
Regularization, more data, and ensembling (bagging) reduce variance.
</details>

<details><summary>A2. How do you detect and prevent overfitting?</summary>

Detect: train error ≪ validation error, and validation error rises as complexity grows. Prevent: more data, simpler model, regularization (L1/L2, depth limits),
cross-validation for hyper-parameters, early stopping, ensembles, and fewer features (selection informed by validation, not by the test set).
</details>

<details><summary>A3. Train / validation / test: why three sets?</summary>

Train fits parameters, validation chooses hyper-parameters and models, test gives one final unbiased estimate. If you tune on the test set,
it becomes a validation set and your reported score is optimistic. Cross-validation replaces a single validation split when data is small.
</details>

<details><summary>A4. L1 vs L2 regularization: what's the difference and why does L1 give zeros?</summary>

L2 (ridge) penalizes Σβ², which shrinks coefficients smoothly and is good with correlated features. L1 (lasso) penalizes Σ|β|, which sets some coefficients to exactly 0.
Geometrically, the L1 ball has corners on the axes and the loss contours usually touch it there. Algebraically, the L1 subgradient at 0 is an interval,
so 0 is optimal whenever |gradient of the loss| < λ. Elastic net combines both.
</details>

<details><summary>A5. Gradient descent vs stochastic gradient descent vs mini-batch?</summary>

GD uses all n samples per step (accurate, expensive). SGD uses 1 sample (cheap, noisy, and the noise can help escape bad regions). Mini-batch (e.g. 32–512) is the
usual compromise and is vectorizable. Learning rate too high → divergence; too low → slow. Adam and momentum adapt the step.
</details>

<details><summary>A6. Why scale features? Which models need it?</summary>

Needed when the algorithm uses distances or a shared penalty/learning rate: kNN, k-means, SVM, PCA, regularized linear/logistic regression, neural nets.
Not needed for trees and tree ensembles (only the order of values matters). Always fit the scaler on train only.
</details>

<details><summary>A7. What is data leakage? Give 3 examples.</summary>

Information that won't be available at prediction time leaks into training. (1) Scaling or imputing with full-data statistics. (2) Random splits on time series.
(3) A feature computed after the outcome (e.g. "account closed date" to predict churn). (4) Survivorship bias. (5) Duplicates spread across train and test.
</details>

<details><summary>A8. Precision vs recall: give a case where each matters more.</summary>

Precision: spam filter (a false positive hides a real email) or a trading signal where each false trade costs money.
Recall: cancer screening, fraud detection (missing a positive is costly). F1 balances both. Choose the threshold from the cost of each error type.
</details>

<details><summary>A9. What does ROC-AUC measure? When is PR-AUC better?</summary>

AUC = P(a random positive is scored above a random negative), which measures ranking quality and is threshold-free. With heavy imbalance (1% positives), ROC-AUC can look great
while precision is terrible, because FPR divides by the huge number of negatives. PR-AUC focuses on the positive class.
</details>

<details><summary>A10. Random forest vs gradient boosting vs single tree?</summary>

Single tree: interpretable, high variance. RF: averages many deep trees on bootstrap samples with random feature subsets, which reduces variance and is robust.
Boosting: shallow trees added sequentially to fix residuals, which reduces bias, is usually the most accurate on tabular data, and is more sensitive to tuning and noise.
</details>

<details><summary>A11. What is PCA, in one minute?</summary>

Find orthogonal directions of maximum variance: the eigenvectors of the covariance matrix (equivalently, the SVD of centered X). Project onto the top k to reduce
dimension while keeping most variance. Unsupervised: the top variance directions are not necessarily predictive of y. Scale features first. In finance,
the first PC of stock returns is roughly "the market".
</details>

<details><summary>A12. How would you handle a dataset with 1000 features and 200 samples?</summary>

d > n means OLS is not identifiable and overfitting is guaranteed. Use strong regularization (lasso/ridge/elastic net), dimension reduction (PCA), feature selection inside CV,
simple models, and domain knowledge to cut features. Be suspicious of any great in-sample result.
</details>

<details><summary>A13. Parametric vs non-parametric models?</summary>

Parametric: a fixed number of parameters regardless of n (linear/logistic regression), with strong assumptions and data efficiency. Non-parametric: complexity grows with data
(kNN, trees, kernel methods), flexible, needs more data.
</details>

<details><summary>A14. Your model has 99% test accuracy. What do you check?</summary>

Class balance (baseline accuracy), leakage (features that encode the label, duplicates across splits, time leakage), whether the test set is representative,
and other metrics (confusion matrix, recall on the minority class). "Too good to be true" usually is, especially in finance.
</details>

## B. Statistics

<details><summary>B1. Var(X + Y)? Var(aX)? Var of the sample mean?</summary>

Var(X+Y) = Var X + Var Y + 2Cov(X,Y). Var(aX) = a²Var X. Var(X̄) = σ²/n for i.i.d. samples, so the standard error is σ/√n.
With correlation ρ between all pairs: Var(X̄) = σ²(1/n + ρ(1 − 1/n)), which tends to ρσ² and doesn't go to 0. That's why diversification has limits.
</details>

<details><summary>B2. Two unbiased forecasts with variances σ₁², σ₂² and covariance σ₁₂. Best linear combination?</summary>

Minimize Var(w f₁ + (1−w) f₂): w* = (σ₂² − σ₁₂) / (σ₁² + σ₂² − 2σ₁₂). If they're uncorrelated, w* ∝ 1/σ₁² (inverse-variance weighting) and the combined variance is lower than either alone.
(A version of this, "combine predictors to minimize the error", is reported for Citadel.)
</details>

<details><summary>B3. Central Limit Theorem: statement and why it matters.</summary>

The standardized sum/mean of i.i.d. variables with finite variance converges in distribution to N(0,1). It justifies normal-based confidence intervals and t-tests for means
even when the data isn't normal. Caveats: heavy tails (infinite variance → fails), dependence, small n.
</details>

<details><summary>B4. What is a p-value? What is it NOT?</summary>

P(data at least this extreme | H₀ true). It is NOT P(H₀ true | data), and it is not the probability that the result is due to chance. With 100 tests at 5%, about 5 are "significant" by luck
(multiple testing → Bonferroni, FDR, or a held-out sample). Very relevant to signal research: test 1000 signals and the best one looks great.
</details>

<details><summary>B5. Type I vs Type II error, power?</summary>

Type I: reject a true H₀ (false positive, rate α). Type II: fail to reject a false H₀ (false negative, rate β). Power = 1 − β, which grows with sample size and effect size.
</details>

<details><summary>B6. MLE: what is it, and how does it connect to OLS and logistic regression?</summary>

Choose the parameters maximizing the likelihood of the observed data. Linear model with Gaussian noise → maximizing the likelihood = minimizing squared error, so OLS = MLE.
Bernoulli outcomes with p = σ(βᵀx) → the negative log-likelihood is the log-loss.
</details>

<details><summary>B7. Correlation 0 means independent?</summary>

No. Correlation measures linear dependence only. Example: X ~ N(0,1), Y = X² gives corr = 0, yet Y is a function of X. (Independence ⇒ zero correlation, not the converse,
except for jointly Gaussian variables.)
</details>

<details><summary>B8. Confidence interval: what does "95%" mean?</summary>

If you repeated the experiment many times, 95% of the intervals constructed this way would contain the true parameter. It is not "95% probability the parameter is in this particular interval"
(that's a Bayesian credible interval).
</details>

<details><summary>B9. How would you test whether a trading strategy's mean return is > 0?</summary>

t-stat = mean / (std/√n), roughly Sharpe_per_period × √n. Issues: returns are autocorrelated and heavy-tailed (use Newey–West or the bootstrap), non-stationary,
and above all multiple testing / data snooping (deflated Sharpe ratio, out-of-sample period, walk-forward). Also check transaction costs and capacity.
</details>

<details><summary>B10. Correlation vs causation: how could you establish causation?</summary>

Randomized experiments (A/B tests) are the gold standard. Observational: control for confounders, natural experiments, instrumental variables, difference-in-differences.
Always ask about confounders (ice-cream sales vs drownings → summer).
</details>

## C. Finance-flavoured ML

<details><summary>C1. Why is ML on financial returns harder than on images?</summary>

Very low signal-to-noise (R² of 1% can be valuable), non-stationarity (regimes change, relationships decay once traded on), small effective sample sizes,
adversarial and reflexive markets, heavy tails, and costs that eat small edges. Hence: simple models, strong regularization, rigorous out-of-sample testing.
</details>

<details><summary>C2. How do you cross-validate a model on time-series data?</summary>

Walk-forward / expanding window: train on [0, t], test on (t, t+h], move t forward. Add a gap (purging/embargo) when labels overlap in time (e.g. 5-day forward returns) so
training labels don't overlap test labels. Never shuffle.
</details>

<details><summary>C3. Your backtest Sharpe is 3. List what could be wrong.</summary>

Look-ahead bias (using data not available at the time, e.g. close price to trade at the close, restated fundamentals), survivorship bias, overfitting / multiple testing,
no or unrealistic transaction costs and slippage, unrealistic fills (trading at the mid, ignoring capacity and market impact), short-sale constraints, too short a sample,
a single lucky regime, and data errors.
</details>
