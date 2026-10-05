"""Run:  python check.py   |  python check.py B2   |  python check.py solution
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

# hand-made toy problem: feature 0 is useless, feature 1 separates perfectly at 2.5
XT = np.array([[1.0, 1.0], [2.0, 2.0], [1.0, 3.0], [2.0, 4.0], [1.0, 2.0], [2.0, 3.5]])
YT = np.array([0, 0, 1, 1, 0, 1])


def same_tree(a, b, path="root"):
    if a["leaf"] != b["leaf"]:
        raise AssertionError(f"at {path}: expected {'a leaf' if b['leaf'] else 'a split'}, got the opposite")
    equal(a["n"], b["n"], f"number of samples 'n' at {path}")
    if b["leaf"]:
        equal(a["prediction"], b["prediction"], f"prediction at {path}")
        return
    equal(a["feature"], b["feature"], f"split feature at {path}")
    close(a["threshold"], b["threshold"], what=f"threshold at {path}")
    same_tree(a["left"], b["left"], path + ".left")
    same_tree(a["right"], b["right"], path + ".right")


@checks.task("A1", "load_split", "map + split")
def _(f):
    out = f()
    equal(len(out), 4, "number of returned arrays")
    equal((out[0].shape, out[1].shape), ((240, 4), (80, 4)), "(X_train.shape, X_test.shape)")
    close(out[0], X_TR, what="X_train (column order = FEATURES, contract mapped to months)")
    close(out[3], Y_TE, what="y_test")


@checks.task("A2", "gini", "1 - sum p^2")
def _(f):
    close(f(np.array([0, 0, 0, 0])), 0.0, what="gini of a pure node")
    close(f(np.array([0, 1, 0, 1])), 0.5, what="gini of 50/50")
    close(f(np.array([1, 0, 0, 0])), 0.375, what="gini of [1,0,0,0]")
    close(f(np.array([], dtype=int)), 0.0, what="gini of empty")


@checks.task("A3", "entropy", "-sum p log2 p")
def _(f):
    close(f(np.array([1, 1, 1])), 0.0, what="entropy of a pure node")
    close(f(np.array([0, 1])), 1.0, what="entropy of 50/50")
    close(f(np.array([1, 0, 0, 0])), 0.811278124, what="entropy of [1,0,0,0]")


@checks.task("B1", "weighted_impurity", "size-weighted gini")
def _(f):
    close(f(np.array([0, 0]), np.array([1, 1])), 0.0, what="perfect split")
    close(f(np.array([0, 1]), np.array([0, 0, 0, 1])), (2 / 6) * 0.5 + (4 / 6) * 0.375, what="weighted gini")


@checks.task("B2", "best_threshold", "scan midpoints")
def _(f):
    t, s = f(XT[:, 1], YT)
    close((t, s), (2.5, 0.0), what="(threshold, gini) on the separating feature")
    t, s = f(np.array([5.0, 5.0, 5.0]), np.array([0, 1, 0]))
    if t is not None or s != np.inf:
        raise AssertionError(f"constant feature should return (None, inf), got ({t}, {s})")
    close(f(X_TR[:, 0], Y_TR), ref.best_threshold(X_TR[:, 0], Y_TR), what="(threshold, gini) for tenure")


@checks.task("B3", "best_split", "best feature")
def _(f):
    j, t, s = f(XT, YT)
    equal(j, 1, "best feature on toy data")
    close(t, 2.5, what="threshold on toy data")
    j, t, s = f(X_TR, Y_TR)
    ej, et, es = ref.best_split(X_TR, Y_TR)
    equal(j, ej, "best root feature on churn data")
    close((t, s), (et, es), what="(threshold, gini) at the root")


@checks.task("C1", "build_tree", "recursion + stopping rules")
def _(f):
    toy = f(XT, YT, max_depth=3)
    is_type(toy, dict)
    same_tree(toy, {"leaf": False, "feature": 1, "threshold": 2.5, "n": 6,
                    "left": {"leaf": True, "prediction": 0, "n": 3},
                    "right": {"leaf": True, "prediction": 1, "n": 3}})
    stump = f(X_TR, Y_TR, max_depth=0)
    equal(stump, {"leaf": True, "prediction": 0, "n": 240}, "tree with max_depth=0")
    same_tree(f(X_TR, Y_TR, max_depth=3), ref.build_tree(X_TR, Y_TR, max_depth=3))


@checks.task("C2", "predict_one", "walk down the tree")
def _(f):
    tree = ref.build_tree(XT, YT, max_depth=3)
    equal(int(f(tree, np.array([9.0, 1.0]))), 0, "prediction for x=[9, 1]")
    equal(int(f(tree, np.array([9.0, 3.0]))), 1, "prediction for x=[9, 3]")


@checks.task("C3", "predict_tree", "predict many")
def _(f):
    tree = ref.build_tree(X_TR, Y_TR, max_depth=3)
    out = f(tree, X_TE)
    is_type(out, np.ndarray)
    close(out, ref.predict_tree(tree, X_TE), what="test predictions")


@checks.task("D1", "depth_experiment", "overfitting curve")
def _(f):
    out = f(X_TR, Y_TR, X_TE, Y_TE, depths=(1, 3, 8))
    is_type(out, dict)
    exp = ref.depth_experiment(X_TR, Y_TR, X_TE, Y_TE, depths=(1, 3, 8))
    for d in (1, 3, 8):
        close(out[d], exp[d], what=f"(train acc, test acc) at depth {d}")


@checks.task("D2", "sklearn_tree", "DecisionTreeClassifier")
def _(f):
    acc, imp = f(X_TR, Y_TR, X_TE, Y_TE, max_depth=3)
    between(float(acc), 0.85, 0.95, "sklearn depth-3 test accuracy")
    close(np.sum(imp), 1.0, what="sum of feature importances")


if __name__ == "__main__":
    checks.run()
