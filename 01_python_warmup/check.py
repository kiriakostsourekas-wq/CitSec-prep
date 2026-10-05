"""Run:  python check.py        (or: python check.py A2   /   python check.py solution)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from checker import Checks, close, equal, is_type  # noqa: E402

checks = Checks(__file__)
TRADES = [
    {"ticker": "A", "qty": 5, "price": 1.0},
    {"ticker": "B", "qty": 2, "price": 3.0},
    {"ticker": "A", "qty": 1, "price": 20.0},
]


@checks.task("A1", "sum_of_squares", "loop / generator")
def _(f):
    equal(f([1, 2, 3]), 14, "sum_of_squares([1,2,3])")
    equal(f([]), 0, "sum_of_squares([])")
    equal(f([-2, 5]), 29, "sum_of_squares([-2,5])")


@checks.task("A2", "evens_squared", "list comprehension")
def _(f):
    equal(f([1, 2, 3, 4, 5, 6]), [4, 16, 36], "evens_squared([1..6])")
    equal(f([1, 3]), [], "evens_squared([1,3])")
    equal(f([-2, 0]), [4, 0], "evens_squared([-2,0])")


@checks.task("A3", "count_words", "dict counting")
def _(f):
    equal(f("The cat. The DOG!"), {"the": 2, "cat": 1, "dog": 1}, "count_words")
    equal(f("buy buy SELL, hold? buy"), {"buy": 3, "sell": 1, "hold": 1}, "count_words")


@checks.task("B1", "mean", "average")
def _(f):
    close(f([1, 2, 3, 4]), 2.5, what="mean([1,2,3,4])")
    close(f([10]), 10, what="mean([10])")


@checks.task("B2", "variance", "population vs sample")
def _(f):
    close(f([1, 2, 3, 4]), 1.25, what="population variance")
    close(f([1, 2, 3, 4], sample=True), 5 / 3, what="sample variance")
    close(f([7, 7, 7]), 0, what="variance of constant list")


@checks.task("B3", "median", "sorting")
def _(f):
    data = [3, 1, 2]
    equal(f(data), 2, "median([3,1,2])")
    equal(data, [3, 1, 2], "your function must not modify the input list; list")
    close(f([4, 1, 3, 2]), 2.5, what="median([4,1,3,2])")


@checks.task("C1", "total_quantity_by_ticker", "group-by with a dict")
def _(f):
    equal(f(TRADES), {"A": 6, "B": 2}, "totals")
    equal(f([]), {}, "totals of empty list")


@checks.task("C2", "sort_trades_by_value", "sorted(key=...)")
def _(f):
    original = list(TRADES)
    out = f(TRADES)
    equal([t["price"] * t["qty"] for t in out], [20.0, 6.0, 5.0], "notional values in order")
    equal(TRADES, original, "the original list must not change; list")


@checks.task("C3", "is_palindrome", "strings")
def _(f):
    equal(f("A man, a plan, a canal: Panama"), True, "classic palindrome")
    equal(f("Citadel"), False, "'Citadel'")
    equal(f(""), True, "empty string")
    equal(f("No 'x' in Nixon"), True, "'No x in Nixon'")


@checks.task("D1", "Portfolio", "class with methods + errors")
def _(Portfolio):
    p = Portfolio(cash=1000)
    p.buy("AAA", 5, 100)
    p.sell("AAA", 2, 110)
    equal(p.position("AAA"), 3, "position after buy 5 / sell 2")
    equal(p.position("ZZZ"), 0, "position of a ticker never traded")
    close(p.cash, 720, what="cash")
    close(p.value({"AAA": 120}), 1080, what="value")
    for action, args in [("buy", ("BBB", 100, 100)), ("sell", ("AAA", 10, 1))]:
        try:
            getattr(p, action)(*args)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{action}{args} should raise ValueError")
    close(p.cash, 720, what="cash must be unchanged after a rejected trade; cash")


@checks.task("D2", "read_closes", "csv module + file I/O")
def _(f):
    out = f()
    is_type(out, dict)
    equal(sorted(out), ["AAA", "BBB", "CCC", "DDD"], "tickers")
    equal(len(out["AAA"]), 60, "number of AAA closes")
    is_type(out["AAA"][0], float, "first AAA close")
    close(out["AAA"][0], 98.46, what="first AAA close")


if __name__ == "__main__":
    checks.run()
