# 04 · Linear regression (≈ 2 hours)

**Goal:** implement linear regression three ways (closed form for 1 feature, normal equations, gradient descent),
evaluate it properly, and be able to answer **every** "what happens if…" question about it.
Linear regression comes up in Citadel interviews more than any other model. Several candidates report
"what happens to the coefficients / R² / t-stats if you duplicate the data?" (that is task D3).

**Dataset:** `data/apartments.csv`, 300 apartments.

| sqm | bedrooms | dist_center_km | age_years | floor | has_balcony | neighborhood | rent |
|---|---|---|---|---|---|---|---|
| 103 | 4 | 6.25 | 34 | 8 | 0 | Suburb | 1766 |

The data was simulated from a known linear model plus noise (see `tools/make_datasets.py`), so you can
check whether your coefficients recover the truth (e.g. ≈ +16 per sqm, ≈ −45 per km from the center).

## Concept notes

**Model:** y = β₀ + β₁x₁ + … + β_d x_d + ε. In matrix form, **y = Xβ + ε** with a column of ones in X for β₀.

**OLS** minimizes ‖y − Xβ‖². Setting the gradient −2Xᵀ(y − Xβ) to zero gives the **normal equations**
XᵀX β = Xᵀy  →  β̂ = (XᵀX)⁻¹Xᵀy. Geometrically, Xβ̂ is the orthogonal projection of y onto the column space of X,
so the residuals are orthogonal to every column (and they sum to 0 when there is an intercept).

**1 feature:** β₁ = Cov(x,y)/Var(x) = ρ·σ_y/σ_x, and β₀ = ȳ − β₁x̄. The line passes through (x̄, ȳ).

**R² = 1 − SS_res/SS_tot**, the fraction of variance explained. In-sample R² **never decreases** when you add a feature
(even pure noise), which is why we use adjusted R² or, better, a test set. Test R² can be negative.
With one feature, R² = ρ².

**Gauss–Markov assumptions** (then OLS is BLUE, the best linear unbiased estimator): linear model, E[ε|X] = 0 (no omitted
confounders), homoskedastic and uncorrelated errors, no perfect multicollinearity. Normality of ε is only needed for
exact t/F tests in small samples.

**Standard errors:** Cov(β̂) = σ²(XᵀX)⁻¹ with σ̂² = RSS/(n − p). t-stat = β̂ / SE.

**Gradient descent:** β ← β − η·∇L with ∇L = (2/n)Xᵀ(Xβ − y). Standardize features first, otherwise one
learning rate can't fit features on very different scales (the loss surface is a long thin valley).
Cost: normal equations O(nd² + d³); GD O(nd) per iteration (better for huge d, or streaming data).

**Regularization**
| | Penalty | Effect | Closed form |
|---|---|---|---|
| Ridge (L2) | λ‖β‖² | shrinks all coefficients smoothly; handles multicollinearity | (XᵀX + λI)⁻¹Xᵀy |
| Lasso (L1) | λ‖β‖₁ | sets some coefficients exactly to 0 (feature selection) | none (coordinate descent) |
Don't penalize the intercept; standardize first so the penalty treats features equally.
Bayesian view: ridge = Gaussian prior on β, lasso = Laplace prior.

**Bias–variance:** expected test error = bias² + variance + irreducible noise. Regularization adds a little bias to remove a lot of variance.

## Tasks
| ID | Function | Skill |
|---|---|---|
| A1–A3 | `simple_fit`, `mse`, `r2_score` | formulas by hand |
| B1 | `load_design` | one-hot + numpy arrays |
| B2–B3 | `fit_ols`, `predict` | normal equations |
| B4 | `train_test_r2` | out-of-sample evaluation |
| C1–C2 | `mse_gradient`, `fit_gd` | gradient descent |
| D1 | `fit_ridge` | regularization |
| D2 | `coef_standard_errors` | inference |
| D3 | `duplicate_data_experiment` | **the Citadel question** |

