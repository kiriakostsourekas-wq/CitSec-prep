"""
06 - kNN (+ Naive Bayes) - REFERENCE SOLUTION
"""
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "fruits.csv"
FEATURES = ["weight_g", "width_cm", "height_cm", "color_score"]
LABELS = ["apple", "lemon", "orange"]


def load_split(path=DATA, test_frac=0.3, seed=0):
    df = pd.read_csv(path)
    X, y = df[FEATURES].to_numpy(float), df["fruit"].to_numpy(str)
    idx = np.random.default_rng(seed).permutation(len(y))
    n_test = round(test_frac * len(y))
    return X[idx[n_test:]], X[idx[:n_test]], y[idx[n_test:]], y[idx[:n_test]]


# ======================= PART A =======================
def euclidean(a, b):
    return float(np.sqrt(np.sum((a - b) ** 2)))


def knn_predict_one(X_train, y_train, x, k):
    dists = np.sqrt(((X_train - x) ** 2).sum(axis=1))   # distance to every training row
    nearest = np.argsort(dists, kind="stable")[:k]      # positions of the k closest
    votes = Counter(y_train[nearest])                   # labels inserted nearest-first
    return votes.most_common(1)[0][0]                   # ties -> earliest inserted = closest


def knn_predict(X_train, y_train, X_test, k):
    return np.array([knn_predict_one(X_train, y_train, x, k) for x in X_test])
    # Cost: O(n_train * d) per query. For big data: KD-trees / ball trees / approximate NN.


# ======================= PART B =======================
def accuracy(y, y_hat):
    return float(np.mean(y == y_hat))


def scale_train_test(X_train, X_test):
    mu, sd = X_train.mean(axis=0), X_train.std(axis=0)
    return (X_train - mu) / sd, (X_test - mu) / sd


def scaling_experiment(X_train, X_test, y_train, y_test, k=5):
    raw = accuracy(y_test, knn_predict(X_train, y_train, X_test, k))
    Xtr, Xte = scale_train_test(X_train, X_test)
    scaled = accuracy(y_test, knn_predict(Xtr, y_train, Xte, k))
    return raw, scaled
    # Unscaled, distance ~ |weight difference| (std 40 g), and weight barely separates the
    # fruits. color_score (std 0.08) separates them well but contributes almost nothing.


# ======================= PART C =======================
def cross_val_accuracy(X, y, k, n_folds=5):
    folds = np.array_split(np.arange(len(y)), n_folds)
    scores = []
    for val_idx in folds:
        train_mask = np.ones(len(y), dtype=bool)
        train_mask[val_idx] = False
        pred = knn_predict(X[train_mask], y[train_mask], X[val_idx], k)
        scores.append(accuracy(y[val_idx], pred))
    return float(np.mean(scores))
    # Strictly, scaling should be re-fitted inside each fold (fit on the training folds only).
    # With a scaler that's a tiny effect; with target-based preprocessing it can be huge.


def best_k(X, y, ks=(1, 3, 5, 7, 9, 15, 25, 51), n_folds=5):
    scores = {k: cross_val_accuracy(X, y, k, n_folds) for k in ks}
    return max(ks, key=lambda k: scores[k])          # max returns the first best on ties


def confusion_matrix(y, y_hat, labels=LABELS):
    pos = {lab: i for i, lab in enumerate(labels)}
    M = np.zeros((len(labels), len(labels)), dtype=int)
    for t, p in zip(y, y_hat):
        M[pos[t], pos[p]] += 1
    return M


# ======================= PART D =======================
def sklearn_knn_accuracy(X_train, X_test, y_train, y_test, k=5):
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    return model.fit(X_train, y_train).score(X_test, y_test)


def fit_gaussian_nb(X, y):
    model = {}
    for c in np.unique(y):
        Xc = X[y == c]
        model[c] = {"prior": len(Xc) / len(X), "mean": Xc.mean(axis=0), "var": Xc.var(axis=0)}
    return model


def predict_gaussian_nb(model, X):
    classes = list(model)
    scores = []
    for c in classes:
        m, v, prior = model[c]["mean"], model[c]["var"], model[c]["prior"]
        log_lik = (-0.5 * np.log(2 * np.pi * v) - (X - m) ** 2 / (2 * v)).sum(axis=1)
        scores.append(np.log(prior) + log_lik)        # shape (n,) per class
    scores = np.column_stack(scores)                  # (n, n_classes)
    return np.array(classes)[scores.argmax(axis=1)]
    # Work in LOG space: multiplying many small densities underflows to 0.


if __name__ == "__main__":
    X_tr, X_te, y_tr, y_te = load_split()
    raw, scaled = scaling_experiment(X_tr, X_te, y_tr, y_te)
    print(f"kNN accuracy  unscaled: {raw:.3f}   scaled: {scaled:.3f}")

    Xs_tr, Xs_te = scale_train_test(X_tr, X_te)
    for k in (1, 3, 5, 9, 25, 51):
        print(f"  CV accuracy k={k:<3} {cross_val_accuracy(Xs_tr, y_tr, k):.3f}")
    k = best_k(Xs_tr, y_tr)
    pred = knn_predict(Xs_tr, y_tr, Xs_te, k)
    print("best k:", k, " test accuracy:", round(accuracy(y_te, pred), 3))
    print("confusion matrix (rows=true, cols=pred):", LABELS)
    print(confusion_matrix(y_te, pred))

    nb = fit_gaussian_nb(X_tr, y_tr)
    print("Gaussian NB test accuracy (no scaling needed!):",
          round(accuracy(y_te, predict_gaussian_nb(nb, X_te)), 3))
    print("sklearn kNN pipeline:", round(sklearn_knn_accuracy(X_tr, X_te, y_tr, y_te), 3))
