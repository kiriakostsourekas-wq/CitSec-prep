"""
01 - PYTHON WARM-UP  - REFERENCE SOLUTION
Only look here after you tried (or to compare styles after you passed).
"""
import csv
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "02_numpy_pandas_basics" / "data" / "stock_prices.csv"


# ---------------- PART A ----------------
def sum_of_squares(nums):
    # generator expression inside sum(): no intermediate list is built
    return sum(x * x for x in nums)


def evens_squared(nums):
    return [x * x for x in nums if x % 2 == 0]


def count_words(text):
    counts = {}
    for raw in text.split():                 # split() with no args splits on any whitespace
        word = raw.lower().strip(".,!?")     # strip removes these chars from BOTH ends
        if word:                             # skip things like "!" that became ""
            counts[word] = counts.get(word, 0) + 1
    return counts
    # Alternative: from collections import Counter; return dict(Counter(words))


# ---------------- PART B ----------------
def mean(xs):
    return sum(xs) / len(xs)


def variance(xs, sample=False):
    m = mean(xs)
    ss = sum((x - m) ** 2 for x in xs)       # sum of squared deviations
    return ss / (len(xs) - 1 if sample else len(xs))


def median(xs):
    s = sorted(xs)                            # sorted() returns a NEW list (xs unchanged)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


# ---------------- PART C ----------------
def total_quantity_by_ticker(trades):
    totals = defaultdict(int)                 # missing keys start at 0
    for t in trades:
        totals[t["ticker"]] += t["qty"]
    return dict(totals)


def sort_trades_by_value(trades):
    return sorted(trades, key=lambda t: t["price"] * t["qty"], reverse=True)


def is_palindrome(s):
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]           # [::-1] reverses a list/string
    # Interview follow-up: O(1) extra memory version uses two pointers i, j
    # moving inwards and skipping non-alphanumeric characters.


# ---------------- PART D ----------------
class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.holdings = {}                    # ticker -> qty

    def buy(self, ticker, qty, price):
        cost = qty * price
        if cost > self.cash:
            raise ValueError(f"Not enough cash: need {cost}, have {self.cash}")
        self.cash -= cost
        self.holdings[ticker] = self.holdings.get(ticker, 0) + qty

    def sell(self, ticker, qty, price):
        if qty > self.position(ticker):
            raise ValueError(f"Cannot sell {qty} {ticker}: only hold {self.position(ticker)}")
        self.holdings[ticker] -= qty
        self.cash += qty * price

    def position(self, ticker):
        return self.holdings.get(ticker, 0)

    def value(self, prices):
        return self.cash + sum(qty * prices[t] for t, qty in self.holdings.items() if qty)


def read_closes(path=DATA):
    closes = defaultdict(list)
    with open(path, newline="") as f:          # `with` closes the file automatically
        reader = csv.DictReader(f)             # each row is a dict keyed by the header
        for row in reader:
            closes[row["ticker"]].append(float(row["close"]))  # csv gives strings!
    return dict(closes)


if __name__ == "__main__":
    print(count_words("The cat. The DOG!"))
    p = Portfolio(1000)
    p.buy("AAA", 5, 100)
    p.sell("AAA", 2, 110)
    print(p.cash, p.position("AAA"), p.value({"AAA": 120}))
    closes = read_closes()
    print({t: len(v) for t, v in closes.items()})
