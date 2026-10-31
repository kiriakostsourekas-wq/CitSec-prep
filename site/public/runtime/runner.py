"""
Bridge between the website and the prep kit's own files. Runs inside Pyodide (Python in the browser).

The worker writes a module's files under /prep/<folder>/ (exactly the repo layout), then calls:
    run_script(folder, filename)          -> run exercise.py / solution.py as __main__ (the playground)
    run_checks(folder, which, wanted)     -> the same checks as `python check.py`, but as JSON for the UI
"""
import base64
import contextlib
import importlib
import io
import json
import os
import runpy
import sys
import traceback
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

ROOT = Path("/prep")
_BASE_PATH = list(sys.path)
_KIT_MODULES = ("exercise", "solution", "check", "checker")


def _fresh(folder):
    """Forget previously imported kit modules (every folder has an exercise.py) and cd into the folder."""
    for name in _KIT_MODULES:
        sys.modules.pop(name, None)
    sys.path[:] = [str(folder), str(ROOT / "tools")] + _BASE_PATH
    os.chdir(folder)
    importlib.invalidate_caches()


def _user_traceback(exc, filename):
    """Traceback limited to the frames in the user's file (falls back to the full one)."""
    frames = traceback.extract_tb(exc.__traceback__)
    mine = [f for f in frames if f.filename.endswith(filename)]
    lines = traceback.format_list(mine or frames)
    lines += traceback.format_exception_only(type(exc), exc)
    return "Traceback (most recent call last):\n" + "".join(lines)


def _collect_images(folder, before):
    images = []
    if "matplotlib.pyplot" in sys.modules:
        plt = sys.modules["matplotlib.pyplot"]
        for num in plt.get_fignums():
            buf = io.BytesIO()
            plt.figure(num).savefig(buf, format="png", dpi=110, bbox_inches="tight")
            images.append({"name": f"figure {num}", "png": base64.b64encode(buf.getvalue()).decode()})
        plt.close("all")
    for path in sorted(folder.glob("*.png")):
        if path.name not in before:
            images.append({"name": path.name, "png": base64.b64encode(path.read_bytes()).decode()})
            path.unlink()
    return images


def run_script(folder, filename):
    """Run a file as __main__. Its prints stream to the console through Pyodide's stdout hook."""
    folder = ROOT / folder
    _fresh(folder)
    before = {p.name for p in folder.glob("*.png")}
    error = None
    try:
        runpy.run_path(str(folder / filename), run_name="__main__")
    except SystemExit:
        pass
    except BaseException as exc:  # noqa: BLE001 - show the user whatever went wrong
        error = _user_traceback(exc, filename)
    return json.dumps({"error": error, "images": _collect_images(folder, before)})


def run_checks(folder, which="exercise", wanted=None):
    """Mirror of Checks.run in tools/checker.py, returning one result per task instead of printing."""
    folder = ROOT / folder
    _fresh(folder)
    wanted = {w.upper() for w in (wanted or [])}
    filename = f"{which}.py"

    try:
        check = importlib.import_module("check")
    except BaseException as exc:  # noqa: BLE001
        return json.dumps({"fatal": "Could not load check.py:\n" + _user_traceback(exc, "check.py")})

    sink = io.StringIO()
    try:
        with contextlib.redirect_stdout(sink):
            module = importlib.import_module(which)
    except BaseException as exc:  # noqa: BLE001
        return json.dumps({"fatal": f"Could not even import {filename}. There is a syntax/import error:\n"
                                    + _user_traceback(exc, filename)})

    results = []
    for task_id, func_name, title, fn in check.checks.items:
        if wanted and task_id.upper() not in wanted:
            continue
        res = {"id": task_id, "func": func_name, "title": title, "status": "PASS", "message": ""}
        func = getattr(module, func_name, None)
        out = io.StringIO()
        if func is None:
            res.update(status="TODO", message=f"function `{func_name}` not found")
        else:
            try:
                with contextlib.redirect_stdout(out):
                    fn(func)
            except NotImplementedError:
                res["status"] = "TODO"
            except AssertionError as exc:
                res.update(status="FAIL", message=str(exc))
            except BaseException as exc:  # noqa: BLE001
                tb = traceback.extract_tb(exc.__traceback__)
                where = next((f for f in reversed(tb) if f.filename.endswith(filename)), tb[-1])
                res.update(status="ERROR",
                           message=f"{type(exc).__name__}: {exc}\n(at {Path(where.filename).name} "
                                   f"line {where.lineno}: {where.line})",
                           line=where.lineno if where.filename.endswith(filename) else None)
        res["output"] = out.getvalue()[-4000:]
        results.append(res)
    return json.dumps({"results": results, "importOutput": sink.getvalue()[-4000:]})
