"""Run:  python check.py   |  python check.py A2   |  python check.py solution
(Don't read below - it contains the answers.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from checker import Checks, between, close, equal, is_type  # noqa: E402
import solution as ref  # noqa: E402
import numpy as np  # noqa: E402

checks = Checks(__file__)
X_TR, X_TE, Y_TR, Y_TE = ref.load_split()
XS_TR, XS_TE = ref.scale_train_test(X_TR, X_TE)

# tiny hand-made example
XT = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [5.0, 5.0], [6.0, 5.0]])
YT = np.array(["a", "a", "b", "b", "b"])


@checks.task("A1", "euclidean", "distance")
def _(f):
    close(f(np.array([0.0, 0.0]), np.array([3.0, 4.0])), 5.0, what="euclidean((0,0),(3,4))")


@checks.task("A2", "knn_predict_one", "argsort + vote")
def _(f):
    equal(str(f(XT, YT, np.array([0.2, 0.1]), 1)), "a", "k=1 near origin")
    equal(str(f(XT, YT, np.array([0.2, 0.1]), 3)), "a", "k=3 near origin (votes a,a,b)")
    equal(str(f(XT, YT, np.array([5.5, 5.0]), 3)), "b", "k=3 near (5.5,5)")
    equal(str(f(XT, YT, np.array([0.1, 0.9]), 2)), "b", "k=2 tie -> closest neighbour's label")


@checks.task("A3", "knn_predict", "predict many")
def _(f):
    out = f(XS_TR, Y_TR, XS_TE[:20], 5)
    is_type(out, np.ndarray)
    equal(list(out), list(ref.knn_predict(XS_TR, Y_TR, XS_TE[:20], 5)), "predictions for 20 test rows")


@checks.task("B1", "accuracy", "mean of matches")
def _(f):
    close(f(np.array(["a", "b", "c", "a"]), np.array(["a", "b", "a", "a"])), 0.75, what="accuracy")


@checks.task("B2", "scale_train_test", "train statistics")
def _(f):
    a, b = f(X_TR, X_TE)
    close(a.mean(axis=0), np.zeros(4), tol=1e-9, what="scaled train means")
    close(a.std(axis=0), np.ones(4), tol=1e-9, what="scaled train stds")
    close(b, XS_TE, tol=1e-9, what="scaled test (must use TRAIN mean/std)")


@checks.task("B3", "scaling_experiment", "why scaling matters")
def _(f):
    raw, scaled = f(X_TR, X_TE, Y_TR, Y_TE, k=5)
    close((raw, scaled), ref.scaling_experiment(X_TR, X_TE, Y_TR, Y_TE, 5), tol=1e-9,
          what="(acc_unscaled, acc_scaled)")


@checks.task("C1", "cross_val_accuracy", "k-fold CV by hand")
def _(f):
    for k in (1, 5):
        close(f(XS_TR, Y_TR, k), ref.cross_val_accuracy(XS_TR, Y_TR, k), tol=1e-9, what=f"CV accuracy k={k}")


@checks.task("C2", "best_k", "model selection")
def _(f):
    equal(int(f(XS_TR, Y_TR)), ref.best_k(XS_TR, Y_TR), "best k")


@checks.task("C3", "confusion_matrix", "multi-class counts")
def _(f):
    M = f(np.array(["apple", "lemon", "orange", "apple"]), np.array(["apple", "orange", "orange", "lemon"]))
    close(M, [[1, 1, 0], [0, 0, 1], [0, 0, 1]], what="confusion matrix")


@checks.task("D1", "sklearn_knn_accuracy", "Pipeline")
def _(f):
    between(float(f(X_TR, X_TE, Y_TR, Y_TE, 5)), 0.85, 0.95, "sklearn pipeline accuracy")


@checks.task("D2", "fit_gaussian_nb", "BONUS priors, means, vars")
def _(f):
    m = f(X_TR, Y_TR)
    is_type(m, dict)
    equal(sorted(m), ref.LABELS, "classes")
    e = ref.fit_gaussian_nb(X_TR, Y_TR)
    for c in ref.LABELS:
        close(m[c]["prior"], e[c]["prior"], what=f"prior[{c}]")
        close(m[c]["mean"], e[c]["mean"], what=f"mean[{c}]")
        close(m[c]["var"], e[c]["var"], what=f"var[{c}] (ddof=0)")


@checks.task("D3", "predict_gaussian_nb", "BONUS log-posterior argmax")
def _(f):
    model = ref.fit_gaussian_nb(X_TR, Y_TR)
    equal(list(f(model, X_TE)), list(ref.predict_gaussian_nb(model, X_TE)), "NB predictions")


if __name__ == "__main__":
    checks.run()
