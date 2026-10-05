"""
Tiny offline test runner used by every `check.py` in this folder.

You never need to edit this file. From inside an exercise folder:

    python check.py            -> checks YOUR code in exercise.py
    python check.py A2         -> checks only task A2 (several allowed: A1 B2)
    python check.py solution   -> checks the reference solution.py
"""
import importlib
import math
import sys
import traceback
from pathlib import Path

USE_COLOR = sys.stdout.isatty()


def _c(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


GREEN = lambda s: _c(s, "32")
RED = lambda s: _c(s, "31")
YELLOW = lambda s: _c(s, "33")
BOLD = lambda s: _c(s, "1")
DIM = lambda s: _c(s, "2")


def _require_environment():
    """Fail early with instructions if the prep folder's .venv is not being used."""
    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
        import sklearn  # noqa: F401
    except Exception:
        venv = Path(__file__).resolve().parent.parent / ".venv"
        print(RED("\nThis Python can't import numpy/pandas/scikit-learn.\n"))
        print(f"You are running: {sys.executable}")
        print("Use the prep folder's own environment instead. In the terminal, run once per window:\n")
        print(f"    source {venv}/bin/activate\n")
        print("(the prompt then starts with '(.venv)'). Then run `python check.py` again.")
        print("Details: see 'Setup' in the README.md at the top of the prep folder.\n")
        sys.exit(1)


_require_environment()   # runs as soon as a check.py imports this module


class Checks:
    """Collects checks with the @checks.task(...) decorator, then runs them."""

    def __init__(self, folder_file):
        self.folder = Path(folder_file).resolve().parent
        self.items = []

    def task(self, task_id, func_name, title):
        def deco(fn):
            self.items.append((task_id, func_name, title, fn))
            return fn
        return deco

    # ------------------------------------------------------------------
    def run(self):
        args = sys.argv[1:]
        which = "solution" if "solution" in args else "exercise"
        wanted = {a.upper() for a in args if a != "solution"}

        sys.path.insert(0, str(self.folder))
        try:
            module = importlib.import_module(which)
        except Exception:
            print(RED(f"Could not even import {which}.py - there is a syntax/import error:\n"))
            traceback.print_exc()
            sys.exit(1)

        print(BOLD(f"\nChecking {which}.py in {self.folder.name}\n"))
        counts = {"PASS": 0, "FAIL": 0, "TODO": 0}
        for task_id, func_name, title, fn in self.items:
            if wanted and task_id.upper() not in wanted:
                continue
            label = f"[{task_id}] {func_name:<28} {DIM(title)}"
            func = getattr(module, func_name, None)
            if func is None:
                print(f"  {YELLOW('TODO')}  {label}\n        function `{func_name}` not found")
                counts["TODO"] += 1
                continue
            try:
                fn(func)
                print(f"  {GREEN('PASS')}  {label}")
                counts["PASS"] += 1
            except NotImplementedError:
                print(f"  {YELLOW('TODO')}  {label}")
                counts["TODO"] += 1
            except AssertionError as e:
                print(f"  {RED('FAIL')}  {label}\n        {e}")
                counts["FAIL"] += 1
            except Exception as e:
                tb = traceback.extract_tb(e.__traceback__)
                where = next((f for f in reversed(tb) if which in f.filename), tb[-1])
                print(f"  {RED('ERROR')} {label}\n        {type(e).__name__}: {e}"
                      f"\n        (at {Path(where.filename).name} line {where.lineno}: {where.line})")
                counts["FAIL"] += 1

        total = sum(counts.values())
        print(f"\n  {GREEN(str(counts['PASS']))}/{total} passed, "
              f"{RED(str(counts['FAIL']))} failing, {YELLOW(str(counts['TODO']))} not started")
        if counts["PASS"] == total and total:
            print(GREEN("  All done here. Read the 'Interviewer follow-ups' in README.md next!\n"))
        else:
            print(DIM("  Stuck? Open hints.md (hints are folded, open one at a time).\n"))
        return counts


# ----------------------------------------------------------------------
# helpers used inside checks
# ----------------------------------------------------------------------
def close(actual, expected, tol=1e-6, what="value"):
    """Assert two numbers (or arrays) are close, with a readable message."""
    import numpy as np
    a = np.asarray(actual, dtype=float)
    e = np.asarray(expected, dtype=float)
    if a.shape != e.shape:
        raise AssertionError(f"{what}: expected shape {e.shape}, got shape {a.shape}")
    if not np.allclose(a, e, atol=tol, rtol=tol):
        if a.size == 1:
            raise AssertionError(f"{what}: expected {float(e):.6g}, got {float(a):.6g}")
        raise AssertionError(f"{what}: expected\n          {np.round(e, 4)}\n        got\n          {np.round(a, 4)}")


def equal(actual, expected, what="value"):
    if actual != expected:
        raise AssertionError(f"{what}: expected {expected!r}, got {actual!r}")


def between(x, lo, hi, what="value"):
    if x is None or (isinstance(x, float) and math.isnan(x)) or not (lo <= x <= hi):
        raise AssertionError(f"{what}: expected something between {lo} and {hi}, got {x!r}")


def is_type(x, typ, what="return value"):
    if not isinstance(x, typ):
        name = typ.__name__ if isinstance(typ, type) else " or ".join(t.__name__ for t in typ)
        raise AssertionError(f"{what}: expected type {name}, got {type(x).__name__}"
                             + (" (did you forget to `return`?)" if x is None else ""))
