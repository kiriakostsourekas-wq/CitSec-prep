"""
Generates every CSV dataset used in this prep folder.

You do NOT need to run this - the CSVs are already inside each exercise's
data/ folder. It is kept here so you can see exactly how each dataset was
built (the "true" relationships are written below, which is useful when you
want to check whether your model recovered them).

Run (only if you deleted a CSV by accident):
    python tools/make_datasets.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
rng = np.random.default_rng(2026)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


# --------------------------------------------------------------------------
# 02 - stock prices (long format: one row per date per ticker)
# --------------------------------------------------------------------------
def make_stock_prices():
    dates = pd.bdate_range("2026-01-05", periods=60)
    market = rng.normal(0.0, 0.008, len(dates))
    specs = {  # ticker: (start price, daily drift, idiosyncratic vol, beta)
        "AAA": (100.0, 0.0008, 0.010, 1.0),
        "BBB": (50.0, 0.0002, 0.018, 1.3),
        "CCC": (200.0, -0.0006, 0.012, 0.6),
        "DDD": (20.0, 0.0015, 0.028, 1.8),
    }
    rows = []
    for ticker, (p0, mu, sig, beta) in specs.items():
        r = mu + beta * market + rng.normal(0.0, sig, len(dates))
        prices = p0 * np.cumprod(1.0 + r)
        volume = rng.integers(80_000, 400_000, len(dates))
        for d, p, v in zip(dates, prices, volume):
            rows.append({"date": d.strftime("%Y-%m-%d"), "ticker": ticker,
                         "close": round(float(p), 2), "volume": int(v)})
    df = pd.DataFrame(rows).sort_values(["date", "ticker"]).reset_index(drop=True)
    df.to_csv(ROOT / "02_numpy_pandas_basics/data/stock_prices.csv", index=False)


# --------------------------------------------------------------------------
# 03 - messy customer table (missing values, typos, duplicates, bad strings)
# --------------------------------------------------------------------------
def make_customers_raw():
    n = 200
    ids = np.arange(1001, 1001 + n)
    age = rng.integers(18, 70, n).astype(float)
    city = rng.choice(["London", "Paris", "Dubai"], n, p=[0.4, 0.3, 0.3])
    plan = rng.choice(["basic", "premium"], n, p=[0.65, 0.35])
    income = np.clip(rng.normal(55_000, 15_000, n), 15_000, None).round(-2)
    spend = np.where(plan == "premium", 60, 22) + rng.normal(0, 8, n)
    spend = np.clip(spend, 5, None).round(2)
    signup = pd.to_datetime("2022-01-01") + pd.to_timedelta(rng.integers(0, 1400, n), unit="D")

    # true churn rule: young, basic-plan, low-spend customers churn more
    z = -0.4 - 0.04 * (age - 40) + 0.9 * (plan == "basic") - 0.03 * (spend - 35)
    churned = rng.binomial(1, sigmoid(z))

    df = pd.DataFrame({
        "customer_id": ids,
        "age": age,
        "income": income,
        "city": city,
        "plan": plan,
        "monthly_spend": spend,
        "signup_date": signup.strftime("%Y-%m-%d"),
        "churned": churned,
    })

    # ---- make it messy ----
    df["income"] = df["income"].astype(object)
    for i in range(n):  # most incomes as strings with commas, some plain
        val = df.at[i, "income"]
        df.at[i, "income"] = f"{int(val):,}" if rng.random() < 0.7 else str(int(val))
    df.loc[rng.choice(n, 10, replace=False), "income"] = np.nan
    df.loc[rng.choice(n, 12, replace=False), "age"] = np.nan
    df.loc[rng.choice(n, 3, replace=False), "age"] = [999, -1, 999]   # data-entry typos
    messy_city = {"London": [" london", "LONDON", "London "], "Paris": ["paris", " Paris"],
                  "Dubai": ["dubai", "DUBAI "]}
    for i in rng.choice(n, 40, replace=False):
        df.at[i, "city"] = rng.choice(messy_city[df.at[i, "city"]])
    df.loc[rng.choice(n, 8, replace=False), "plan"] = np.nan

    dupes = df.sample(6, random_state=1)
    df = pd.concat([df, dupes]).sample(frac=1, random_state=2).reset_index(drop=True)
    df.to_csv(ROOT / "03_data_preprocessing/data/customers_raw.csv", index=False)


# --------------------------------------------------------------------------
# 04 - apartments (regression target: monthly rent)
# --------------------------------------------------------------------------
def make_apartments():
    n = 300
    hood = rng.choice(["Center", "Suburb", "Riverside"], n, p=[0.3, 0.45, 0.25])
    dist = np.where(hood == "Center", rng.uniform(0.5, 3, n),
                    np.where(hood == "Suburb", rng.uniform(5, 15, n), rng.uniform(2, 8, n)))
    sqm = np.clip(rng.normal(75, 25, n), 25, 180).round()
    bedrooms = np.clip(np.round(sqm / 30 + rng.normal(0, 0.6, n)), 1, 5).astype(int)
    age = rng.integers(0, 60, n)
    floor = rng.integers(0, 13, n)
    balcony = rng.binomial(1, 0.45, n)
    hood_effect = np.select([hood == "Center", hood == "Riverside"], [250, 150], 0)
    # TRUE MODEL (what a good regression should roughly recover):
    rent = (300 + 16 * sqm + 60 * bedrooms - 45 * dist - 5 * age + 12 * floor
            + 110 * balcony + hood_effect + rng.normal(0, 120, n))
    df = pd.DataFrame({
        "sqm": sqm.astype(int), "bedrooms": bedrooms, "dist_center_km": dist.round(2),
        "age_years": age, "floor": floor, "has_balcony": balcony,
        "neighborhood": hood, "rent": rent.round().astype(int),
    })
    df.to_csv(ROOT / "04_linear_regression/data/apartments.csv", index=False)


# --------------------------------------------------------------------------
# 05 - loan default (binary classification, ~20% positives)
# --------------------------------------------------------------------------
def make_loans():
    n = 400
    income = np.clip(rng.lognormal(np.log(55), 0.45, n), 15, 250).round(1)
    dti = rng.beta(2, 5, n).round(3)
    credit = np.clip(rng.normal(680, 60, n), 450, 850).round().astype(int)
    years = np.clip(rng.exponential(6, n), 0, 40).round(1)
    late = rng.poisson(0.8, n)
    # TRUE MODEL (log-odds of default):
    z = (-1.7 - 0.015 * (income - 60) + 3.5 * (dti - 0.3) - 0.012 * (credit - 680)
         - 0.05 * (years - 6) + 0.45 * late)
    default = rng.binomial(1, sigmoid(z))
    df = pd.DataFrame({
        "income_k": income, "debt_to_income": dti, "credit_score": credit,
        "years_employed": years, "late_payments": late, "default": default,
    })
    df.to_csv(ROOT / "05_logistic_regression/data/loan_default.csv", index=False)


# --------------------------------------------------------------------------
# 06 - fruits (3-class classification; weight is noisy and on a big scale)
# --------------------------------------------------------------------------
def make_fruits():
    specs = {  # name: (weight mean, width mean, height mean, color mean)
        "apple": (170, 7.5, 7.3, 0.80),
        "orange": (185, 8.0, 7.8, 0.55),
        "lemon": (155, 6.2, 8.2, 0.30),
    }
    frames = []
    for name, (w, wd, h, c) in specs.items():
        m = 60
        frames.append(pd.DataFrame({
            "weight_g": rng.normal(w, 40, m).round(),
            "width_cm": rng.normal(wd, 0.55, m).round(2),
            "height_cm": rng.normal(h, 0.55, m).round(2),
            "color_score": np.clip(rng.normal(c, 0.08, m), 0, 1).round(3),
            "fruit": name,
        }))
    df = pd.concat(frames).sample(frac=1, random_state=3).reset_index(drop=True)
    df.to_csv(ROOT / "06_knn_classification/data/fruits.csv", index=False)


# --------------------------------------------------------------------------
# 07 - customer churn (rule-based target -> trees shine)
# --------------------------------------------------------------------------
def make_churn():
    n = 320
    tenure = rng.integers(1, 73, n)
    contract = rng.choice(["month-to-month", "one-year", "two-year"], n, p=[0.55, 0.27, 0.18])
    charges = rng.uniform(20, 120, n).round(2)
    calls = rng.poisson(1.6, n)
    # TRUE RULE (an if/else tree!) + 7% label noise
    churn = ((contract == "month-to-month") & (tenure < 24)) | ((calls >= 3) & (charges > 70))
    flip = rng.random(n) < 0.07
    churn = np.where(flip, ~churn, churn).astype(int)
    df = pd.DataFrame({
        "tenure_months": tenure, "contract": contract, "monthly_charges": charges,
        "support_calls": calls, "churn": churn,
    })
    df.to_csv(ROOT / "07_decision_tree/data/churn.csv", index=False)


# --------------------------------------------------------------------------
# 10 - daily bike rentals (mock interview: messy + non-linear + time trend)
# --------------------------------------------------------------------------
def make_bikes():
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    n = len(dates)
    doy = dates.dayofyear.values
    temp = 15 + 11 * np.sin(2 * np.pi * (doy - 110) / 365) + rng.normal(0, 3, n)
    humidity = rng.uniform(30, 95, n)
    wind = rng.gamma(2.0, 6.0, n)
    weekend = (dates.dayofweek >= 5).astype(int)
    p_rain = sigmoid((humidity - 75) / 6)
    weather = np.where(rng.random(n) < p_rain, "rain",
                       np.where(rng.random(n) < 0.45, "cloudy", "clear"))
    # TRUE MODEL: inverted-U in temperature (peak ~ 24C), upward trend over the year
    rentals = (900 + 3200 * np.exp(-((temp - 24) / 9) ** 2) + 2.5 * np.arange(n)
               + 450 * weekend - 900 * (weather == "rain") - 200 * (weather == "cloudy")
               - 8 * (humidity - 60) - 15 * wind + rng.normal(0, 250, n))
    df = pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"), "temp_c": temp.round(1),
        "humidity": humidity.round(), "windspeed_kmh": wind.round(1),
        "is_weekend": weekend, "weather": weather,
        "rentals": np.clip(rentals, 50, None).round().astype(int),
    })
    df.loc[rng.choice(n, 9, replace=False), "temp_c"] = np.nan
    df.loc[rng.choice(n, 6, replace=False), "humidity"] = np.nan
    df.to_csv(ROOT / "10_mock_interview/data/bike_rentals.csv", index=False)


if __name__ == "__main__":
    make_stock_prices()
    make_customers_raw()
    make_apartments()
    make_loans()
    make_fruits()
    make_churn()
    make_bikes()
    print("All datasets written.")
