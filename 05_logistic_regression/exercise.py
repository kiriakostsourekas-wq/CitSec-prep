"""
05 - LOGISTIC REGRESSION  (about 2 hours)
==========================================
Dataset: data/loan_default.csv - predict whether a borrower defaults (1) or not (0).
About 25% of borrowers default -> the classes are imbalanced (keep that in mind!).

Part A: sigmoid + log-loss
Part B: train logistic regression with gradient descent (from scratch)
Part C: evaluate a classifier: confusion matrix, precision/recall/F1, ROC-AUC
Part D: baseline, interpretation (odds ratios), compare with sklearn

Same conventions as folder 04:
  - X has NO intercept column; beta[0] is the intercept, beta[1:] the weights.
  - prepare_data() (already written) gives you standardized train/test arrays.

Run `python check.py` to test, `python exercise.py` for the playground.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "loan_default.csv"
FEATURES = ["income_k", "debt_to_income", "credit_score", "years_employed", "late_payments"]


def add_intercept(X):
    return np.column_stack([np.ones(len(X)), X])


def prepare_data(path=DATA, test_frac=0.25, seed=0):
    """GIVEN (you practised this in folder 03): shuffle, split, standardize with TRAIN stats.
    Returns X_train, X_test, y_train, y_test (numpy arrays)."""
    df = pd.read_csv(path)
    X, y = df[FEATURES].to_numpy(float), df["default"].to_numpy(int)
    idx = np.random.default_rng(seed).permutation(len(y))
    n_test = round(test_frac * len(y))
    te, tr = idx[:n_test], idx[n_test:]
    mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
    return (X[tr] - mu) / sd, (X[te] - mu) / sd, y[tr], y[te]


# ======================================================================
# PART A - THE BUILDING BLOCKS
# ======================================================================
def sigmoid(z):
    """sigma(z) = 1 / (1 + exp(-z)). Must work on numpy arrays (element-wise)
    and must not return nan for very large |z| (e.g. z = -1000 or 1000)."""
    raise NotImplementedError


def log_loss(y, p, eps=1e-12):
    """Binary cross-entropy (average over samples):
        L = -mean( y*log(p) + (1-y)*log(1-p) )
    Clip p into [eps, 1-eps] first so that log(0) never happens."""
    raise NotImplementedError


# ======================================================================
# PART B - TRAINING
# ======================================================================
def logistic_gradient(Xb, y, beta):
    """Xb HAS the intercept column. Gradient of the average log-loss w.r.t. beta:
            (1/n) * Xb^T (sigmoid(Xb @ beta) - y)
    (Same shape as linear regression's gradient - that's not a coincidence!)"""
    raise NotImplementedError


def fit_logistic(X, y, lr=0.5, n_iters=3000):
    """Gradient descent from beta = zeros. Return beta (intercept first)."""
    raise NotImplementedError


def predict_proba(X, beta):
    """Predicted probability of class 1 for every row of X."""
    raise NotImplementedError


def predict_labels(X, beta, threshold=0.5):
    """1 if predicted probability >= threshold else 0 (as an int numpy array)."""
    raise NotImplementedError


# ======================================================================
# PART C - EVALUATION
# ======================================================================
def confusion_counts(y, y_hat):
    """Return a dict with integer counts {"tp": ..., "fp": ..., "tn": ..., "fn": ...}
    (positive = 1 = default)."""
    raise NotImplementedError


def classification_metrics(y, y_hat):
    """Return a dict {"accuracy", "precision", "recall", "f1"}.
        precision = tp / (tp + fp)   "when I say default, how often am I right?"
        recall    = tp / (tp + fn)   "of the real defaults, how many did I catch?"
        f1        = 2 * precision * recall / (precision + recall)
    If a denominator is 0, define that metric as 0.0."""
    raise NotImplementedError


def roc_auc(y, p):
    """ROC-AUC = probability that a randomly chosen POSITIVE gets a higher score than
    a randomly chosen NEGATIVE (ties count 1/2).
    Compute it directly from that definition by comparing every (positive, negative) pair.
    Hint: numpy broadcasting  pos[:, None] > neg[None, :]  makes the whole comparison table."""
    raise NotImplementedError


# ======================================================================
# PART D - BASELINE, INTERPRETATION, LIBRARY
# ======================================================================
def baseline_accuracy(y):
    """Accuracy of the dumbest model: always predict the majority class."""
    raise NotImplementedError


def odds_ratios(beta, feature_names=FEATURES):
    """Return a dict feature -> exp(weight). Because features are standardized, this is
    the multiplicative change in the ODDS of default for a +1 standard deviation change."""
    raise NotImplementedError


def sklearn_beta(X, y):
    """Fit sklearn.linear_model.LogisticRegression with C=1e6 (C = 1/regularization, so a
    huge C means 'almost no regularization') and max_iter=5000.
    Return np.concatenate([model.intercept_, model.coef_[0]]) - it should match fit_logistic."""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print(df.head())
    print("default rate:", df["default"].mean())
    print(df.groupby("default").mean().round(2))    # how do defaulters differ on average?
