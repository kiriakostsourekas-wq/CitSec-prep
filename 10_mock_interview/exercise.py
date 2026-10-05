"""
10 - MOCK INTERVIEW: BIKE RENTALS  (60 minutes, timed!)
========================================================
Read README.md first - it contains the interviewer's script.
Set a timer for 60 minutes. Talk out loud (record yourself on your phone if you can).

Scenario: "Here is one year of daily bike-rental data from a city. We want to forecast
daily rentals for the next quarter. Walk me through it."

Dataset: data/bike_rentals.csv
  date, temp_c, humidity, windspeed_kmh, is_weekend, weather (clear/cloudy/rain), rentals

The functions below are the checkpoints the interviewer will push you through.
`python check.py` verifies them. You may use sklearn freely here (that's realistic
for a data/ML round); the from-scratch work was in folders 04-07.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "bike_rentals.csv"
FEATURES = ["temp_c", "humidity", "windspeed_kmh", "is_weekend", "weather_cloudy", "weather_rain"]


# ---------------- Stage 1 (10 min): explore + clean ----------------
def load_and_clean(path=DATA):
    """- parse 'date' as datetime and sort by it (reset the index)
    - fill missing temp_c and humidity by LINEAR INTERPOLATION between neighbouring days
      (Series.interpolate()) - think about why that's better than the global mean here
    - add 't' = number of days since the first date (0, 1, 2, ...)
    - one-hot encode 'weather' with drop_first=True, dtype=int  (baseline = clear)
    Return the DataFrame."""
    raise NotImplementedError


# ---------------- Stage 2 (5 min): split ----------------
def time_split(df, train_frac=0.75):
    """The goal is to forecast the FUTURE, so: NO shuffling.
    First round(train_frac * n) days -> train, the rest -> test. Return (train, test)."""
    raise NotImplementedError


def rmse(y, y_hat):
    """Root mean squared error."""
    raise NotImplementedError


# ---------------- Stage 3 (5 min): baseline ----------------
def baseline_rmse(train, test):
    """Test RMSE of predicting the TRAIN mean of 'rentals' for every test day.
    Every model you build must beat this number."""
    raise NotImplementedError


# ---------------- Stage 4 (10 min): linear regression ----------------
def linear_fit_eval(train, test, features):
    """Fit sklearn LinearRegression on train[features] -> train['rentals'].
    Return (test_rmse, test_bias) with bias = mean(prediction - actual) on test.
    Then compare FEATURES + ['t'] with FEATURES alone. One of them is worse than the
    baseline! Explain why before you look at the README."""
    raise NotImplementedError


# ---------------- Stage 5 (5 min): feature engineering ----------------
def add_temp_squared(df):
    """Return a copy with an extra column 'temp_sq' = temp_c ** 2.
    Why might rentals be NON-monotonic in temperature?"""
    raise NotImplementedError


# ---------------- Stage 6 (10 min): a tree ----------------
def tree_rmse(train, test, features, max_depth=4):
    """sklearn DecisionTreeRegressor(max_depth=max_depth, random_state=0): return test RMSE."""
    raise NotImplementedError


# ---------------- Stage 7 (10 min): the classification twist ----------------
def busy_day_auc(train, test, features):
    """'Ops only cares whether tomorrow is BUSY.' Busy = rentals > TRAIN median rentals
    (use the train median for both sets!). Fit make_pipeline(StandardScaler(), LogisticRegression())
    on train and return the test ROC-AUC (sklearn.metrics.roc_auc_score on predict_proba[:, 1])."""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    raw = pd.read_csv(DATA)
    print(raw.head())
    print(raw.describe())
    print(raw.isna().sum())
    # Your exploration here: rentals by month? by weather? vs temperature?
