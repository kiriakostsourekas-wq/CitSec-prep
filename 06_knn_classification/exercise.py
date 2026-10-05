"""
06 - k-NEAREST NEIGHBOURS (+ bonus Naive Bayes)  (about 1-1.5 hours)
====================================================================
Dataset: data/fruits.csv - classify apple / orange / lemon from
         weight_g, width_cm, height_cm, color_score.

kNN has no training step: to classify a point, find the k closest training
points and take a majority vote. It's the simplest non-linear classifier,
and the perfect example of WHY FEATURE SCALING MATTERS (weight is in the
hundreds, color_score is between 0 and 1...).

Part A: kNN from scratch
Part B: evaluation + the scaling experiment
Part C: choose k with k-fold cross-validation (from scratch), multi-class confusion matrix
Part D: sklearn version + BONUS Gaussian Naive Bayes from scratch

Run `python check.py` to test, `python exercise.py` for the playground.
"""
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "fruits.csv"
FEATURES = ["weight_g", "width_cm", "height_cm", "color_score"]
LABELS = ["apple", "lemon", "orange"]


def load_split(path=DATA, test_frac=0.3, seed=0):
    """GIVEN: returns X_train, X_test, y_train, y_test (y are numpy arrays of strings). NOT scaled."""
    df = pd.read_csv(path)
    X, y = df[FEATURES].to_numpy(float), df["fruit"].to_numpy(str)
    idx = np.random.default_rng(seed).permutation(len(y))
    n_test = round(test_frac * len(y))
    return X[idx[n_test:]], X[idx[:n_test]], y[idx[n_test:]], y[idx[:n_test]]


# ======================================================================
# PART A - kNN FROM SCRATCH
# ======================================================================
def euclidean(a, b):
    """Euclidean distance between two 1-D arrays."""
    raise NotImplementedError


def knn_predict_one(X_train, y_train, x, k):
    """Predict the label of ONE point x:
      1) distances from x to every training row (vectorized, no loop needed)
      2) indices of the k smallest distances, ordered from nearest to farthest (np.argsort)
      3) majority vote among their labels.
    Tie-break: if several labels have the same number of votes, return the one whose
    neighbour is CLOSEST. (Counter(...).most_common(1) does exactly this if you feed it
    the labels ordered from nearest to farthest.)"""
    raise NotImplementedError


def knn_predict(X_train, y_train, X_test, k):
    """Predict every row of X_test. Return a numpy array of labels."""
    raise NotImplementedError


# ======================================================================
# PART B - EVALUATION + SCALING
# ======================================================================
def accuracy(y, y_hat):
    """Fraction of correct predictions."""
    raise NotImplementedError


def scale_train_test(X_train, X_test):
    """Standardize both arrays using the mean and std of X_TRAIN (population std).
    Return (X_train_scaled, X_test_scaled)."""
    raise NotImplementedError


def scaling_experiment(X_train, X_test, y_train, y_test, k=5):
    """Return (acc_without_scaling, acc_with_scaling) of kNN on the test set.
    Before you run it: predict which will win and by how much."""
    raise NotImplementedError


# ======================================================================
# PART C - CHOOSING k WITH CROSS-VALIDATION
# ======================================================================
def cross_val_accuracy(X, y, k, n_folds=5):
    """k-fold cross-validation of kNN with neighbour count k, on (X, y) which is
    assumed to be ALREADY shuffled and scaled.
      folds = np.array_split(np.arange(len(y)), n_folds)
      for each fold: validate on that fold, train on all the other rows
    Return the mean validation accuracy over the folds."""
    raise NotImplementedError


def best_k(X, y, ks=(1, 3, 5, 7, 9, 15, 25, 51), n_folds=5):
    """Return the k in ks with the highest cross_val_accuracy (first one if tied)."""
    raise NotImplementedError


def confusion_matrix(y, y_hat, labels=LABELS):
    """Return a len(labels) x len(labels) integer numpy array M where
    M[i, j] = number of samples whose TRUE label is labels[i] and PREDICTED label is labels[j]."""
    raise NotImplementedError


# ======================================================================
# PART D - LIBRARY + BONUS: GAUSSIAN NAIVE BAYES
# ======================================================================
def sklearn_knn_accuracy(X_train, X_test, y_train, y_test, k=5):
    """Use sklearn: make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)),
    fit on train, return test accuracy (model.score)."""
    raise NotImplementedError


def fit_gaussian_nb(X, y):
    """BONUS. Naive Bayes assumes features are independent GIVEN the class, and each is
    Gaussian. "Fitting" = computing, for every class c:
        prior[c] = fraction of rows with label c
        mean[c]  = per-feature mean of those rows           (shape (d,))
        var[c]   = per-feature variance of those rows (ddof=0)  (shape (d,))
    Return a dict: {c: {"prior": float, "mean": array, "var": array}}"""
    raise NotImplementedError


def predict_gaussian_nb(model, X):
    """BONUS. For each row x and each class c compute the log-posterior (up to a constant):
        log prior[c] + sum_j [ -0.5*log(2*pi*var[c][j]) - (x_j - mean[c][j])^2 / (2*var[c][j]) ]
    and predict the class with the largest value. Return a numpy array of labels."""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print(df.head())
    print(df.groupby("fruit").agg(["mean", "std"]).round(2).T)   # which feature separates the classes best?
