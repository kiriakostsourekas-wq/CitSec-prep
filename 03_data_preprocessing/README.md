# 03 · Data pre-processing (≈ 1.5 hours)

**Goal:** turn a messy table into a clean numeric matrix `X` and a target vector `y`, **without data leakage**.
This is the step interviewers use to tell people who have only read about ML apart from people who have actually done it.

**Dataset:** `data/customers_raw.csv`, 206 rows of a subscription business. Target: `churned` (1 = customer left).

| customer_id | age | income | city | plan | monthly_spend | signup_date | churned |
|---|---|---|---|---|---|---|---|
| 1026 | 29.0 | "53,700" | Dubai | premium | 66.66 | 2022-07-27 | 0 |
| 1085 | 66.0 | 51700 | LONDON | premium | 59.22 | 2023-10-29 | 0 |

**Before coding**, run `python exercise.py` and look at the output of `describe()` and `value_counts()`.
Write down every problem you see. (Answer key: duplicates, text incomes, messy cities, ages 999 and −1, NaNs, date as text.)

## Concept notes

**The golden order**
```
raw → remove duplicates → fix types / typos → feature engineering (dates → numbers)
    → encode categories → SPLIT train/test → learn medians/means/stds on TRAIN → apply to train & test → model
```

**Data leakage** = information from the test set (or from the future) sneaks into training.
If you compute the mean/std for scaling on the *whole* dataset, the test set has influenced your preprocessing,
and your test score becomes optimistic. Rule: **anything learned from data (`fit`) uses train only.**
Stateless transforms (lower-casing strings, one-hot with a fixed category list) are safe before the split.

**Missing values: options**
| Strategy | When |
|---|---|
| drop rows | very few missing, missing at random |
| median imputation | numeric, robust to outliers (mean is not; see what age=999 does to the mean!) |
| "unknown" category | categorical; missingness may itself carry signal |
| add an `is_missing` flag column | when missingness may be informative |

**Categorical encoding**
- One-hot: `city ∈ {Dubai, London, Paris}` → columns `city_London`, `city_Paris` (Dubai = all zeros).
- `drop_first=True` because with an intercept, all k dummies would be perfectly collinear (they sum to 1), which is the **dummy variable trap**.
  Trees don't care; linear models do.
- Never encode categories as 1, 2, 3 for a linear model: that invents an order and equal spacing.

**Scaling (standardization):** z = (x − μ_train) / σ_train.
Needed for: gradient descent (faster convergence), kNN (distances), regularization (L1/L2 penalize all coefficients equally).
Not needed for: tree models (splits are invariant to monotone transforms).

## Tasks
| ID | Function | Skill |
|---|---|---|
| A1–A3 | `load_raw`, `missing_report`, `drop_duplicate_rows` | first look |
| B1 | `clean_income` | `.str.replace`, `astype(float)` |
| B2 | `clean_city` | `.str.strip().str.title()` |
| B3 | `fix_age` | `.loc[mask, col] = np.nan` |
| B4 | `add_tenure_days` | `pd.to_datetime`, `.dt.days` |
| C1 | `one_hot` | `fillna`, `pd.get_dummies` |
| C2 | `train_test_split_df` | `rng.permutation`, `.iloc` |
| C3–C4 | `fit_preprocessor`, `apply_preprocessor` | fit on train, apply to both |
| D1 | `build_dataset` | whole pipeline |

When everything passes, run `python solution.py` to see a logistic regression trained on your clean data.

## Interviewer follow-ups

<details><summary>1. You have 40% missing values in one column. What do you do?</summary>

First ask *why* it's missing (MCAR / MAR / MNAR). If the missingness is informative (e.g. income missing because people with
low income refuse to answer), add an `is_missing` indicator and impute. If the column is weak and mostly empty,
consider dropping it. Always compare options with validation performance, not intuition.
</details>

<details><summary>2. Why median instead of mean for imputation?</summary>

The median is robust to outliers. In this dataset, before fixing the 999 typos the mean age is ≈ 54 and std ≈ 98;
the median is 43. Financial data (incomes, volumes, returns) is heavy-tailed, so the median is usually safer.
</details>

<details><summary>3. Give an example of leakage in finance.</summary>

(a) Normalizing features with the full-sample mean/std, which uses future data. (b) Using a random train/test split on time series:
the model is trained on tomorrow to predict yesterday. Use a time-based split / walk-forward validation.
(c) Survivorship bias: training only on stocks that exist *today* (e.g. current S&P 500 members), which silently removes
companies that went bankrupt. (d) Features that are only known after the event (e.g. "number of collections calls" to predict default).
</details>

<details><summary>4. A category in the test set never appeared in train. What happens?</summary>

With one-hot built separately on test you'd get mismatched columns, and the model breaks or silently misaligns.
Fix: fix the category list on train (sklearn `OneHotEncoder(handle_unknown="ignore")`), map unseen categories to all-zeros or an "other" bucket.
</details>

<details><summary>5. Is `customer_id` a useful feature?</summary>

No. It's an arbitrary label. A flexible model (tree) could still "use" it if IDs were assigned in time order, which
would be a leakage-like proxy for signup date. Remove IDs; if time matters, engineer an explicit time feature.
</details>
