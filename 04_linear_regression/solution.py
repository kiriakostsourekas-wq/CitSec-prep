"""
04 - LINEAR REGRESSION - REFERENCE SOLUTION
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "apartments.csv"
FEATURES = ["sqm", "bedrooms", "dist_center_km", "age_years", "floor", "has_balcony",
            "neighborhood_Riverside", "neighborhood_Suburb"]


def add_intercept(X):
    return np.column_stack([np.ones(len(X)), X])


# ======================= PART A =======================
def simple_fit(x, y):
    x_bar, y_bar = x.mean(), y.mean()
    b = np.sum((x - x_bar) * (y - y_bar)) / np.sum((x - x_bar) ** 2)   # cov / var
    a = y_bar - b * x_bar             # the fitted line always passes through (x_bar, y_bar)
    return a, b


def mse(y, y_hat):
    return np.mean((y - y_hat) ** 2)


def r2_score(y, y_hat):
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return 1 - ss_res / ss_tot


# ======================= PART B =======================
def load_design(path=DATA):
    df = pd.read_csv(path)
    df = pd.get_dummies(df, columns=["neighborhood"], drop_first=True, dtype=int)
    return df[FEATURES].to_numpy(dtype=float), df["rent"].to_numpy(dtype=float)


def fit_ols(X, y):
    Xb = add_intercept(X)
    return np.linalg.solve(Xb.T @ Xb, Xb.T @ y)
    # Even more stable (uses QR/SVD): np.linalg.lstsq(Xb, y, rcond=None)[0]


def predict(X, beta):
    return add_intercept(X) @ beta        # = beta[0] + X @ beta[1:]


def train_test_r2(X, y, test_frac=0.2, seed=0):
    idx = np.random.default_rng(seed).permutation(len(y))
    n_test = round(test_frac * len(y))
    te, tr = idx[:n_test], idx[n_test:]
    beta = fit_ols(X[tr], y[tr])
    return r2_score(y[tr], predict(X[tr], beta)), r2_score(y[te], predict(X[te], beta))


# ======================= PART C =======================
def mse_gradient(Xb, y, beta):
    n = len(y)
    residual = Xb @ beta - y
    return (2 / n) * Xb.T @ residual


def fit_gd(X, y, lr=0.1, n_iters=2000):
    Xb = add_intercept(X)
    beta = np.zeros(Xb.shape[1])
    for _ in range(n_iters):
        beta -= lr * mse_gradient(Xb, y, beta)
    return beta
    # If X were NOT standardized (sqm ~ 75, has_balcony ~ 0.5), the loss surface would be
    # a very elongated valley: lr small enough for sqm is far too small for the others.


# ======================= PART D =======================
def fit_ridge(X, y, lam):
    x_mean, y_mean = X.mean(axis=0), y.mean()
    Xc, yc = X - x_mean, y - y_mean
    d = X.shape[1]
    b = np.linalg.solve(Xc.T @ Xc + lam * np.eye(d), Xc.T @ yc)
    a = y_mean - x_mean @ b
    return np.concatenate([[a], b])


def coef_standard_errors(X, y):
    Xb = add_intercept(X)
    n, p = Xb.shape
    beta = np.linalg.solve(Xb.T @ Xb, Xb.T @ y)
    e = y - Xb @ beta
    sigma2 = (e @ e) / (n - p)
    cov = sigma2 * np.linalg.inv(Xb.T @ Xb)
    return np.sqrt(np.diag(cov))


def duplicate_data_experiment(X, y):
    X2, y2 = np.vstack([X, X]), np.concatenate([y, y])
    beta, beta_dup = fit_ols(X, y), fit_ols(X2, y2)
    return {
        "beta": beta, "beta_dup": beta_dup,
        "r2": r2_score(y, predict(X, beta)), "r2_dup": r2_score(y2, predict(X2, beta_dup)),
        "se": coef_standard_errors(X, y), "se_dup": coef_standard_errors(X2, y2),
    }
    # WHY: X2^T X2 = 2 X^T X and X2^T y2 = 2 X^T y -> the 2s cancel -> same beta.
    # R^2 is a ratio of sums that both double -> unchanged.
    # sigma2_hat ~ unchanged, but (X2^T X2)^-1 = (1/2)(X^T X)^-1 -> SE shrinks by 1/sqrt(2),
    # t-stats grow by sqrt(2): you look "more significant" with ZERO new information.
    # Lesson: standard errors assume independent observations. Duplicated / overlapping
    # samples (e.g. overlapping multi-day returns) fake significance.


if __name__ == "__main__":
    df = pd.read_csv(DATA)
    a, b = simple_fit(df["sqm"].to_numpy(float), df["rent"].to_numpy(float))
    print(f"Simple fit: rent = {a:.1f} + {b:.2f} * sqm")

    X, y = load_design()
    beta = fit_ols(X, y)
    se = coef_standard_errors(X, y)
    print(f"\n{'term':<24}{'coef':>9}{'SE':>8}{'t':>7}   (true value in tools/make_datasets.py)")
    for name, c, s in zip(["intercept"] + FEATURES, beta, se):
        print(f"{name:<24}{c:9.1f}{s:8.1f}{c / s:7.1f}")
    print("\n(train R2, test R2):", tuple(round(float(v), 3) for v in train_test_r2(X, y)))

    Z = (X - X.mean(axis=0)) / X.std(axis=0)
    print("GD matches OLS on standardized X:", np.allclose(fit_gd(Z, y), fit_ols(Z, y), atol=1e-3))

    for lam in [0, 10, 100, 1000]:
        print(f"ridge lam={lam:<5} slopes on standardized X:", np.round(fit_ridge(Z, y, lam)[1:], 1))

    res = duplicate_data_experiment(X, y)
    print("\nDuplicate data: same beta?", np.allclose(res["beta"], res["beta_dup"]),
          "| R2", round(res["r2"], 4), "->", round(res["r2_dup"], 4),
          "| SE ratio", np.round(res["se_dup"] / res["se"], 3)[:3])

    from sklearn.linear_model import LinearRegression
    sk = LinearRegression().fit(X, y)
    print("sklearn agrees with OLS:", np.allclose(np.r_[sk.intercept_, sk.coef_], beta))
