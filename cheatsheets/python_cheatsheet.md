# Python cheatsheet (offline)

> **Built-in offline docs:** in a Python shell, `help(sorted)`, `help(str.strip)`, `help(dict)`, `dir(obj)`.
> For a browsable local documentation website of everything installed: `python -m pydoc -b` (works with no internet).

## Basics
```python
x = 7 // 2        # 3  integer division
x = 7 % 2         # 1  remainder
x = 2 ** 10       # 1024
abs(-3), round(3.14159, 2), min(3, 1, 2), max([4, 9])
float("3.5"), int("42"), str(42)
a, b = b, a       # swap
```

## Strings
```python
s = "  Hello, World  "
s.strip() s.lower() s.upper() s.title()
s.split(",")                 # ['  Hello', ' World  ']
"-".join(["a", "b", "c"])    # 'a-b-c'
s.replace("l", "L")
s.startswith("He"), "World" in s
ch.isalnum(), ch.isdigit(), ch.isalpha()
f"{name} has {x:.2f} dollars"   # f-string, 2 decimals
s[::-1]                      # reversed
```

## Lists
```python
xs = [3, 1, 2]
xs.append(4); xs.pop(); xs.insert(0, 9); xs.remove(9)
xs[0], xs[-1], xs[1:3], xs[::2]
len(xs), sum(xs), sorted(xs), sorted(xs, reverse=True)
xs.sort()                                 # in place, returns None!
sorted(trades, key=lambda t: t["price"])  # sort by a field
[x * x for x in xs if x > 1]              # comprehension
list(zip([1, 2], ["a", "b"]))             # [(1,'a'), (2,'b')]
for i, x in enumerate(xs): ...
any(x > 2 for x in xs), all(x > 0 for x in xs)
```

## Dicts & sets
```python
d = {"AAA": 10, "BBB": 5}
d["CCC"] = 7; d.get("ZZZ", 0); "AAA" in d; del d["BBB"]
for k, v in d.items(): ...
{k: v * 2 for k, v in d.items()}           # dict comprehension
max(d, key=d.get)                          # key with the largest value

from collections import defaultdict, Counter, deque
g = defaultdict(list); g["x"].append(1)    # no KeyError
c = Counter("mississippi"); c.most_common(2)   # [('i', 4), ('s', 4)]
q = deque(maxlen=3); q.append(1); q.popleft()  # O(1) both ends

s = {1, 2, 3}; s.add(4); s & {2, 9}; s | {9}; s - {1}
```

## Heaps (priority queues), bisect
```python
import heapq
h = []; heapq.heappush(h, 5); heapq.heappush(h, 1)
heapq.heappop(h)          # 1 (smallest first). Max-heap: push -x
h[0]                      # peek at the smallest
heapq.nlargest(3, xs), heapq.nsmallest(3, xs, key=...)

import bisect
bisect.bisect_left(sorted_list, x)   # insertion index, O(log n)
```

## Functions, lambdas, errors
```python
def f(x, k=2, *args, **kwargs):
    """Docstring."""
    return x ** k

square = lambda x: x * x

try:
    risky()
except ValueError as e:
    print("bad value:", e)
finally:
    cleanup()

raise ValueError("message")
assert x > 0, "x must be positive"
```

## Classes
```python
class Account:
    fee = 1.0                       # class attribute (shared)
    def __init__(self, owner, cash=0):
        self.owner = owner          # instance attributes
        self.cash = cash
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.cash += amount
    def __repr__(self):             # what print() shows
        return f"Account({self.owner}, {self.cash})"

a = Account("K", 100); a.deposit(50); print(a)
```

## Files
```python
with open("file.txt") as f:          # closes automatically
    for line in f:
        print(line.strip())

import csv
with open("data.csv", newline="") as f:
    for row in csv.DictReader(f):    # row = dict of STRINGS
        price = float(row["close"])
```

## Itertools & math
```python
import itertools, math
itertools.product(range(1, 7), repeat=2)   # all pairs of dice
itertools.combinations([1, 2, 3], 2)       # (1,2) (1,3) (2,3)
itertools.permutations([1, 2, 3])
math.comb(5, 2), math.factorial(5), math.sqrt(2), math.log(10), math.inf
```

## Common pitfalls
- `xs.sort()` returns `None`; `sorted(xs)` returns a new list.
- Mutable default argument: `def f(acc=[])` shares one list across calls → use `acc=None`.
- `a = b` for lists does NOT copy → `a = b.copy()` or `list(b)`.
- Integer vs float division: `/` always gives a float, `//` floors.
- Floating point: `0.1 + 0.2 != 0.3` → compare with `math.isclose`.
