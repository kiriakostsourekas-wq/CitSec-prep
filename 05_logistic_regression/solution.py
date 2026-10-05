"""
05 - LOGISTIC REGRESSION - REFERENCE SOLUTION
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "loan_default.csv"
FEATURES = ["income_k", "debt_to_income", "credit_score", "years_employed", "late_payments"]


def add_intercept(X):
    return np.column_stack([np.ones(len(X)), X])


def prepare_data(path=DATA, test_frac=0.25, seed=0):
    df = pd.read_csv(path)
    X, y = df[FEATURES].to_numpy(float), df["default"].to_numpy(int)
    idx = np.random.default_rng(seed).permutation(len(y))
    n_test = round(test_frac * len(y))
    te, tr = idx[:n_test], idx[n_test:]
    mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
    return (X[tr] - mu) / sd, (X[te] - mu) / sd, y[tr], y[te]


# ======================= PART A =======================
def sigmoid(z):
    z = np.clip(z, -500, 500)          # exp(500) is fine; exp(1000) overflows to inf
    return 1.0 / (1.0 + np.exp(-z))


def log_loss(y, p, eps=1e-12):
    p = np.clip(p, eps, 1 - eps)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


# ======================= PART B =======================
def logistic_gradient(Xb, y, beta):
    p = sigmoid(Xb @ beta)
    return Xb.T @ (p - y) / len(y)


def fit_logistic(X, y, lr=0.5, n_iters=3000):
    Xb = add_intercept(X)
    beta = np.zeros(Xb.shape[1])
    for _ in range(n_iters):
        beta -= lr * logistic_gradient(Xb, y, beta)
    return beta
    # No closed form exists (the gradient equation is non-linear in beta), but the loss is
    # CONVEX, so gradient descent finds the global minimum. Newton's method / IRLS is what
    # statistics packages use (much faster: uses the Hessian X^T W X).


def predict_proba(X, beta):
    return sigmoid(add_intercept(X) @ beta)


def predict_labels(X, beta, threshold=0.5):
    return (predict_proba(X, beta) >= threshold).astype(int)


# ======================= PART C =======================
def confusion_counts(y, y_hat):
    return {
        "tp": int(np.sum((y == 1) & (y_hat == 1))),
        "fp": int(np.sum((y == 0) & (y_hat == 1))),
        "tn": int(np.sum((y == 0) & (y_hat == 0))),
        "fn": int(np.sum((y == 1) & (y_hat == 0))),
    }


def classification_metrics(y, y_hat):
    c = confusion_counts(y, y_hat)
    tp, fp, tn, fn = c["tp"], c["fp"], c["tn"], c["fn"]
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"accuracy": (tp + tn) / len(y), "precision": precision, "recall": recall, "f1": f1}


def roc_auc(y, p):
    pos, neg = p[y == 1], p[y == 0]
    greater = (pos[:, None] > neg[None, :]).sum()    # table of shape (n_pos, n_neg)
    ties = (pos[:, None] == neg[None, :]).sum()
    return (greater + 0.5 * ties) / (len(pos) * len(neg))
    # O(n_pos * n_neg) memory. The O(n log n) way: sort by score and use ranks
    # (AUC = (sum of ranks of positives - n_pos(n_pos+1)/2) / (n_pos n_neg), Mann-Whitney U).


# ======================= PART D =======================
def baseline_accuracy(y):
    rate = np.mean(y)
    return max(rate, 1 - rate)


def odds_ratios(beta, feature_names=FEATURES):
    return {name: float(np.exp(w)) for name, w in zip(feature_names, beta[1:])}


def sklearn_beta(X, y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(C=1e6, max_iter=5000).fit(X, y)
    return np.concatenate([model.intercept_, model.coef_[0]])


if __name__ == "__main__":
    X_tr, X_te, y_tr, y_te = prepare_data()
    beta = fit_logistic(X_tr, y_tr)
    print("beta:", np.round(beta, 3))
    print("train log-loss:", round(log_loss(y_tr, predict_proba(X_tr, beta)), 4))

    p_te = predict_proba(X_te, beta)
    print("\nTest metrics @0.5:", {k: round(v, 3) for k, v in
                                   classification_metrics(y_te, predict_labels(X_te, beta)).items()})
    print("Baseline accuracy:", round(baseline_accuracy(y_te), 3), "<- always compare with this!")
    print("Test ROC-AUC:", round(roc_auc(y_te, p_te), 3))

    print("\nThreshold trade-off (lower threshold -> catch more defaults, more false alarms):")
    for t in [0.2, 0.3, 0.5, 0.7]:
        m = classification_metrics(y_te, (p_te >= t).astype(int))
        print(f"  t={t}: precision={m['precision']:.2f} recall={m['recall']:.2f} f1={m['f1']:.2f}")

    print("\nOdds ratios per +1 std:")
    for k, v in odds_ratios(beta).items():
        print(f"  {k:<16} x{v:.2f}")
    print("\nsklearn agrees:", np.allclose(sklearn_beta(X_tr, y_tr), beta, atol=1e-2))
