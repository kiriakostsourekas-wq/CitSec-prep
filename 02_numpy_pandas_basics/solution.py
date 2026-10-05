"""
02 - NUMPY & PANDAS BASICS - REFERENCE SOLUTION
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "stock_prices.csv"


# ======================= PART A - NUMPY =======================
def filter_positive(x):
    mask = x > 0            # array of True/False, same shape as x
    return x[mask]          # boolean indexing keeps the True positions


def standardize(X):
    mu = X.mean(axis=0)     # axis=0 -> collapse the rows -> one mean per COLUMN, shape (d,)
    sd = X.std(axis=0)
    return (X - mu) / sd    # broadcasting: (n, d) - (d,) works row by row


def add_intercept(X):
    ones = np.ones((X.shape[0], 1))
    return np.hstack([ones, X])          # or np.column_stack([np.ones(len(X)), X])


def solve_linear_system(A, b):
    return np.linalg.solve(A, b)         # faster and more stable than inv(A) @ b


def distances_to_point(X, p):
    diff = X - p                          # broadcasting: subtract p from every row
    return np.sqrt((diff ** 2).sum(axis=1))   # axis=1 -> sum across columns -> one per row
    # equivalently: np.linalg.norm(X - p, axis=1)


# ======================= PART B - PANDAS =======================
def load_prices(path=DATA):
    return pd.read_csv(path, parse_dates=["date"])
    # alternative: df = pd.read_csv(path); df["date"] = pd.to_datetime(df["date"])


def average_close_by_ticker(df):
    return df.groupby("ticker")["close"].mean()


def add_daily_returns(df):
    out = df.sort_values(["ticker", "date"]).copy()
    # groupby makes pct_change restart at every ticker -> no "return" across tickers
    out["return"] = out.groupby("ticker")["close"].pct_change()
    return out.sort_index()               # restore original row order (optional)


def to_wide(df):
    return df.pivot(index="date", columns="ticker", values="close").sort_index()


# ======================= PART C =======================
def rolling_mean(wide, window=5):
    return wide.rolling(window).mean()


def high_volume_days(df, ticker, min_volume):
    mask = (df["ticker"] == ticker) & (df["volume"] >= min_volume)   # & not `and`, with brackets!
    return df[mask].sort_values("volume", ascending=False)


def best_day_per_ticker(df):
    r = add_daily_returns(df)
    idx = r.groupby("ticker")["return"].idxmax()        # row label of the max per group
    best = r.loc[idx, ["ticker", "date"]]
    return {t: d.strftime("%Y-%m-%d") for t, d in zip(best["ticker"], best["date"])}


def return_correlation(wide):
    return wide.pct_change().corr()       # correlate RETURNS: prices are trending, non-stationary


# ======================= PART D =======================
def annualized_sharpe(wide, periods_per_year=252):
    r = wide.pct_change().dropna()
    return r.mean() / r.std() * np.sqrt(periods_per_year)


def max_drawdown(prices):
    running_max = prices.cummax()
    drawdown = prices / running_max - 1
    return float(drawdown.min())


if __name__ == "__main__":
    df = load_prices()
    print(average_close_by_ticker(df))
    wide = to_wide(df)
    print(wide.head())
    print(return_correlation(wide).round(2))
    print(annualized_sharpe(wide).round(2))
    print({t: round(max_drawdown(wide[t]), 4) for t in wide.columns})
