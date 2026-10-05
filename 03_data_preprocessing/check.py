"""Run:  python check.py   |  python check.py C3   |  python check.py solution
(Don't read below - it contains the answers.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from checker import Checks, close, equal, is_type  # noqa: E402
import solution as ref  # noqa: E402  (reference, used only to build clean inputs for each task)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

checks = Checks(__file__)


def unchanged(f, df):
    before = df.copy()
    out = f(df)
    if not df.equals(before):
        raise AssertionError("you modified the input DataFrame - start with out = df.copy()")
    is_type(out, pd.DataFrame)
    return out


def stage(n):
    """Reference data after the first n cleaning steps (so each task is tested independently)."""
    df = ref.drop_duplicate_rows(ref.load_raw())
    for step in [ref.clean_income, ref.clean_city, ref.fix_age, ref.add_tenure_days, ref.one_hot][:n]:
        df = step(df)
    return df


@checks.task("A1", "load_raw", "read_csv")
def _(f):
    df = f()
    is_type(df, pd.DataFrame)
    equal(df.shape, (206, 8), "raw shape")


@checks.task("A2", "missing_report", "isna().sum()")
def _(f):
    out = f(ref.load_raw())
    is_type(out, pd.Series)
    equal(out.to_dict(), {"age": 12, "income": 11, "plan": 8}, "missing counts")
    equal(list(out.index), ["age", "income", "plan"], "order (most missing first)")


@checks.task("A3", "drop_duplicate_rows", "drop_duplicates")
def _(f):
    out = unchanged(f, ref.load_raw())
    equal(len(out), 200, "rows after removing duplicates")
    equal(list(out.index), list(range(200)), "index should be 0..199 (reset_index)")


@checks.task("B1", "clean_income", "text -> float")
def _(f):
    out = unchanged(f, stage(0))
    if not pd.api.types.is_float_dtype(out["income"]):
        raise AssertionError(f"income dtype is {out['income'].dtype}, expected float")
    equal(int(out["income"].isna().sum()), 10, "missing incomes after cleaning")
    close(out["income"].iloc[:3].values, [53700, 51700, 60400], what="first three incomes")


@checks.task("B2", "clean_city", "string normalization")
def _(f):
    out = unchanged(f, stage(1))
    equal(sorted(out["city"].unique()), ["Dubai", "London", "Paris"], "distinct cities")
    equal(int((out["city"] == "London").sum()), 62, "number of London customers")


@checks.task("B3", "fix_age", "invalid values -> NaN")
def _(f):
    out = unchanged(f, stage(2))
    equal(len(out), 200, "rows (do not delete rows!)")
    equal(int(out["age"].isna().sum()), 15, "missing ages after fixing typos (12 + 3)")
    if out["age"].max() > 100 or out["age"].min() < 18:
        raise AssertionError(f"ages still out of range: min {out['age'].min()}, max {out['age'].max()}")


@checks.task("B4", "add_tenure_days", "dates -> numbers")
def _(f):
    out = unchanged(f, stage(3))
    if "signup_date" in out.columns:
        raise AssertionError("drop the 'signup_date' column after computing tenure_days")
    equal([int(v) for v in out["tenure_days"].iloc[:3]], [1254, 795, 306], "first three tenure_days")


@checks.task("C1", "one_hot", "get_dummies")
def _(f):
    out = unchanged(f, stage(4))
    for col in ["city_London", "city_Paris", "plan_premium", "plan_unknown"]:
        if col not in out.columns:
            raise AssertionError(f"missing column {col}; you have {list(out.columns)}")
    for col in ["city", "plan", "city_Dubai", "plan_basic"]:
        if col in out.columns:
            raise AssertionError(f"column {col} should not exist (drop_first=True / original removed)")
    equal(int(out["plan_unknown"].sum()), 8, "number of plan_unknown rows")
    equal(set(np.unique(out["city_Paris"])), {0, 1}, "values of city_Paris")


@checks.task("C2", "train_test_split_df", "manual shuffle split")
def _(f):
    df = stage(5)
    train, test = f(df, test_frac=0.25, seed=0)
    equal((len(train), len(test)), (150, 50), "(train size, test size)")
    if set(train["customer_id"]) & set(test["customer_id"]):
        raise AssertionError("train and test share rows - they must be disjoint")
    exp_train, exp_test = ref.train_test_split_df(df, 0.25, 0)
    equal(sorted(test["customer_id"]), sorted(exp_test["customer_id"]),
          "test customer ids (did you use rng = np.random.default_rng(seed) and the FIRST n_test positions?)")


@checks.task("C3", "fit_preprocessor", "statistics from train")
def _(f):
    train, _ = ref.train_test_split_df(stage(5))
    params = f(train)
    is_type(params, dict)
    equal(sorted(params), sorted(ref.NUMERIC_COLS), "keys")
    exp = ref.fit_preprocessor(train)
    for col in ref.NUMERIC_COLS:
        for k in ["median", "mean", "std"]:
            close(params[col][k], exp[col][k], tol=1e-6, what=f"params['{col}']['{k}']")


@checks.task("C4", "apply_preprocessor", "impute + scale")
def _(f):
    train, test = ref.train_test_split_df(stage(5))
    params = ref.fit_preprocessor(train)
    tr = unchanged(lambda d: f(d, params), train)
    te = f(test, params)
    for col in ref.NUMERIC_COLS:
        if tr[col].isna().any() or te[col].isna().any():
            raise AssertionError(f"column {col} still has NaN")
        close(tr[col].mean(), 0, tol=1e-6, what=f"train mean of {col}")
        close(tr[col].std(), 1, tol=1e-6, what=f"train std of {col}")
    close(te["age"].values, ref.apply_preprocessor(test, params)["age"].values, tol=1e-9,
          what="test ages (must use TRAIN params)")


@checks.task("D1", "build_dataset", "end-to-end pipeline")
def _(f):
    out = f()
    equal(len(out), 4, "number of returned objects")
    X_train, X_test, y_train, y_test = out
    for name, arr in [("X_train", X_train), ("X_test", X_test), ("y_train", y_train), ("y_test", y_test)]:
        is_type(arr, np.ndarray, name)
    equal((X_train.shape, X_test.shape), ((150, 8), (50, 8)), "(X_train.shape, X_test.shape)")
    if np.isnan(X_train).any() or np.isnan(X_test).any():
        raise AssertionError("there are NaNs left in X")
    eX_train, eX_test, ey_train, ey_test = ref.build_dataset()
    close(X_test, eX_test, tol=1e-6, what="X_test (check the column order in the docstring)")
    close(y_train, ey_train, what="y_train")


if __name__ == "__main__":
    checks.run()
