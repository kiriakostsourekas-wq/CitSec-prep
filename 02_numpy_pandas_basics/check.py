"""Run:  python check.py   |  python check.py B3   |  python check.py solution
(Don't read below - the expected answers are computed here.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from checker import Checks, close, equal, is_type  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

checks = Checks(__file__)
DATA = Path(__file__).resolve().parent / "data" / "stock_prices.csv"


def fresh_df():
    return pd.read_csv(DATA, parse_dates=["date"])


def fresh_wide():
    return fresh_df().pivot(index="date", columns="ticker", values="close").sort_index()


@checks.task("A1", "filter_positive", "boolean masks")
def _(f):
    close(f(np.array([-1.0, 2.0, 0.0, 3.5])), [2.0, 3.5], what="filter_positive")
    equal(len(f(np.array([-1.0, -2.0]))), 0, "length when nothing is positive")


@checks.task("A2", "standardize", "axis + broadcasting")
def _(f):
    X = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 60.0]])
    Z = f(X)
    is_type(Z, np.ndarray)
    close(Z.mean(axis=0), [0, 0], tol=1e-9, what="column means after standardizing")
    close(Z.std(axis=0), [1, 1], tol=1e-9, what="column stds after standardizing")
    close(Z[:, 0], [-1.224744871, 0, 1.224744871], what="first column")


@checks.task("A3", "add_intercept", "hstack / column_stack")
def _(f):
    out = f(np.array([[2.0, 5.0], [3.0, 6.0], [4.0, 7.0]]))
    close(out, [[1, 2, 5], [1, 3, 6], [1, 4, 7]], what="add_intercept")


@checks.task("A4", "solve_linear_system", "np.linalg")
def _(f):
    A = np.array([[3.0, 1.0], [1.0, 2.0]])
    b = np.array([9.0, 8.0])
    close(f(A, b), [2.0, 3.0], what="solution x")


@checks.task("A5", "distances_to_point", "vectorized distances")
def _(f):
    X = np.array([[0.0, 0.0], [3.0, 4.0], [1.0, 1.0]])
    close(f(X, np.array([0.0, 0.0])), [0, 5, np.sqrt(2)], what="distances to origin")
    close(f(X, np.array([3.0, 4.0])), [5, 0, np.sqrt(13)], what="distances to (3,4)")


@checks.task("B1", "load_prices", "read_csv + datetimes")
def _(f):
    df = f()
    is_type(df, pd.DataFrame)
    equal(df.shape, (240, 4), "shape")
    equal(list(df.columns), ["date", "ticker", "close", "volume"], "columns")
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        raise AssertionError(f"'date' column has dtype {df['date'].dtype}, expected datetime64 "
                             "(look at parse_dates= or pd.to_datetime)")


@checks.task("B2", "average_close_by_ticker", "groupby")
def _(f):
    out = f(fresh_df())
    is_type(out, pd.Series)
    exp = fresh_df().groupby("ticker")["close"].mean()
    close(out.sort_index().values, exp.values, tol=1e-6, what="mean close per ticker (A,B,C,D)")


@checks.task("B3", "add_daily_returns", "groupby + pct_change")
def _(f):
    df = fresh_df()
    before = df.copy()
    out = f(df)
    is_type(out, pd.DataFrame)
    if "return" not in out.columns:
        raise AssertionError("no column named 'return' in the result")
    if not df.equals(before):
        raise AssertionError("you modified the input df - work on df.copy()")
    equal(int(out["return"].isna().sum()), 4, "number of NaN returns (one per ticker)")
    s = out.sort_values(["ticker", "date"])
    aaa = s[s.ticker == "AAA"]
    close(aaa["return"].iloc[1], aaa["close"].iloc[1] / aaa["close"].iloc[0] - 1,
          what="AAA second-day return")
    exp = df.sort_values(["ticker", "date"]).groupby("ticker")["close"].pct_change()
    close(s["return"].fillna(0).values, exp.loc[s.index].fillna(0).values, tol=1e-9,
          what="all returns")


@checks.task("B4", "to_wide", "pivot")
def _(f):
    w = f(fresh_df())
    is_type(w, pd.DataFrame)
    equal(w.shape, (60, 4), "wide shape (dates x tickers)")
    equal(sorted(w.columns), ["AAA", "BBB", "CCC", "DDD"], "columns")
    close(w.iloc[0].values, fresh_wide().iloc[0].values, what="first row of closes")


@checks.task("C1", "rolling_mean", "rolling windows")
def _(f):
    w = fresh_wide()
    out = f(w, window=5)
    equal(int(out["AAA"].isna().sum()), 4, "NaNs at the start for window=5")
    close(out["AAA"].iloc[4], w["AAA"].iloc[:5].mean(), what="first full 5-day mean of AAA")
    close(out["DDD"].iloc[-1], w["DDD"].iloc[-5:].mean(), what="last 5-day mean of DDD")


@checks.task("C2", "high_volume_days", "boolean filtering + sort")
def _(f):
    df = fresh_df()
    out = f(df, "BBB", 300_000)
    exp = df[(df.ticker == "BBB") & (df.volume >= 300_000)]
    equal(len(out), len(exp), "number of rows")
    equal(set(out["ticker"]), {"BBB"}, "tickers in result")
    equal(list(out["volume"]), sorted(exp["volume"], reverse=True), "volumes (largest first)")


@checks.task("C3", "best_day_per_ticker", "idxmax per group")
def _(f):
    df = fresh_df()
    out = f(df)
    is_type(out, dict)
    w = fresh_wide().pct_change()
    exp = {t: w[t].idxmax().strftime("%Y-%m-%d") for t in w.columns}
    equal(out, exp, "best day per ticker")


@checks.task("C4", "return_correlation", "corr of returns")
def _(f):
    w = fresh_wide()
    out = f(w)
    is_type(out, pd.DataFrame)
    exp = w.pct_change().corr()
    if np.allclose(out.values, w.corr().values):
        raise AssertionError("that's the correlation of PRICES - compute returns first")
    close(out.loc[exp.index, exp.columns].values, exp.values, tol=1e-6, what="correlation matrix")


@checks.task("D1", "annualized_sharpe", "mean/std*sqrt(252)")
def _(f):
    w = fresh_wide()
    out = f(w)
    r = w.pct_change().dropna()
    exp = r.mean() / r.std() * np.sqrt(252)
    close(out[exp.index].values, exp.values, tol=1e-6, what="Sharpe per ticker (A,B,C,D)")


@checks.task("D2", "max_drawdown", "cummax")
def _(f):
    equal(round(f(pd.Series([100.0, 120.0, 90.0, 130.0, 117.0])), 6), -0.25, "max drawdown of [100,120,90,130,117]")
    close(f(pd.Series([1.0, 2.0, 3.0])), 0.0, what="max drawdown of a rising series")
    w = fresh_wide()
    close(f(w["DDD"]), (w["DDD"] / w["DDD"].cummax() - 1).min(), what="DDD max drawdown")


if __name__ == "__main__":
    checks.run()
