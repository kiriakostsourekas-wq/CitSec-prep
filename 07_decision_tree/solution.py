"""
07 - DECISION TREE - REFERENCE SOLUTION
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "churn.csv"
FEATURES = ["tenure_months", "contract_months", "monthly_charges", "support_calls"]
CONTRACT_MONTHS = {"month-to-month": 1, "one-year": 12, "two-year": 24}


def print_tree(node, names=FEATURES, indent=""):
    if node["leaf"]:
        print(f"{indent}-> predict {node['prediction']}  (n={node['n']})")
        return
    print(f"{indent}if {names[node['feature']]} <= {node['threshold']:.2f}:  (n={node['n']})")
    print_tree(node["left"], names, indent + "    ")
    print(f"{indent}else:")
    print_tree(node["right"], names, indent + "    ")


# ======================= PART A =======================
def load_split(path=DATA, test_frac=0.25, seed=0):
    df = pd.read_csv(path)
    df["contract_months"] = df["contract"].map(CONTRACT_MONTHS)
    X, y = df[FEATURES].to_numpy(float), df["churn"].to_numpy(int)
    idx = np.random.default_rng(seed).permutation(len(y))
    n_test = round(test_frac * len(y))
    te, tr = idx[:n_test], idx[n_test:]
    return X[tr], X[te], y[tr], y[te]
    # No scaling: a split "x <= t" only depends on the ORDER of the values, so any monotone
    # transform (scaling, log) gives the same tree.


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y, minlength=2) / len(y)       # class proportions [p0, p1]
    return float(1 - np.sum(p ** 2))


def entropy(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y) / len(y)
    p = p[p > 0]                                   # 0 * log(0) is defined as 0
    return float(-np.sum(p * np.log2(p)))


# ======================= PART B =======================
def weighted_impurity(y_left, y_right):
    n = len(y_left) + len(y_right)
    return len(y_left) / n * gini(y_left) + len(y_right) / n * gini(y_right)


def best_threshold(x, y):
    values = np.unique(x)                          # sorted distinct values
    if len(values) < 2:
        return None, np.inf
    candidates = (values[:-1] + values[1:]) / 2    # midpoints
    best_t, best_score = None, np.inf
    for t in candidates:
        left = x <= t
        score = weighted_impurity(y[left], y[~left])
        if score < best_score:                     # strict < keeps the first best
            best_t, best_score = t, score
    return float(best_t), float(best_score)
    # O(#values * n) per feature. Faster: sort once and sweep, updating class counts
    # incrementally -> O(n log n) per feature (what real libraries do).


def best_split(X, y):
    best = (None, None, np.inf)
    for j in range(X.shape[1]):
        t, score = best_threshold(X[:, j], y)
        if score < best[2]:
            best = (j, t, score)
    return best


# ======================= PART C =======================
def _leaf(y):
    return {"leaf": True, "prediction": int(np.mean(y) >= 0.5), "n": len(y)}


def build_tree(X, y, max_depth=3, min_samples_split=2, depth=0):
    if depth == max_depth or len(y) < min_samples_split or gini(y) == 0:
        return _leaf(y)
    j, t, score = best_split(X, y)
    if j is None or score >= gini(y):              # no useful split
        return _leaf(y)
    left = X[:, j] <= t
    return {
        "leaf": False, "feature": j, "threshold": t, "n": len(y),
        "left": build_tree(X[left], y[left], max_depth, min_samples_split, depth + 1),
        "right": build_tree(X[~left], y[~left], max_depth, min_samples_split, depth + 1),
    }


def predict_one(node, x):
    while not node["leaf"]:
        node = node["left"] if x[node["feature"]] <= node["threshold"] else node["right"]
    return node["prediction"]


def predict_tree(tree, X):
    return np.array([predict_one(tree, x) for x in X], dtype=int)


# ======================= PART D =======================
def depth_experiment(X_train, y_train, X_test, y_test, depths=(1, 2, 3, 4, 6, 8, 12)):
    out = {}
    for d in depths:
        tree = build_tree(X_train, y_train, max_depth=d)
        out[d] = (float(np.mean(predict_tree(tree, X_train) == y_train)),
                  float(np.mean(predict_tree(tree, X_test) == y_test)))
    return out


def sklearn_tree(X_train, y_train, X_test, y_test, max_depth=3):
    from sklearn.tree import DecisionTreeClassifier
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=0).fit(X_train, y_train)
    return model.score(X_test, y_test), model.feature_importances_


if __name__ == "__main__":
    X_tr, X_te, y_tr, y_te = load_split()
    tree = build_tree(X_tr, y_tr, max_depth=3)
    print("Your depth-3 tree (compare with the TRUE rule in tools/make_datasets.py):")
    print_tree(tree)

    print("\ndepth -> (train acc, test acc)")
    for d, (a, b) in depth_experiment(X_tr, y_tr, X_te, y_te).items():
        print(f"  {d:>2}: train {a:.3f}  test {b:.3f}")
    print("baseline (always 0):", round(1 - y_te.mean(), 3))

    acc, imp = sklearn_tree(X_tr, y_tr, X_te, y_te)
    print("\nsklearn depth-3 test acc:", round(acc, 3))
    print("feature importances:", {f: round(float(v), 3) for f, v in zip(FEATURES, imp)})

    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    lr = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_tr, y_tr)
    rf = RandomForestClassifier(n_estimators=300, max_depth=5, random_state=0).fit(X_tr, y_tr)
    print("logistic regression test acc:", round(lr.score(X_te, y_te), 3), "(can't model the AND interaction)")
    print("random forest test acc:      ", round(rf.score(X_te, y_te), 3), "(just for reference)")
