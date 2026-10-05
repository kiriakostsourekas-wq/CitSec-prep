# ML & stats formula sheet (one page)

## Linear regression
| | |
|---|---|
| model | y = Xβ + ε (X has a column of ones) |
| OLS | β̂ = (XᵀX)⁻¹Xᵀy (solve XᵀXβ = Xᵀy) |
| 1 feature | β₁ = Cov(x,y)/Var(x) = ρ σ_y/σ_x, β₀ = ȳ − β₁x̄ |
| MSE gradient | ∇ = (2/n) Xᵀ(Xβ − y) |
| ridge | β̂ = (XᵀX + λI)⁻¹Xᵀy (don't penalize the intercept) |
| lasso | min ‖y − Xβ‖² + λ‖β‖₁ (no closed form) |
| R² | 1 − SS_res/SS_tot; with 1 feature R² = ρ² |
| adjusted R² | 1 − (1−R²)(n−1)/(n−p−1) |
| σ̂² | RSS/(n − p), p = number of columns incl. intercept |
| Cov(β̂) | σ̂²(XᵀX)⁻¹; SE = sqrt(diagonal); t = β̂/SE |
| VIF_j | 1/(1 − R²_j), where R²_j regresses x_j on the other features |

## Logistic regression
| | |
|---|---|
| model | p = σ(z) = 1/(1+e^{−z}), z = β₀ + βᵀx |
| log-odds | log(p/(1−p)) = z; odds ratio per unit = e^{β_j} |
| σ' | σ(z)(1 − σ(z)) |
| log-loss | −(1/n) Σ [y log p + (1−y) log(1−p)] |
| gradient | (1/n) Xᵀ(p − y) |
| softmax | p_k = e^{z_k}/Σ_j e^{z_j} |

## Classification metrics
accuracy = (TP+TN)/n · precision = TP/(TP+FP) · recall = TPR = TP/(TP+FN) · FPR = FP/(FP+TN) · specificity = 1 − FPR
F1 = 2PR/(P+R) · AUC = P(score⁺ > score⁻)

## Trees & kNN
Gini = 1 − Σ p_k² · entropy = −Σ p_k log₂ p_k · split score = (n_L/n)I_L + (n_R/n)I_R · regression tree impurity = variance
kNN: majority vote of the k nearest (scaled!) neighbours; k↑ → bias↑, variance↓

## Naive Bayes
P(c|x) ∝ P(c) Π_j P(x_j|c); Gaussian: log N(x; μ, σ²) = −½ log(2πσ²) − (x−μ)²/(2σ²)

## Bias–variance
E[(y − f̂(x))²] = Bias[f̂]² + Var[f̂] + σ²_noise

## Probability & statistics
| | |
|---|---|
| Bayes | P(A\|B) = P(B\|A)P(A)/P(B) |
| total probability | P(B) = Σ P(B\|A_i)P(A_i) |
| total expectation | E[X] = E[E[X\|Y]] |
| variance | Var X = E[X²] − (E X)²; Var(aX+bY) = a²VarX + b²VarY + 2ab Cov |
| sample mean | E[X̄] = μ, Var(X̄) = σ²/n, SE = σ/√n |
| sample variance | s² = Σ(x − x̄)²/(n − 1) (unbiased) |
| correlation | ρ = Cov(X,Y)/(σ_X σ_Y) ∈ [−1, 1] |
| 95% CI for a mean | x̄ ± 1.96 s/√n |
| geometric (success p) | E = 1/p, Var = (1−p)/p² |
| binomial(n,p) | E = np, Var = np(1−p) |
| Poisson(λ) | E = Var = λ |
| exponential(λ) | E = 1/λ, memoryless |
| uniform(0,1) | E = 1/2, Var = 1/12; E[max of n] = n/(n+1) |
| coupon collector | n H_n = n(1 + 1/2 + … + 1/n) |
| gambler's ruin (fair) | P(hit b before 0 from a) = a/b; E[time to hit −a or +b] = ab |
| optimal combination of 2 forecasts | w* = (σ₂² − σ₁₂)/(σ₁² + σ₂² − 2σ₁₂) |

## Finance
simple return r = P_t/P_{t−1} − 1 · log return = ln(P_t/P_{t−1}) · Sharpe = mean(r)/std(r)·√252 (rf = 0)
SE(annualized Sharpe from Y years of daily data) ≈ 1/√Y · max drawdown = min_t (P_t / max_{s≤t} P_s − 1)
VWAP = Σ p·q / Σ q · portfolio variance = wᵀΣw
