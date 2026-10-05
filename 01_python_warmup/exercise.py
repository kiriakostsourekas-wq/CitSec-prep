"""
01 - PYTHON WARM-UP  (about 1 hour)
===================================
Pure Python only - NO numpy, NO pandas here. Interviewers like to see that
you can write a loop, use a dict, and write a small class without libraries.

How to work:
  1. Read the docstring of a function.
  2. Delete the line `raise NotImplementedError` and write your code.
  3. Run `python check.py` (or `python check.py A1` for one task).
  4. Stuck for more than ~10 minutes? Open hints.md.

You can also run this file directly (`python exercise.py`) to try things in
the playground at the bottom.
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "02_numpy_pandas_basics" / "data" / "stock_prices.csv"


# ----------------------------------------------------------------------
# PART A - loops, comprehensions, dictionaries
# ----------------------------------------------------------------------
def sum_of_squares(nums):
    """Return the sum of the squares of the numbers in `nums`.

    >>> sum_of_squares([1, 2, 3])
    14
    >>> sum_of_squares([])
    0
    """
    raise NotImplementedError


def evens_squared(nums):
    """Return a NEW list with the squares of the even numbers only, in order.
    Try to write it as a one-line list comprehension.

    >>> evens_squared([1, 2, 3, 4, 5, 6])
    [4, 16, 36]
    """
    raise NotImplementedError


def count_words(text):
    """Count how many times each word appears. Return a dict word -> count.
    - lower-case everything ("The" and "the" are the same word)
    - remove the punctuation characters . , ! ? from the ends of words

    >>> count_words("The cat. The DOG!")
    {'the': 2, 'cat': 1, 'dog': 1}
    """
    raise NotImplementedError


# ----------------------------------------------------------------------
# PART B - basic statistics by hand (you will reuse these ideas in ML)
# ----------------------------------------------------------------------
def mean(xs):
    """Arithmetic mean of a non-empty list.

    >>> mean([1, 2, 3, 4])
    2.5
    """
    raise NotImplementedError


def variance(xs, sample=False):
    """Variance of xs.
    - sample=False: population variance  -> divide by n
    - sample=True : sample variance      -> divide by n - 1  (Bessel's correction)

    >>> variance([1, 2, 3, 4])
    1.25
    >>> round(variance([1, 2, 3, 4], sample=True), 4)
    1.6667
    """
    raise NotImplementedError


def median(xs):
    """Median of a non-empty list. Do NOT modify the input list.
    Odd length -> middle element. Even length -> average of the two middle ones.

    >>> median([3, 1, 2])
    2
    >>> median([4, 1, 3, 2])
    2.5
    """
    raise NotImplementedError


# ----------------------------------------------------------------------
# PART C - working with "records" (lists of dicts), sorting, strings
# ----------------------------------------------------------------------
def total_quantity_by_ticker(trades):
    """trades is a list of dicts like {"ticker": "AAA", "qty": 10, "price": 99.5}.
    Return a dict ticker -> total qty traded.

    >>> total_quantity_by_ticker([{"ticker": "A", "qty": 5, "price": 1.0},
    ...                           {"ticker": "B", "qty": 2, "price": 3.0},
    ...                           {"ticker": "A", "qty": 1, "price": 2.0}])
    {'A': 6, 'B': 2}
    """
    raise NotImplementedError


def sort_trades_by_value(trades):
    """Return a NEW list of the trades sorted by notional value (price * qty),
    LARGEST first. Do not change the original list.
    """
    raise NotImplementedError


def is_palindrome(s):
    """True if s reads the same forwards and backwards, ignoring case and any
    character that is not a letter or a digit.

    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("Citadel")
    False
    """
    raise NotImplementedError


# ----------------------------------------------------------------------
# PART D - a small class + reading a file  (interview-style)
# ----------------------------------------------------------------------
class Portfolio:
    """A tiny portfolio tracker.

    p = Portfolio(cash=1000)
    p.buy("AAA", 5, 100)      # spend 500 cash, now hold 5 AAA
    p.sell("AAA", 2, 110)     # receive 220 cash, now hold 3 AAA
    p.position("AAA")         # -> 3
    p.position("ZZZ")         # -> 0   (never traded)
    p.cash                    # -> 720
    p.value({"AAA": 120})     # -> 720 + 3*120 = 1080

    Rules:
      - buy() raises ValueError if there is not enough cash
      - sell() raises ValueError if you try to sell more than you hold
    """

    def __init__(self, cash):
        raise NotImplementedError

    def buy(self, ticker, qty, price):
        raise NotImplementedError

    def sell(self, ticker, qty, price):
        raise NotImplementedError

    def position(self, ticker):
        raise NotImplementedError

    def value(self, prices):
        raise NotImplementedError


def read_closes(path=DATA):
    """Read the CSV at `path` using the built-in `csv` module (NOT pandas).
    The file has columns: date,ticker,close,volume
    Return a dict ticker -> list of close prices (as floats), in file order.

    Example result shape: {"AAA": [98.46, 99.1, ...], "BBB": [...], ...}
    """
    raise NotImplementedError


# ----------------------------------------------------------------------
# Playground: run `python exercise.py` to try your functions by hand.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Try your functions by hand here once you've written them, e.g.:
    # print(sum_of_squares([1, 2, 3]))
    # print(count_words("The cat. The DOG!"))
    print("Playground: uncomment the lines above (or add your own) to try your functions.")
