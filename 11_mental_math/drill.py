"""
Timed mental-math drill (offline). No calculator, no paper: that's the point.

    python drill.py                    # 8 minutes or 80 questions, mixed topics
    python drill.py --minutes 3        # short session
    python drill.py --topics mul pct   # only some topics (see TOPICS below)
    python drill.py --history          # show your past scores

Answers: type a number. Decimals are accepted within ±0.005 (e.g. 0.375, .375).
Press Enter on an empty line to skip. Your scores are saved in history.csv in this folder.
"""
import argparse
import csv
import random
import time
from datetime import datetime
from pathlib import Path

HISTORY = Path(__file__).resolve().parent / "history.csv"


def q_mul(rng):
    kind = rng.random()
    if kind < 0.4:
        a, b = rng.randint(12, 99), rng.randint(3, 9)
    elif kind < 0.8:
        a, b = rng.randint(11, 49), rng.randint(11, 29)
    else:
        a, b = rng.randint(101, 999), rng.randint(2, 9)
    return f"{a} × {b}", a * b


def q_div(rng):
    if rng.random() < 0.6:
        b, c = rng.randint(3, 19), rng.randint(3, 60)
        return f"{b * c} ÷ {b}", c
    b = rng.choice([4, 8, 5, 20, 25, 40])
    a = rng.randint(1, 4 * b)
    return f"{a} ÷ {b}", a / b


def q_add(rng):
    a, b = round(rng.uniform(10, 99), 1), round(rng.uniform(10, 99), 1)
    if rng.random() < 0.5:
        return f"{a} + {b}", round(a + b, 1)
    a, b = max(a, b), min(a, b)
    return f"{a} − {b}", round(a - b, 1)


def q_pct(rng):
    p = rng.choice([5, 10, 12.5, 15, 20, 25, 30, 40, 60, 75, 2.5, 120])
    n = rng.choice([40, 80, 120, 160, 240, 320, 360, 480, 640, 800, 1200])
    return f"{p:g}% of {n}", p * n / 100


def q_frac(rng):
    d = rng.choice([3, 6, 7, 8, 9, 11, 12, 16])
    k = rng.randint(1, d - 1)
    return f"{k}/{d} as a decimal (3 d.p.)", round(k / d, 3)


def q_sq(rng):
    n = rng.choice(list(range(11, 33)) + [45, 55, 65, 75, 85, 95])
    return f"{n}²", n * n


def q_ev(rng):
    kind = rng.random()
    if kind < 0.33:
        p = rng.choice([0.1, 0.2, 0.25, 0.4, 0.6, 0.75])
        a, b = rng.randint(1, 20) * 5, rng.randint(0, 10) * 2
        return f"EV: {p:g} chance of {a}, else {b}", round(p * a + (1 - p) * b, 2)
    if kind < 0.66:
        n = rng.randint(2, 6)
        return f"expected sum of {n} dice", 3.5 * n
    s = rng.choice([4, 6, 8, 10, 12, 20])
    return f"expected value of one fair d{s} (1..{s})", (s + 1) / 2


TOPICS = {"mul": q_mul, "div": q_div, "add": q_add, "pct": q_pct, "frac": q_frac, "sq": q_sq, "ev": q_ev}


def correct(ans, truth):
    return abs(ans - truth) <= (1e-9 if float(truth).is_integer() else 0.005 + 1e-9)


def run(minutes, n, topics, seed):
    rng = random.Random(seed)
    gens = [TOPICS[t] for t in topics]
    print(f"\n{n} questions or {minutes} minutes, whichever comes first. Topics: {', '.join(topics)}.")
    try:
        input("Press Enter to start...")
    except EOFError:
        pass
    start = time.time()
    results, misses = [], []
    for i in range(1, n + 1):
        left = minutes * 60 - (time.time() - start)
        if left <= 0:
            print("\nTime!")
            break
        gen = rng.choice(gens)
        text, truth = gen(rng)
        try:
            raw = input(f"[{int(left):>3}s] Q{i}: {text} = ").strip().replace(",", "")
        except EOFError:
            break
        if raw.lower() in {"q", "quit"}:
            break
        try:
            ok = raw != "" and correct(float(raw), truth)
        except ValueError:
            ok = False
        if time.time() - start > minutes * 60:
            print("  (answered after the bell, not counted)")
            break
        results.append((gen.__name__[2:], ok))
        if not ok:
            misses.append((text, raw, truth))
    elapsed = time.time() - start
    done = len(results)
    right = sum(ok for _, ok in results)
    print(f"\nScore: {right}/{done} correct in {elapsed / 60:.1f} min "
          f"({right / max(done, 1):.0%} accuracy, {done / max(elapsed, 1) * 60:.1f} questions/min)")
    by_topic = {}
    for t, ok in results:
        a, b = by_topic.get(t, (0, 0))
        by_topic[t] = (a + ok, b + 1)
    print("By topic: " + ", ".join(f"{t} {a}/{b}" for t, (a, b) in sorted(by_topic.items())))
    if misses:
        print("Missed:")
        for text, raw, truth in misses[:15]:
            print(f"  {text} = {truth:g}   (you: {raw or 'skip'})")
    new = not HISTORY.exists()
    with open(HISTORY, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["when", "topics", "correct", "answered", "minutes"])
        w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), " ".join(topics), right, done, round(elapsed / 60, 2)])
    print(f"(saved to {HISTORY.name})")


def show_history():
    if not HISTORY.exists():
        print("No history yet.")
        return
    with open(HISTORY) as f:
        rows = list(csv.DictReader(f))
    for r in rows[-20:]:
        print(f"{r['when']}  {r['correct']:>3}/{r['answered']:<3} in {r['minutes']} min   [{r['topics']}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=8)
    ap.add_argument("--n", type=int, default=80)
    ap.add_argument("--topics", nargs="+", choices=list(TOPICS), default=list(TOPICS))
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--history", action="store_true")
    args = ap.parse_args()
    if args.history:
        show_history()
    else:
        run(args.minutes, args.n, args.topics, args.seed)


if __name__ == "__main__":
    main()
