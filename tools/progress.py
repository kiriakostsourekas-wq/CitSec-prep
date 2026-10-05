"""
Progress dashboard: runs every folder's check.py and prints a summary.

    python tools/progress.py            # your progress (exercise.py files)
    python tools/progress.py solution   # sanity check: all reference solutions should pass
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    which = ["solution"] if "solution" in sys.argv[1:] else []
    folders = sorted(p.parent for p in ROOT.glob("[0-9][0-9]_*/check.py"))
    print(f"\n{'folder':<30}{'passed':>8}{'total':>7}   progress")
    grand_pass = grand_total = 0
    for folder in folders:
        res = subprocess.run([sys.executable, "check.py", *which], cwd=folder,
                             capture_output=True, text=True, timeout=600)
        m = re.search(r"(\d+)/(\d+) passed", res.stdout)
        if not m:
            print(f"{folder.name:<30}{'ERROR':>8}        (run `python check.py` inside it to see why)")
            continue
        passed, total = int(m.group(1)), int(m.group(2))
        grand_pass += passed
        grand_total += total
        bar = "#" * passed + "." * (total - passed)
        print(f"{folder.name:<30}{passed:>8}{total:>7}   [{bar}]")
    if grand_total:
        print(f"\n{'TOTAL':<30}{grand_pass:>8}{grand_total:>7}   {100 * grand_pass / grand_total:.0f}%\n")


if __name__ == "__main__":
    main()
