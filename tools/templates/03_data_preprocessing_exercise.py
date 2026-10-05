"""
03 - DATA PRE-PROCESSING  (about 1.5 hours)
============================================
Real data is messy. In an ML interview, the person who silently fits a model
on dirty data loses to the person who says: "first let me look at the data".

Dataset: data/customers_raw.csv  (customer table, target = `churned`)
Problems hidden inside (find them yourself in the playground first!):
  - duplicated rows
  - income stored as text, sometimes with commas: "53,700"
  - city names with random case and spaces: " london", "LONDON", "London "
  - impossible ages (typos)
  - missing values in several columns
  - a date column stored as text

Order of work matters:  clean  ->  split  ->  learn statistics on TRAIN only  ->  apply to both.

Run `python check.py` to test, `python exercise.py` for the playground.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "customers_raw.csv"
NUMERIC_COLS = ["age", "income", "monthly_spend", "tenure_days"]
TARGET = "churned"


# ======================================================================
# PART A - LOOK AT THE DATA
# ======================================================================
def load_raw(path=DATA):
    """Just read the CSV and return the DataFrame (no cleaning yet)."""
    raise NotImplementedError


def missing_report(df):
    """Return a Series: column name -> number of missing values,
    ONLY for columns that have at least one missing value,
    sorted from most missing to least missing."""
    raise NotImplementedError


def drop_duplicate_rows(df):
    """Return a copy of df with exact duplicate rows removed
    (keep the first occurrence) and a fresh 0..n-1 index."""
    raise NotImplementedError


# ======================================================================
# PART B - CLEAN COLUMNS  (each function returns a NEW DataFrame)
# ======================================================================
def clean_income(df):
    """Convert 'income' from text like "53,700" / "48000" to float.
    Missing values must stay missing (NaN)."""
    raise NotImplementedError


def clean_city(df):
    """Normalize 'city' so the only values are exactly 'London', 'Paris', 'Dubai'.
    (Remove surrounding spaces, fix capitalization.)"""
    raise NotImplementedError


def fix_age(df):
    """Ages outside [18, 100] are data-entry errors -> replace them with NaN
    (do NOT delete the rows - we will impute later)."""
    raise NotImplementedError


def add_tenure_days(df, reference_date="2026-01-01"):
    """Add a numeric column 'tenure_days' = number of days between
    'signup_date' and reference_date, then DROP the 'signup_date' column.
    (Models cannot use raw date strings.)"""
    raise NotImplementedError


# ======================================================================
# PART C - ENCODE, SPLIT, IMPUTE + SCALE WITHOUT LEAKAGE
# ======================================================================
def one_hot(df):
    """1) Fill missing 'plan' with the string 'unknown' (missingness itself can be informative).
    2) One-hot encode the columns 'city' and 'plan' with drop_first=True
       (avoids the "dummy variable trap" for linear models) and integer 0/1 values.
    Expected new columns: city_London, city_Paris, plan_premium, plan_unknown
    (Dubai and basic are the dropped baseline categories - alphabetically first)."""
    raise NotImplementedError


def train_test_split_df(df, test_frac=0.25, seed=0):
    """Shuffle the row positions with np.random.default_rng(seed).permutation(len(df)),
    put the FIRST round(test_frac * n) shuffled rows in test, the rest in train.
    Return (train_df, test_df). Do not use sklearn here - write it yourself."""
    raise NotImplementedError


def fit_preprocessor(train_df, numeric_cols=NUMERIC_COLS):
    """Learn the preprocessing statistics from the TRAINING data only.
    Return a dict:  col -> {"median": ..., "mean": ..., "std": ...}
      - median: of the column (ignoring NaN) -> used to fill missing values
      - mean, std: of the column AFTER filling NaN with that median
        (use pandas .std(), i.e. ddof=1)
    """
    raise NotImplementedError


def apply_preprocessor(df, params):
    """Return a copy of df where, for every column in params:
        1) NaN -> params[col]["median"]
        2) value -> (value - mean) / std
    Works for both train and test (always uses the TRAIN statistics in params)."""
    raise NotImplementedError


# ======================================================================
# PART D - THE FULL PIPELINE
# ======================================================================
def build_dataset(path=DATA, seed=0):
    """Put everything together in the right order:
        load -> drop duplicates -> clean income/city/age -> tenure_days
        -> one_hot -> split -> fit_preprocessor(train) -> apply to train AND test
    Then drop 'customer_id' (an ID is not a feature!) and separate the target.

    Return X_train, X_test, y_train, y_test as numpy arrays, where the feature
    columns are in this exact order:
        age, income, monthly_spend, tenure_days, city_London, city_Paris, plan_premium, plan_unknown
    """
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print(df.head(10))
    print(df.dtypes)
    print(df.describe())               # look at age: min and max!
    print(df["city"].value_counts())   # look at all the London variants
