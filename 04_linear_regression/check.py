"""Run:  python check.py   |  python check.py B2   |  python check.py solution
(Don't read below - it contains the answers.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from checker import Checks, between, close, equal, is_type  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

checks = Checks(__file__)
DATA = Path(__file__).resolve().parent / "data" / "apartments.csv"
FEATURES = ["sqm", "bedrooms", "dist_center_km", "age_years", "floor", "has_balcony",
            "neighborhood_Riverside", "neighborhood_Suburb"]


def design():
    df = pd.get_dummies(pd.read_csv(DATA), columns=["neighborhood"], drop_first=True, dtype=int)
    return df[FEATURES].to_numpy(float), df["rent"].to_numpy(float)


def ols(X, y):
    Xb = np.column_stack([np.ones(len(X)), X])
    return np.linalg.lstsq(Xb, y, rcond=None)[0]


def r2(y, yh):
    return 1 - np.sum((y - yh) ** 2) / np.sum((y - y.mean()) ** 2)


X, Y = design()
Z = (X - X.mean(axis=0)) / X.std(axis=0)


@checks.task("A1", "simple_fit", "slope = cov/var")
def _(f):
    a, b = f(np.array([0.0, 1.0, 2.0, 3.0]), np.array([1.0, 3.0, 5.0, 7.0]))
    close(a, 1, what="intercept for y = 1 + 2x")
    close(b, 2, what="slope for y = 1 + 2x")
    a, b = f(X[:, 0], Y)
    ea, eb = ols(X[:, :1], Y)
    close((a, b), (ea, eb), tol=1e-6, what="(intercept, slope) for rent ~ sqm")


@checks.task("A2", "mse", "mean squared error")
def _(f):
    close(f(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 5.0])), 4 / 3, what="mse")


@checks.task("A3", "r2_score", "1 - SSres/SStot")
def _(f):
    y = np.array([1.0, 2.0, 3.0, 4.0])
    close(f(y, y), 1.0, what="R2 of perfect predictions")
    close(f(y, np.full(4, y.mean())), 0.0, what="R2 of predicting the mean")
    close(f(y, np.array([2.0, 2.0, 3.0, 3.0])), 0.6, what="R2 example")


@checks.task("B1", "load_design", "one-hot + to_numpy")
def _(f):
    Xo, yo = f()
    is_type(Xo, np.ndarray, "X")
    equal(Xo.shape, (300, 8), "X shape")
    close(Xo, X, what="X (check column order = FEATURES)")
    close(yo, Y, what="y")


@checks.task("B2", "fit_ols", "normal equations")
def _(f):
    beta = f(X, Y)
    is_type(beta, np.ndarray, "beta")
    equal(beta.shape, (9,), "beta shape (intercept + 8 slopes)")
    close(beta, ols(X, Y), tol=1e-6, what="beta")


@checks.task("B3", "predict", "Xb @ beta")
def _(f):
    beta = ols(X, Y)
    close(f(X[:3], beta), np.column_stack([np.ones(3), X[:3]]) @ beta, tol=1e-8, what="predictions")


@checks.task("B4", "train_test_r2", "evaluate out-of-sample")
def _(f):
    out = f(X, Y, test_frac=0.2, seed=0)
    equal(len(out), 2, "number of returned values")
    idx = np.random.default_rng(0).permutation(len(Y))
    te, tr = idx[:60], idx[60:]
    b = ols(X[tr], Y[tr])
    Xb = lambda A: np.column_stack([np.ones(len(A)), A])
    close(out, (r2(Y[tr], Xb(X[tr]) @ b), r2(Y[te], Xb(X[te]) @ b)), tol=1e-6, what="(r2_train, r2_test)")


@checks.task("C1", "mse_gradient", "(2/n) X^T (X b - y)")
def _(f):
    Xb = np.column_stack([np.ones(3), np.array([1.0, 2.0, 3.0])])
    y = np.array([2.0, 4.0, 6.0])
    close(f(Xb, y, np.zeros(2)), [-8.0, -56 / 3], what="gradient at beta = 0")
    close(f(Xb, y, np.array([0.0, 2.0])), [0.0, 0.0], what="gradient at the optimum")


@checks.task("C2", "fit_gd", "gradient descent loop")
def _(f):
    beta = f(Z, Y, lr=0.1, n_iters=2000)
    close(beta, ols(Z, Y), tol=1e-2, what="GD beta vs OLS beta on standardized X")


@checks.task("D1", "fit_ridge", "L2 regularization")
def _(f):
    close(f(Z, Y, 0.0), ols(Z, Y), tol=1e-6, what="ridge with lam=0 (must equal OLS)")
    lam = 100.0
    Zc, yc = Z - Z.mean(0), Y - Y.mean()
    b = np.linalg.solve(Zc.T @ Zc + lam * np.eye(8), Zc.T @ yc)
    exp = np.r_[Y.mean() - Z.mean(0) @ b, b]
    close(f(Z, Y, lam), exp, tol=1e-6, what="ridge beta with lam=100")
    if np.linalg.norm(f(Z, Y, 1000.0)[1:]) >= np.linalg.norm(ols(Z, Y)[1:]):
        raise AssertionError("larger lam should shrink the slopes")


@checks.task("D2", "coef_standard_errors", "sigma^2 (X^T X)^-1")
def _(f):
    se = f(X, Y)
    Xb = np.column_stack([np.ones(len(X)), X])
    e = Y - Xb @ ols(X, Y)
    exp = np.sqrt(np.diag((e @ e) / (300 - 9) * np.linalg.inv(Xb.T @ Xb)))
    close(se, exp, tol=1e-6, what="standard errors")


@checks.task("D3", "duplicate_data_experiment", "the Citadel question")
def _(f):
    res = f(X, Y)
    is_type(res, dict)
    for k in ["beta", "beta_dup", "r2", "r2_dup", "se", "se_dup"]:
        if k not in res:
            raise AssertionError(f"missing key '{k}'")
    close(res["beta_dup"], res["beta"], tol=1e-6, what="beta_dup vs beta")
    close(res["r2_dup"], res["r2"], tol=1e-9, what="r2_dup vs r2")
    ratio = np.asarray(res["se_dup"]) / np.asarray(res["se"])
    between(float(ratio.mean()), 0.70, 0.71, "se_dup / se (should be ~ 1/sqrt(2))")


if __name__ == "__main__":
    checks.run()
