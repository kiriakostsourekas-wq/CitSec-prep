"""
07 - DECISION TREE FROM SCRATCH  (about 2-2.5 hours)
=====================================================
Dataset: data/churn.csv - predict whether a telecom customer churns (1) or stays (0)
from tenure_months, contract, monthly_charges, support_calls.

The true rule behind the data is an if/else rule with an INTERACTION - something
a linear model struggles with and a tree captures naturally. Can your tree find it?

Part A: impurity measures (gini, entropy)
Part B: finding the best split (the heart of the algorithm)
Part C: recursive tree building + prediction
Part D: overfitting vs depth, sklearn comparison

Tree representation (plain dicts, so you can print and inspect them):
    leaf:      {"leaf": True,  "prediction": 0 or 1, "n": number_of_samples}
    internal:  {"leaf": False, "feature": j, "threshold": t, "n": number_of_samples,
                "left": <subtree for x[j] <= t>, "right": <subtree for x[j] > t>}

Run `python check.py` to test, `python exercise.py` for the playground.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "churn.csv"
FEATURES = ["tenure_months", "contract_months", "monthly_charges", "support_calls"]
CONTRACT_MONTHS = {"month-to-month": 1, "one-year": 12, "two-year": 24}


def print_tree(node, names=FEATURES, indent=""):
    """GIVEN: pretty-print a tree built with build_tree()."""
    if node["leaf"]:
        print(f"{indent}-> predict {node['prediction']}  (n={node['n']})")
        return
    print(f"{indent}if {names[node['feature']]} <= {node['threshold']:.2f}:  (n={node['n']})")
    print_tree(node["left"], names, indent + "    ")
    print(f"{indent}else:")
    print_tree(node["right"], names, indent + "    ")


# ======================================================================
# PART A - DATA + IMPURITY
# ======================================================================
def load_split(path=DATA, test_frac=0.25, seed=0):
    """Read the CSV, add a numeric column 'contract_months' using CONTRACT_MONTHS
    (hint: Series.map), then shuffle with np.random.default_rng(seed).permutation(n):
    the first round(test_frac*n) positions are test.
    Return X_train, X_test, y_train, y_test as numpy arrays (X columns = FEATURES).
    Trees do NOT need feature scaling - think about why."""
    raise NotImplementedError


def gini(y):
    """Gini impurity of a 0/1 label array:  1 - sum_k p_k^2.
    0 = pure node; 0.5 = 50/50 node (the maximum for 2 classes). Empty array -> 0."""
    raise NotImplementedError


def entropy(y):
    """Entropy in bits:  -sum_k p_k log2(p_k)   (skip classes with p_k = 0). Empty -> 0."""
    raise NotImplementedError


# ======================================================================
# PART B - SPLITTING
# ======================================================================
def weighted_impurity(y_left, y_right):
    """Gini of a split = (n_L/n) * gini(y_left) + (n_R/n) * gini(y_right)."""
    raise NotImplementedError


def best_threshold(x, y):
    """For ONE feature column x, try every candidate threshold
         t = midpoint between consecutive DISTINCT sorted values of x
    with the rule: left = x <= t, right = x > t.
    Return (best_t, best_weighted_gini). If x has only one distinct value, return (None, inf)."""
    raise NotImplementedError


def best_split(X, y):
    """Try every feature with best_threshold. Return (feature_index, threshold, weighted_gini)
    of the best one (lowest weighted gini; first feature wins ties).
    If no feature can be split, return (None, None, inf)."""
    raise NotImplementedError


# ======================================================================
# PART C - BUILD + PREDICT
# ======================================================================
def build_tree(X, y, max_depth=3, min_samples_split=2, depth=0):
    """Recursively build the tree. Make a LEAF (prediction = 1 if mean(y) >= 0.5 else 0) when:
        - depth == max_depth, or
        - len(y) < min_samples_split, or
        - the node is pure (gini == 0), or
        - the best split does NOT reduce impurity (weighted gini >= gini(y)), or no split exists.
    Otherwise split on best_split(X, y) and build the left/right children with depth + 1."""
    raise NotImplementedError


def predict_one(node, x):
    """Walk down from the root: go left if x[feature] <= threshold, else right, until a leaf."""
    raise NotImplementedError


def predict_tree(tree, X):
    """Predict every row of X. Return an int numpy array."""
    raise NotImplementedError


# ======================================================================
# PART D - OVERFITTING + LIBRARY
# ======================================================================
def depth_experiment(X_train, y_train, X_test, y_test, depths=(1, 2, 3, 4, 6, 8, 12)):
    """For each max_depth, build a tree on train and return a dict
         depth -> (train_accuracy, test_accuracy)
    Before running: what do you expect train accuracy to do as depth grows? And test?"""
    raise NotImplementedError


def sklearn_tree(X_train, y_train, X_test, y_test, max_depth=3):
    """Fit sklearn.tree.DecisionTreeClassifier(max_depth=max_depth, random_state=0).
    Return (test_accuracy, feature_importances) where feature_importances is model.feature_importances_."""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print(df.head())
    print("churn rate:", df["churn"].mean().round(3))
    print(df.groupby("contract")["churn"].mean())                  # churn by contract type
    print(df.groupby(df["support_calls"] >= 3)["churn"].mean())    # churn by many support calls
