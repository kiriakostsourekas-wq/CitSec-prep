"""
Start an exercise again from a blank template (your current attempt is kept as a backup).

    python tools/reset.py 04        # resets 04_linear_regression/exercise.py
    python tools/reset.py all       # resets every folder

Your previous code is saved next to it as exercise_attempt_YYYYmmdd_HHMM.py,
so you can compare your first and second attempts.
"""
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "tools" / "templates"


def reset(folder):
    template = TEMPLATES / f"{folder.name}_exercise.py"
    target = folder / "exercise.py"
    if not template.exists():
        print(f"  no template for {folder.name}")
        return
    if target.exists() and target.read_text() != template.read_text():
        backup = folder / f"exercise_attempt_{datetime.now():%Y%m%d_%H%M}.py"
        shutil.copy(target, backup)
        print(f"  saved your attempt as {backup.relative_to(ROOT)}")
    shutil.copy(template, target)
    print(f"  {target.relative_to(ROOT)} is blank again")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    arg = sys.argv[1]
    folders = sorted(p for p in ROOT.glob("[0-9][0-9]_*") if p.is_dir())
    chosen = folders if arg == "all" else [p for p in folders if p.name.startswith(arg.zfill(2))]
    if not chosen:
        print(f"No folder starts with {arg!r}. Options: {[p.name[:2] for p in folders]}")
        sys.exit(1)
    for folder in chosen:
        reset(folder)


if __name__ == "__main__":
    main()
