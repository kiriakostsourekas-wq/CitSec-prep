"""
04 - LINEAR REGRESSION  (about 2 hours)
========================================
Dataset: data/apartments.csv - predict monthly `rent` from apartment features.

Part A: one feature, closed form by hand            (warm-up)
Part B: many features with the normal equations     (the core)
Part C: the same model with gradient descent        (how ML "really" trains)
Part D: ridge + the famous Citadel question: "what if you duplicate the data?"

Conventions used everywhere in this file:
  - X is a numpy array of shape (n, d) WITHOUT an intercept column
  - beta is a numpy array of shape (d + 1,): beta[0] = intercept, beta[1:] = slopes
  - you can add the intercept column with add_intercept() (already written)

Run `python check.py` to test, `python exercise.py` for the playground.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "apartments.csv"
FEATURES = ["sqm", "bedrooms", "dist_center_km", "age_years", "floor", "has_balcony",
            "neighborhood_Riverside", "neighborhood_Suburb"]


def add_intercept(X):
    """Given (already written): prepend a column of ones."""
    return np.column_stack([np.ones(len(X)), X])


# ======================================================================
# PART A - SIMPLE LINEAR REGRESSION  y = a + b*x
# ======================================================================
def simple_fit(x, y):
    """x, y are 1-D arrays. Return (a, b) = (intercept, slope) minimizing squared error.
    Closed form:   b = cov(x, y) / var(x)      a = mean(y) - b * mean(x)
    (Any consistent ddof works because it cancels in the ratio.)"""
    raise NotImplementedError


def mse(y, y_hat):
    """Mean squared error."""
    raise NotImplementedError


def r2_score(y, y_hat):
    """Coefficient of determination:  R^2 = 1 - SS_res / SS_tot
    SS_res = sum (y - y_hat)^2 ,  SS_tot = sum (y - mean(y))^2"""
    raise NotImplementedError


# ======================================================================
# PART B - MULTIPLE LINEAR REGRESSION (ORDINARY LEAST SQUARES)
# ======================================================================
def load_design(path=DATA):
    """Read the CSV, one-hot encode 'neighborhood' with drop_first=True and dtype=int
    (so 'Center' is the baseline), and return (X, y) as numpy arrays where X has the
    columns listed in FEATURES (in that order) and y is the rent."""
    raise NotImplementedError


def fit_ols(X, y):
    """Return beta (shape (d+1,)) solving the normal equations
            (Xb^T Xb) beta = Xb^T y      where Xb = add_intercept(X)
    Use np.linalg.solve (do not invert the matrix)."""
    raise NotImplementedError


def predict(X, beta):
    """Predictions for X (no intercept column) given beta (intercept first)."""
    raise NotImplementedError


def train_test_r2(X, y, test_frac=0.2, seed=0):
    """Shuffle with idx = np.random.default_rng(seed).permutation(n); the first
    round(test_frac*n) positions are TEST, the rest TRAIN.
    Fit OLS on train. Return (r2_train, r2_test)."""
    raise NotImplementedError


# ======================================================================
# PART C - GRADIENT DESCENT
# ======================================================================
def mse_gradient(Xb, y, beta):
    """Xb already HAS the intercept column. Return the gradient of
            L(beta) = (1/n) * sum (Xb @ beta - y)^2
    with respect to beta, i.e.   (2/n) * Xb^T (Xb @ beta - y)."""
    raise NotImplementedError


def fit_gd(X, y, lr=0.1, n_iters=2000):
    """Gradient descent on the MSE. X is assumed ALREADY STANDARDIZED.
    Start from beta = zeros, repeat n_iters times: beta = beta - lr * gradient.
    Return beta (intercept first). It should match fit_ols(X, y) closely."""
    raise NotImplementedError


# ======================================================================
# PART D - RIDGE, STANDARD ERRORS, DUPLICATED DATA
# ======================================================================
def fit_ridge(X, y, lam):
    """Ridge regression: minimize  sum (y - a - X b)^2 + lam * ||b||^2
    The intercept a is NOT penalized. Easiest way:
       1) center:  Xc = X - X.mean(axis=0),  yc = y - y.mean()
       2) b = solve(Xc^T Xc + lam * I, Xc^T yc)
       3) a = y.mean() - X.mean(axis=0) @ b
    Return np.concatenate([[a], b]).  With lam = 0 it must equal OLS."""
    raise NotImplementedError


def coef_standard_errors(X, y):
    """Classical OLS standard errors of beta (intercept first):
        residuals e = y - Xb beta,   p = number of columns of Xb
        sigma2_hat  = (e @ e) / (n - p)
        Cov(beta)   = sigma2_hat * inverse(Xb^T Xb)
        SE          = sqrt(diagonal of Cov(beta))
    (Here you may use np.linalg.inv.)"""
    raise NotImplementedError


def duplicate_data_experiment(X, y):
    """THE Citadel question: "What happens to the coefficients, R^2 and t-stats if you
    feed the same data twice?" - answer it empirically.
    Stack the data on top of itself (np.vstack / np.concatenate), refit, and return a dict:
        {"beta": ..., "beta_dup": ..., "r2": ..., "r2_dup": ..., "se": ..., "se_dup": ...}
    (r2 = in-sample R^2 of each fit, se = coef_standard_errors of each fit)
    Then THINK: why is beta unchanged but se smaller by ~1/sqrt(2)?"""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print(df.head())
    print(df.describe().round(1))
    print(df.corr(numeric_only=True)["rent"].sort_values())   # which features relate to rent?

    # Optional plot (saved as a file, no window needed):
    # import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    # plt.scatter(df["sqm"], df["rent"], s=8); plt.xlabel("sqm"); plt.ylabel("rent")
    # plt.savefig("rent_vs_sqm.png"); print("saved rent_vs_sqm.png")
