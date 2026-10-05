"""Run:  python check.py   |  python check.py S4   |  python check.py solution
(Don't read below - it contains the answers.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from checker import Checks, close, equal, is_type  # noqa: E402
import solution as ref  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

checks = Checks(__file__)
DF = ref.add_temp_squared(ref.load_and_clean())
TR, TE = ref.time_split(DF)
F = ref.FEATURES


@checks.task("S1", "load_and_clean", "dates, interpolation, dummies")
def _(f):
    df = f()
    is_type(df, pd.DataFrame)
    equal(len(df), 365, "rows")
    for col in ["t", "weather_cloudy", "weather_rain"]:
        if col not in df.columns:
            raise AssertionError(f"missing column '{col}'")
    if df[["temp_c", "humidity"]].isna().any().any():
        raise AssertionError("temp_c / humidity still contain NaN")
    if not df["date"].is_monotonic_increasing:
        raise AssertionError("sort by date")
    equal(int(df["t"].iloc[-1]), 364, "t on the last day")
    close(df["temp_c"].values, DF["temp_c"].values, tol=1e-6, what="temp_c (linear interpolation)")


@checks.task("S2", "time_split", "no shuffling!")
def _(f):
    tr, te = f(DF)
    equal((len(tr), len(te)), (274, 91), "(train days, test days)")
    if tr["date"].max() >= te["date"].min():
        raise AssertionError("train must be entirely BEFORE test (did you shuffle?)")


@checks.task("S3", "baseline_rmse", "the number to beat")
def _(f):
    close(f(TR, TE), ref.baseline_rmse(TR, TE), tol=1e-6, what="baseline RMSE")


@checks.task("S4", "linear_fit_eval", "rmse + bias")
def _(f):
    for feats in (F, F + ["t"]):
        out = f(TR, TE, feats)
        equal(len(out), 2, "number of returned values")
        close(out, ref.linear_fit_eval(TR, TE, feats), tol=1e-4, what=f"(rmse, bias) with {feats[-1]!r} last")


@checks.task("S5", "add_temp_squared", "feature engineering")
def _(f):
    base = ref.load_and_clean()
    out = f(base)
    if "temp_sq" in base.columns:
        raise AssertionError("work on a copy")
    close(out["temp_sq"].values, base["temp_c"].values ** 2, what="temp_sq")


@checks.task("S6", "tree_rmse", "DecisionTreeRegressor")
def _(f):
    close(f(TR, TE, F, 4), ref.tree_rmse(TR, TE, F, 4), tol=1e-4, what="tree depth-4 RMSE")


@checks.task("S7", "busy_day_auc", "classification twist")
def _(f):
    close(f(TR, TE, F + ["temp_sq"]), ref.busy_day_auc(TR, TE, F + ["temp_sq"]), tol=1e-4, what="test AUC")


if __name__ == "__main__":
    checks.run()
