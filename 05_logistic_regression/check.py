"""Run:  python check.py   |  python check.py B2   |  python check.py solution
(Don't read below - it contains the answers.)"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from checker import Checks, close, equal, is_type  # noqa: E402
import solution as ref  # noqa: E402
import numpy as np  # noqa: E402

checks = Checks(__file__)
X_TR, X_TE, Y_TR, Y_TE = ref.prepare_data()
BETA = ref.fit_logistic(X_TR, Y_TR)
Y_SMALL = np.array([1, 0, 1, 1, 0, 0, 1, 0])
Y_HAT_SMALL = np.array([1, 0, 0, 1, 1, 0, 1, 0])     # tp=3 fp=1 tn=3 fn=1


@checks.task("A1", "sigmoid", "1/(1+e^-z), stable")
def _(f):
    close(f(np.array([0.0])), [0.5], what="sigmoid(0)")
    close(f(np.array([2.0, -2.0])), [0.880797078, 0.119202922], what="sigmoid([2,-2])")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = f(np.array([-1000.0, 1000.0]))
    if np.isnan(out).any():
        raise AssertionError("sigmoid returns nan for large |z| - try np.clip(z, -500, 500)")
    close(out, [0.0, 1.0], what="sigmoid([-1000, 1000])")


@checks.task("A2", "log_loss", "binary cross-entropy")
def _(f):
    close(f(np.array([1, 0]), np.array([0.9, 0.2])), -(np.log(0.9) + np.log(0.8)) / 2, what="log_loss")
    out = f(np.array([1, 0]), np.array([0.0, 1.0]))
    if not np.isfinite(out):
        raise AssertionError("log_loss is infinite for p in {0,1} - clip p first")


@checks.task("B1", "logistic_gradient", "(1/n) X^T (p - y)")
def _(f):
    Xb = np.column_stack([np.ones(4), np.array([1.0, 2.0, 3.0, 4.0])])
    y = np.array([0, 0, 1, 1])
    close(f(Xb, y, np.zeros(2)), [0.0, -0.5], what="gradient at beta = 0")
    b = np.array([0.3, -0.2])
    p = 1 / (1 + np.exp(-(Xb @ b)))
    close(f(Xb, y, b), Xb.T @ (p - y) / 4, what="gradient at beta = [0.3, -0.2]")


@checks.task("B2", "fit_logistic", "gradient descent")
def _(f):
    beta = f(X_TR, Y_TR, lr=0.5, n_iters=3000)
    is_type(beta, np.ndarray, "beta")
    equal(beta.shape, (6,), "beta shape")
    close(beta, BETA, tol=1e-3, what="beta")


@checks.task("B3", "predict_proba", "sigmoid(X beta)")
def _(f):
    p = f(X_TE[:5], BETA)
    close(p, 1 / (1 + np.exp(-(BETA[0] + X_TE[:5] @ BETA[1:]))), tol=1e-8, what="probabilities")


@checks.task("B4", "predict_labels", "threshold")
def _(f):
    p = 1 / (1 + np.exp(-(BETA[0] + X_TE @ BETA[1:])))
    close(f(X_TE, BETA), (p >= 0.5).astype(int), what="labels @0.5")
    close(f(X_TE, BETA, threshold=0.2), (p >= 0.2).astype(int), what="labels @0.2")


@checks.task("C1", "confusion_counts", "tp/fp/tn/fn")
def _(f):
    equal(f(Y_SMALL, Y_HAT_SMALL), {"tp": 3, "fp": 1, "tn": 3, "fn": 1}, "counts")
    equal(f(np.array([1, 1]), np.array([0, 0])), {"tp": 0, "fp": 0, "tn": 0, "fn": 2}, "counts")


@checks.task("C2", "classification_metrics", "precision / recall / F1")
def _(f):
    m = f(Y_SMALL, Y_HAT_SMALL)
    for k in ["accuracy", "precision", "recall", "f1"]:
        close(m[k], 0.75, what=k)
    m = f(np.array([1, 0, 0, 0]), np.array([0, 0, 0, 0]))
    close(m["accuracy"], 0.75, what="accuracy when predicting all zeros")
    close((m["precision"], m["recall"], m["f1"]), (0, 0, 0),
          what="(precision, recall, f1) when nothing is predicted positive")
    m = f(np.array([1, 1, 0, 0, 0]), np.array([1, 0, 1, 1, 0]))
    close((m["precision"], m["recall"], m["f1"]), (1 / 3, 1 / 2, 0.4), what="(precision, recall, f1)")


@checks.task("C3", "roc_auc", "pairwise definition")
def _(f):
    close(f(np.array([0, 0, 1, 1]), np.array([0.1, 0.4, 0.35, 0.8])), 0.75, what="AUC small example")
    close(f(np.array([0, 1]), np.array([0.5, 0.5])), 0.5, what="AUC with a tie")
    from sklearn.metrics import roc_auc_score
    p = 1 / (1 + np.exp(-(BETA[0] + X_TE @ BETA[1:])))
    close(f(Y_TE, p), roc_auc_score(Y_TE, p), tol=1e-9, what="AUC on test set")


@checks.task("D1", "baseline_accuracy", "majority class")
def _(f):
    close(f(np.array([0, 0, 0, 1])), 0.75, what="baseline")
    close(f(np.array([1, 1, 0])), 2 / 3, what="baseline when 1 is the majority")


@checks.task("D2", "odds_ratios", "exp(weights)")
def _(f):
    out = f(BETA)
    is_type(out, dict)
    equal(list(out), ref.FEATURES, "keys")
    close([out[k] for k in ref.FEATURES], np.exp(BETA[1:]), what="odds ratios")


@checks.task("D3", "sklearn_beta", "LogisticRegression")
def _(f):
    close(f(X_TR, Y_TR), BETA, tol=1e-2, what="sklearn beta vs your GD beta")


if __name__ == "__main__":
    checks.run()
