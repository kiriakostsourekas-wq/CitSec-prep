"""
10 - MOCK INTERVIEW (bike rentals) - REFERENCE SOLUTION
Read the README first. This file is one good answer, not the only one.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "bike_rentals.csv"
FEATURES = ["temp_c", "humidity", "windspeed_kmh", "is_weekend", "weather_cloudy", "weather_rain"]


# ---------------- Stage 1: load + clean ----------------
def load_and_clean(path=DATA):
    df = pd.read_csv(path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    # Time series -> fill gaps from NEIGHBOURING days (linear interpolation), not a global mean.
    # (Strictly, interpolation peeks one day ahead; in a live system you'd forward-fill instead.)
    df["temp_c"] = df["temp_c"].interpolate()
    df["humidity"] = df["humidity"].interpolate()
    df["t"] = (df["date"] - df["date"].iloc[0]).dt.days          # day index 0..364 (time trend)
    df = pd.get_dummies(df, columns=["weather"], drop_first=True, dtype=int)  # baseline = clear
    return df


# ---------------- Stage 2: split by TIME ----------------
def time_split(df, train_frac=0.75):
    n_train = round(train_frac * len(df))
    return df.iloc[:n_train].copy(), df.iloc[n_train:].copy()      # past -> train, future -> test


def rmse(y, y_hat):
    return float(np.sqrt(np.mean((np.asarray(y, float) - np.asarray(y_hat, float)) ** 2)))


# ---------------- Stage 3: baseline ----------------
def baseline_rmse(train, test):
    return rmse(test["rentals"], np.full(len(test), train["rentals"].mean()))


# ---------------- Stage 4: linear regression ----------------
def linear_fit_eval(train, test, features):
    """Return (test_rmse, test_bias) where bias = mean(prediction - actual)."""
    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(train[features], train["rentals"])
    pred = model.predict(test[features])
    return rmse(test["rentals"], pred), float(np.mean(pred - test["rentals"]))


# ---------------- Stage 5: feature engineering ----------------
def add_temp_squared(df):
    out = df.copy()
    out["temp_sq"] = out["temp_c"] ** 2   # lets a LINEAR model bend: rentals peak at a mild temperature
    return out


# ---------------- Stage 6: tree ----------------
def tree_rmse(train, test, features, max_depth=4):
    from sklearn.tree import DecisionTreeRegressor
    model = DecisionTreeRegressor(max_depth=max_depth, random_state=0).fit(train[features], train["rentals"])
    return rmse(test["rentals"], model.predict(test[features]))


# ---------------- Stage 7: classification twist ----------------
def busy_day_auc(train, test, features):
    """Busy day = rentals above the TRAIN median. Logistic regression -> test ROC-AUC."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    threshold = train["rentals"].median()
    y_tr = (train["rentals"] > threshold).astype(int)
    y_te = (test["rentals"] > threshold).astype(int)
    model = make_pipeline(StandardScaler(), LogisticRegression()).fit(train[features], y_tr)
    return float(roc_auc_score(y_te, model.predict_proba(test[features])[:, 1]))


if __name__ == "__main__":
    df = add_temp_squared(load_and_clean())
    train, test = time_split(df)
    print(f"train: {train.date.min().date()} -> {train.date.max().date()}  ({len(train)} days)")
    print(f"test:  {test.date.min().date()} -> {test.date.max().date()}  ({len(test)} days)\n")

    print(f"{'model':<36}{'test RMSE':>10}{'bias':>9}")
    print(f"{'baseline (train mean)':<36}{baseline_rmse(train, test):10.1f}")
    for name, feats in [("linear, features + t", FEATURES + ["t"]),
                        ("linear, features (no t)", FEATURES),
                        ("linear, features + temp^2", FEATURES + ["temp_sq"])]:
        r, b = linear_fit_eval(train, test, feats)
        print(f"{name:<36}{r:10.1f}{b:9.1f}")
    for d in (2, 4, 8):
        print(f"{'tree depth ' + str(d):<36}{tree_rmse(train, test, FEATURES, d):10.1f}")

    print("\nWhy is 'linear + t' WORSE than the baseline? Train = Jan-Sep: rentals rise with the season,")
    print("and t soaks up that seasonal rise (coef ~7.7/day vs true trend 2.5/day). Extrapolated to")
    print("Oct-Dec it predicts ~1450 too many rentals per day. Always check the bias of test errors.")

    print(f"\nbusy-day logistic AUC: {busy_day_auc(train, test, FEATURES + ['temp_sq']):.3f}")

    shuffled = df.sample(frac=1, random_state=0)
    tr2, te2 = shuffled.iloc[:274], shuffled.iloc[274:]
    print(f"[random split] linear + t RMSE {linear_fit_eval(tr2, te2, FEATURES + ['t'])[0]:7.1f}"
          "   <- looks fine: a random split HIDES the extrapolation problem")