When all pass, run `python solution.py` and read its output: coefficient table with t-stats, the ridge path,
the duplicate experiment and the sklearn comparison.

## Interviewer follow-ups (these are the real exam)

<details><summary>1. You duplicate every row of the dataset. What happens to β̂, R², SEs, t-stats?</summary>

XᵀX and Xᵀy both double, so β̂ is **unchanged**. R² is unchanged (SS_res and SS_tot both double).
σ̂² is about the same, but (XᵀX)⁻¹ halves, so **SEs shrink by 1/√2 and t-stats grow by √2**. You appear more significant
with zero new information, because the SE formula assumes independent observations. Real-life version: overlapping
returns (e.g. regressing 5-day returns sampled daily) inflate t-stats in the same way. Fix: Newey–West SEs or non-overlapping samples.
</details>

<details><summary>2. Two features are highly correlated (sqm and bedrooms here). Consequences?</summary>

Predictions are still fine, but individual coefficients become unstable with large SEs (XᵀX is near-singular). Signs can
even flip. Each coefficient is "the effect holding the other fixed", which is hard to estimate when they move together.
Diagnose with correlation or the VIF = 1/(1−R²_j). Fixes: drop one, combine them, ridge, PCA. Notice in `solution.py` how ridge
moves weight from sqm to bedrooms as λ grows.
</details>

<details><summary>3. Add a feature of pure random noise. What happens to train R² and test R²?</summary>

Train R² goes up (weakly; it can never go down). Test R² typically goes slightly down (more variance).
That's overfitting in miniature, and why adjusted R² = 1 − (1−R²)(n−1)/(n−p−1) exists.
</details>

<details><summary>4. You regress y on x and get slope b. Now regress x on y. Is the slope 1/b?</summary>

No. Slope(y~x) = ρσ_y/σ_x and slope(x~y) = ρσ_x/σ_y. Their product is ρ², so they are reciprocals only when |ρ| = 1.
</details>

<details><summary>5. How do you interpret the coefficient of neighborhood_Suburb ≈ −211?</summary>

Holding all other features fixed, a Suburb apartment rents for ≈ 211 less than a **Center** apartment (the dropped baseline).
Note it's measured *on top of* distance. Part of the "far from center" effect is already in dist_center_km.
</details>

<details><summary>6. Why not compute β = inv(XᵀX) @ Xᵀy?</summary>

Explicit inversion is slower and numerically less stable (it squares the condition number of X). Use `solve`, or better
QR / SVD (`np.linalg.lstsq`), which works on X directly. If XᵀX is singular (perfect collinearity, d > n), OLS has no unique
solution, and ridge fixes that because XᵀX + λI is always invertible for λ > 0.
</details>

<details><summary>7. Residuals fan out as the prediction grows (heteroskedasticity). Problem?</summary>

β̂ is still unbiased, but the classical SEs are wrong (usually too small). Use robust (White/HC) SEs, model log(y),
or weighted least squares. Very common with prices and volumes.
</details>

<details><summary>8. One extreme outlier in y. Effect? What would you do?</summary>

Squared loss gives outliers a lot of influence, and a single point with high leverage can rotate the line. Check whether it's a data error.
Options: winsorize, Huber loss / robust regression, or minimize absolute error (that estimates the conditional median).
</details>

<details><summary>9. When is linear regression a bad idea?</summary>

Strongly non-linear relationships (add features like x² or log x, or use trees), a binary target (use logistic: linear
predictions leave [0,1]), heavy interactions, d ≫ n without regularization, and strongly dependent observations (time series) if you trust the SEs.
</details>

<details><summary>10. Derive the OLS solution (they may ask you to do it on the whiteboard).</summary>

L(β) = (y − Xβ)ᵀ(y − Xβ) = yᵀy − 2βᵀXᵀy + βᵀXᵀXβ. ∇L = −2Xᵀy + 2XᵀXβ = 0 ⇒ XᵀXβ = Xᵀy.
The Hessian 2XᵀX is positive semi-definite, so this is a minimum (unique if X has full column rank).
</details>
