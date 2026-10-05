# 01 · Python warm-up (≈ 1 hour)

**Goal:** get comfortable writing plain Python again: loops, dicts, sorting, a small class, reading a file.
In Citadel coding rounds (usually CoderPad, a shared editor), you may **not have numpy or pandas**, and
the interviewer is watching how fluently you write basic Python.

## How to work
```bash
cd 01_python_warmup
python check.py          # see what's TODO / PASS / FAIL
python check.py A3       # check a single task
python exercise.py       # run the playground at the bottom of the file
```
Open `exercise.py`, replace each `raise NotImplementedError` with your code, and re-run `check.py`.
Stuck? → `hints.md` (three levels per task). Then → `solution.py`.

## Mini refresher (read in 5 minutes)

| Thing | Syntax | Notes |
|---|---|---|
| loop with index | `for i, x in enumerate(xs):` | avoids `range(len(xs))` |
| list comprehension | `[x*x for x in xs if x > 0]` | builds a new list |
| dict get-with-default | `d.get(key, 0)` | no KeyError if missing |
| auto-default dict | `from collections import defaultdict; d = defaultdict(int)` | `d[k] += 1` works immediately |
| counting | `from collections import Counter; Counter(words)` | `.most_common(3)` |
| sort by a key | `sorted(xs, key=lambda t: t["price"], reverse=True)` | returns a new list, `xs.sort()` sorts in place |
| reverse | `s[::-1]` | works on lists and strings |
| integer division / modulo | `7 // 2 == 3`, `7 % 2 == 1` | |
| string cleaning | `s.lower()`, `s.strip()`, `s.strip(".,!")`, `ch.isalnum()` | strings are immutable, so these return new strings |
| raise an error | `raise ValueError("message")` | |
| open a file | `with open(path) as f:` | file closes automatically |

**Classes in 30 seconds**
```python
class Counter2:
    def __init__(self, start):      # runs when you do Counter2(5)
        self.value = start          # attribute stored on the object
    def add(self, k):               # every method takes `self` first
        self.value += k
c = Counter2(5); c.add(2); print(c.value)   # 7
```

## Tasks
| ID | Function | Skill |
|---|---|---|
| A1 | `sum_of_squares` | loop / `sum()` |
| A2 | `evens_squared` | list comprehension |
| A3 | `count_words` | dict counting |
| B1–B3 | `mean`, `variance`, `median` | stats by hand (population vs sample variance!) |
| C1 | `total_quantity_by_ticker` | "group by" with a dict |
| C2 | `sort_trades_by_value` | `sorted` with `key=` |
| C3 | `is_palindrome` | string handling |
| D1 | `Portfolio` class | OOP, raising errors, keeping state consistent |
| D2 | `read_closes` | reading a CSV **without** pandas |

## Interviewer follow-ups (answer out loud, then open the answer)

<details><summary>1. What's the time complexity of your median? Can you do better?</summary>

Sorting costs O(n log n). Quickselect finds the k-th smallest element in O(n) on average.
For a *stream* of numbers (running median), keep two heaps (a max-heap for the lower half and a min-heap for the upper half),
which gives O(log n) per insert and O(1) to read the median.
</details>

<details><summary>2. Why divide by n−1 for sample variance?</summary>

The sample mean is fitted to the same data, so deviations from it are on average smaller than deviations from the
true mean. Dividing by n−1 makes the estimator **unbiased**: E[s²] = σ². You "used up" one degree of freedom estimating the mean.
</details>

<details><summary>3. Dict lookup complexity? List `in` complexity?</summary>

`key in dict` and `key in set` are O(1) on average (hash table). `x in list` is O(n) because it scans the list.
Converting a list to a set before many membership tests is a classic speed-up.
</details>

<details><summary>4. In Portfolio.buy, why check cash BEFORE changing anything?</summary>

That keeps state consistent: if an error is raised halfway, you must not end up having spent the cash without
recording the shares. This is "validate, then mutate". Interviewers in trading firms care about this a lot.
</details>

<details><summary>5. What's the difference between a list and a tuple? Mutable default argument bug?</summary>

Lists are mutable, tuples are immutable (and hashable, so they can be dict keys).
Bug: `def f(x, acc=[])` reuses the SAME list across calls. Use `acc=None` then `if acc is None: acc = []`.
</details>
