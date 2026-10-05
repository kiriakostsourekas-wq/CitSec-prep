# Citadel final-round prep: Python + ML practice (offline after setup)

Hands-on practice for the final round: **Python fluency → data handling → linear regression → logistic regression →
kNN / Naive Bayes → decision trees**, plus probability-by-simulation, coding-interview algorithms, a timed mock interview,
and a guide to the interview itself (format, ML/stats questions, CV deep dive & behavioural).

Everything is inside this folder: datasets, hints, solutions, notes and cheatsheets.
After a one-time setup (which installs 4 Python packages), **no internet is needed.**

---

## 1. Setup

**Once (needs internet):** create a local environment inside the folder with Python 3.11 or newer.
```bash
git clone https://github.com/kiriakostsourekas-wq/CitSec-prep.git
```
```bash
cd CitSec-prep
```
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```
(Windows: `py -m venv .venv` then `.venv\Scripts\pip install -r requirements.txt`.)
Using a dedicated `.venv` avoids clashes with whatever else is installed on your machine. For example, a mixed Anaconda
install with NumPy 2 next to older pandas builds crashes on `import pandas`.

**Every new terminal window (5 seconds):**
```bash
source .venv/bin/activate
```
(Windows: `.venv\Scripts\activate`.) Your prompt now starts with `(.venv)`. Check it works:
```bash
python tools/progress.py
```
You should see a table with every folder at 0. If you forget to activate, the checkers tell you what to do.

**VS Code:** open the folder. It's already configured (`.vscode/settings.json`) to use `.venv/bin/python`.
If it asks, pick the interpreter `./.venv/bin/python`.

---

## 2. How every exercise folder works

```
04_linear_regression/
├── README.md     ← concept notes + task list + "Interviewer follow-ups" (folded answers)
├── exercise.py   ← YOU write code here: replace each `raise NotImplementedError`
├── check.py      ← run it to test your code (PASS / FAIL / TODO with explanations)
├── hints.md      ← stuck? 2–3 progressive hints per task, folded so you see one at a time
├── solution.py   ← reference solution with comments (run it to see a full analysis)
└── data/         ← the small dataset for this topic
```

The loop:
```bash
cd 04_linear_regression
python exercise.py        # playground at the bottom of the file: explore the data first
python check.py           # test everything
python check.py B2        # test one task
python check.py solution  # (see that the reference passes)
```

**Rules of thumb**
1. Read the folder's `README.md` concept notes first (10 min).
2. Tasks go A (easy) → B → C → D (Citadel-style / bonus). Do them in order.
3. Stuck for ~10 minutes? Open **one** hint in `hints.md`, then try again.
4. After a task passes, compare with `solution.py`. Different code is fine; understand any differences.
5. When the folder is done, answer the **Interviewer follow-ups out loud** before opening each answer. This is what the real interview tests.
6. Don't read `check.py`, because it contains the answers.

**Redo an exercise from scratch** (your attempt is backed up automatically):
```bash
python tools/reset.py 04
```
**See your overall progress:**
```bash
python tools/progress.py
```

---

## 3. Folder map

| Folder | Topic | Dataset | Time |
|---|---|---|---|
| `00_interview_guide/` | format, strategy, **ML/stats Q&A**, **CV deep dive** | — | 1 h (spread out) |
| `01_python_warmup/` | loops, dicts, sorting, a class, csv, all without libraries | (stock CSV) | 1 h |
| `02_numpy_pandas_basics/` | arrays, axis, broadcasting; DataFrames, groupby, pivot, rolling; Sharpe, drawdown | `stock_prices.csv` | 1.5–2 h |
| `03_data_preprocessing/` | messy data → clean matrix, **no leakage** | `customers_raw.csv` | 1.5 h |
| `04_linear_regression/` | OLS, gradient descent, ridge, standard errors, **duplicate-data question** | `apartments.csv` | 2 h |
| `05_logistic_regression/` | sigmoid, log-loss, GD, precision/recall, ROC-AUC, odds ratios | `loan_default.csv` | 2 h |
| `06_knn_classification/` | kNN, scaling, k-fold CV by hand, *bonus* Naive Bayes | `fruits.csv` | 1–1.5 h |
| `07_decision_tree/` | Gini/entropy, best split, recursive tree, overfitting vs depth | `churn.csv` | 2–2.5 h |
| `08_probability_simulation/` | exact vs Monte Carlo + 12 interview probability questions | — | 1–1.5 h |
| `09_algorithms/` | moving average, two-sum, DP, heaps, *bonus* order book | — | 1.5–2 h |
| `10_mock_interview/` | **timed 60-min end-to-end ML case** with interviewer script | `bike_rentals.csv` | 1 h |
| `cheatsheets/` | Python, numpy, pandas, sklearn, formula sheet | — | reference |
| `tools/` | checker, progress, reset, dataset generator | — | — |

All datasets are small (180–400 rows) and simulated from known rules, so you can check whether your model recovered the truth
(see `tools/make_datasets.py` *after* finishing a folder).

---

## 4. Study plan (≈ 13 h core + bonuses)

| Session | Work | Time |
|---|---|---|
| **1** | `00_interview_guide/README.md` · `01_python_warmup` · `02` part A (numpy) | 3 h |
| **2** | `02` parts B–D (pandas) · `03_data_preprocessing` | 3 h |
| **3** | `04_linear_regression` (+ its follow-ups!) · first pass of `00/cv_and_behavioral.md` | 3 h |
| **4** | `05_logistic_regression` · `06_knn` (A–C) | 3 h |
| **5** | `07_decision_tree` · `08_probability_simulation` | 3.5 h |
| **6** | `09_algorithms` (A–C) · `10_mock_interview` (timed) · `00/ml_stats_questions.md` | 3 h |
| extra | bonuses (`06` D2–D3, `09` D1–D2) · `reset.py` and redo whatever felt hardest · redo the mock | as available |

**Only ~6 hours?** `00` guide + CV file → `04` → `05` → `07` (A–C) → `09` A1–A3 → `08` README questions → follow-ups in 04/05/07.

**The evening before:** the checklist in `00_interview_guide/README.md` §5.

---

## 5. Offline help when you're stuck
1. `hints.md` in the folder (progressive), then `solution.py` (commented).
2. `cheatsheets/`: `python_cheatsheet.md`, `numpy_cheatsheet.md`, `pandas_cheatsheet.md`, `sklearn_cheatsheet.md`, `ml_formulas.md`.
3. Built-in docs: in Python, `help(np.argsort)`, `help(pd.DataFrame.groupby)`, `help(LogisticRegression)`.
4. A full local documentation browser for every installed library (no internet):
   ```bash
   python -m pydoc -b
   ```
5. Error messages: read the **last line** first (`KeyError: 'income'` = that column doesn't exist; check spelling with `df.columns`).
   `print(x.shape)`, `print(type(x))` and `print(df.head())` solve most bugs.

Good luck! If you know the theory already, this folder is about making the code feel just as natural.
