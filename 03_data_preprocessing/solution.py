"""
03 - DATA PRE-PROCESSING - REFERENCE SOLUTION
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "customers_raw.csv"
NUMERIC_COLS = ["age", "income", "monthly_spend", "tenure_days"]
TARGET = "churned"
FEATURES = NUMERIC_COLS + ["city_London", "city_Paris", "plan_premium", "plan_unknown"]


# ======================= PART A =======================
def load_raw(path=DATA):
    return pd.read_csv(path)


def missing_report(df):
    counts = df.isna().sum()               # True counts as 1 when summed
    counts = counts[counts > 0]
    return counts.sort_values(ascending=False)


def drop_duplicate_rows(df):
    return df.drop_duplicates().reset_index(drop=True)


# ======================= PART B =======================
def clean_income(df):
    out = df.copy()
    # .str methods skip NaN automatically; then convert text -> float
    out["income"] = out["income"].str.replace(",", "", regex=False).astype(float)
    return out
    # (alternative: pd.to_numeric(..., errors="coerce") turns anything unparseable into NaN)


def clean_city(df):
    out = df.copy()
    out["city"] = out["city"].str.strip().str.title()     # " london" -> "London"
    return out


def fix_age(df):
    out = df.copy()
    bad = (out["age"] < 18) | (out["age"] > 100)
    out.loc[bad, "age"] = np.nan                            # .loc[row_mask, column] = value
    return out


def add_tenure_days(df, reference_date="2026-01-01"):
    out = df.copy()
    signup = pd.to_datetime(out["signup_date"])
    out["tenure_days"] = (pd.Timestamp(reference_date) - signup).dt.days
    return out.drop(columns=["signup_date"])


# ======================= PART C =======================
def one_hot(df):
    out = df.copy()
    out["plan"] = out["plan"].fillna("unknown")
    return pd.get_dummies(out, columns=["city", "plan"], drop_first=True, dtype=int)


def train_test_split_df(df, test_frac=0.25, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(df))          # shuffled positions 0..n-1
    n_test = round(test_frac * len(df))
    test_idx, train_idx = idx[:n_test], idx[n_test:]
    return df.iloc[train_idx].copy(), df.iloc[test_idx].copy()   # iloc = by POSITION


def fit_preprocessor(train_df, numeric_cols=NUMERIC_COLS):
    params = {}
    for col in numeric_cols:
        med = train_df[col].median()        # NaN are ignored by default
        filled = train_df[col].fillna(med)
        params[col] = {"median": med, "mean": filled.mean(), "std": filled.std()}
    return params


def apply_preprocessor(df, params):
    out = df.copy()
    for col, p in params.items():
        out[col] = (out[col].fillna(p["median"]) - p["mean"]) / p["std"]
    return out


# ======================= PART D =======================
def build_dataset(path=DATA, seed=0):
    df = load_raw(path)
    df = drop_duplicate_rows(df)
    df = clean_income(df)
    df = clean_city(df)
    df = fix_age(df)
    df = add_tenure_days(df)
    df = one_hot(df)                        # stateless, safe before the split
    df = df.drop(columns=["customer_id"])

    train, test = train_test_split_df(df, seed=seed)
    params = fit_preprocessor(train)        # statistics from TRAIN ONLY
    train = apply_preprocessor(train, params)
    test = apply_preprocessor(test, params)

    X_train = train[FEATURES].to_numpy(dtype=float)
    X_test = test[FEATURES].to_numpy(dtype=float)
    y_train = train[TARGET].to_numpy()
    y_test = test[TARGET].to_numpy()
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    raw = load_raw()
    print("Missing values:\n", missing_report(raw), "\n")
    X_train, X_test, y_train, y_test = build_dataset()
    print("Shapes:", X_train.shape, X_test.shape)

    # Reward: fit a model on your clean data (you'll build this yourself in folder 05)
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression().fit(X_train, y_train)
    print("Test accuracy:", round(model.score(X_test, y_test), 3))
    print("Baseline (always predict majority class):",
          round(max(y_test.mean(), 1 - y_test.mean()), 3))
    for name, coef in zip(FEATURES, model.coef_[0]):
        print(f"  {name:<14} {coef:+.2f}")
