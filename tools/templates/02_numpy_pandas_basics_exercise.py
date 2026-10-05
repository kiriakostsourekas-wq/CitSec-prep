"""
02 - NUMPY & PANDAS BASICS  (about 1.5-2 hours)
================================================
Part A: numpy arrays (the language every ML model is written in)
Part B/C: pandas DataFrames using data/stock_prices.csv
Part D: two quant classics (Sharpe ratio, max drawdown)

Keep ../cheatsheets/numpy_cheatsheet.md and pandas_cheatsheet.md open next to you.

Run `python check.py` to test, `python exercise.py` for the playground at the bottom.
RULE for part A: no Python `for` loops - use vectorized numpy operations.
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "stock_prices.csv"


# ======================================================================
# PART A - NUMPY
# ======================================================================
def filter_positive(x):
    """Return only the strictly positive entries of the 1-D array x, using a
    boolean mask (no loop).

    >>> filter_positive(np.array([-1.0, 2.0, 0.0, 3.5]))
    array([2. , 3.5])
    """
    raise NotImplementedError


def standardize(X):
    """X is a 2-D array (rows = samples, columns = features).
    Return a new array where EACH COLUMN has mean 0 and standard deviation 1:
        Z = (X - column_mean) / column_std
    Use the population std (numpy's default, ddof=0).
    Hint word: axis.
    """
    raise NotImplementedError


def add_intercept(X):
    """Return X with an extra column of ones as the FIRST column.
    Shape (n, d) -> (n, d + 1). You will use this in linear regression.

    >>> add_intercept(np.array([[2.0], [3.0]]))
    array([[1., 2.],
           [1., 3.]])
    """
    raise NotImplementedError


def solve_linear_system(A, b):
    """Return x such that A @ x = b (A is square and invertible).
    Do NOT compute the inverse explicitly - there is a numpy function for this.
    """
    raise NotImplementedError


def distances_to_point(X, p):
    """X has shape (n, d), p has shape (d,).
    Return a 1-D array of length n with the Euclidean distance from every row
    of X to p. (This is the core of k-nearest-neighbours in folder 06.)
    """
    raise NotImplementedError


# ======================================================================
# PART B - PANDAS: load, group, reshape
# ======================================================================
def load_prices(path=DATA):
    """Read the CSV into a DataFrame. Make sure the 'date' column is converted
    to real datetimes (not strings). Columns: date, ticker, close, volume.
    """
    raise NotImplementedError


def average_close_by_ticker(df):
    """Return a pandas Series: index = ticker, value = mean close price."""
    raise NotImplementedError


def add_daily_returns(df):
    """Return a COPY of df with a new column 'return' = daily simple return
        r_t = close_t / close_{t-1} - 1
    computed separately for each ticker (the first day of each ticker is NaN).
    Careful: the rows of different tickers are interleaved in the file!
    """
    raise NotImplementedError


def to_wide(df):
    """Reshape the long table into a WIDE table of close prices:
        index = date (sorted), columns = tickers, values = close
    """
    raise NotImplementedError


# ======================================================================
# PART C - PANDAS: rolling windows, filtering, correlation
# ======================================================================
def rolling_mean(wide, window=5):
    """Rolling (moving) average of every column over `window` rows.
    The first window-1 rows will be NaN - that is expected."""
    raise NotImplementedError


def high_volume_days(df, ticker, min_volume):
    """Return the rows of df for `ticker` whose volume is >= min_volume,
    sorted by volume from largest to smallest."""
    raise NotImplementedError


def best_day_per_ticker(df):
    """Using daily returns, return a dict ticker -> date string 'YYYY-MM-DD'
    of that ticker's LARGEST daily return.
    (You may call your add_daily_returns function.)"""
    raise NotImplementedError


def return_correlation(wide):
    """Given the wide close-price table, return the correlation matrix
    (a DataFrame, tickers x tickers) of the DAILY RETURNS (not prices!)."""
    raise NotImplementedError


# ======================================================================
# PART D - QUANT CLASSICS (if your CV quotes a Sharpe ratio, expect questions on it)
# ======================================================================
def annualized_sharpe(wide, periods_per_year=252):
    """Return a Series (one value per ticker) of the annualized Sharpe ratio
    of daily returns, assuming a risk-free rate of 0:
        Sharpe = mean(daily returns) / std(daily returns) * sqrt(252)
    Use pandas' default std (sample std, ddof=1)."""
    raise NotImplementedError


def max_drawdown(prices):
    """prices is a pandas Series of prices over time.
    Drawdown at time t = prices_t / (running maximum of prices up to t) - 1  (<= 0)
    Return the MAXIMUM drawdown as a negative float, e.g. -0.153 for -15.3%.
    Vectorized (no loop). Hint word: cummax."""
    raise NotImplementedError


# ----------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print(df.head())        # first 5 rows
    print(df.dtypes)        # column types: notice 'date' is 'object' (string) here
    print(df.shape)         # (rows, columns)
