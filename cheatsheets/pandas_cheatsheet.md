# pandas cheatsheet (offline, pandas 3.x)

`import pandas as pd` · docs offline: `help(pd.DataFrame.groupby)`, or `python -m pydoc -b`

## Mental model
A **DataFrame** is a table: named columns, each column is a **Series** (1-D array + index labels).
`df["col"]` → Series · `df[["a", "b"]]` → DataFrame · each row has an index label (default 0..n−1).

## Load & look
```python
df = pd.read_csv("file.csv", parse_dates=["date"])
df.head(10), df.tail(), df.shape, df.columns, df.dtypes, df.info()
df.describe()                         # count/mean/std/min/quartiles/max
df["city"].value_counts()             # frequency of each value
df["city"].unique(), df["city"].nunique()
df.isna().sum()                       # missing values per column
df.duplicated().sum()
df.to_csv("out.csv", index=False)
```

## Select
```python
df["close"]                           # one column
df[["date", "close"]]                 # several columns
df.loc[row_labels, col_labels]        # by LABEL (df.loc[df.close > 100, "ticker"])
df.iloc[0:5, 0:2]                     # by POSITION
df[df["ticker"] == "AAA"]             # filter rows
df[(df.ticker == "AAA") & (df.volume > 1e5)]   # & | ~ with BRACKETS
df[df["city"].isin(["London", "Paris"])]
df.query("volume > 100000 and ticker == 'AAA'")
```

## Modify (always assign the result!)
```python
out = df.copy()                                     # don't modify the caller's df
out["notional"] = out["close"] * out["volume"]      # new column
out.loc[out["age"] > 100, "age"] = np.nan           # conditional assignment (NOT out["age"][mask] = ...)
out = out.drop(columns=["id"])
out = out.rename(columns={"close": "px"})
out["contract_m"] = out["contract"].map({"monthly": 1, "yearly": 12})
out["x"] = out["x"].astype(float)
out = out.sort_values(["ticker", "date"], ascending=[True, False])
out = out.reset_index(drop=True)
out = out.drop_duplicates()
```

## Missing values
```python
df.dropna(), df.dropna(subset=["age"])
df["age"].fillna(df["age"].median())
df["plan"].fillna("unknown")
df["temp"].interpolate()          # time series: from neighbours
df["temp"].ffill()                # carry the last known value forward
```

## Strings & dates
```python
s.str.strip(), s.str.lower(), s.str.title(), s.str.replace(",", "", regex=False)
s.str.contains("abc"), s.str.split("-").str[0]
pd.to_numeric(s, errors="coerce")       # unparseable -> NaN
d = pd.to_datetime(df["date"])
d.dt.year, d.dt.month, d.dt.dayofweek, d.dt.dayofyear
(d2 - d1).dt.days                       # timedelta -> integer days
pd.Timestamp("2026-01-01")
```

## Group by (split → apply → combine)
```python
df.groupby("ticker")["close"].mean()                       # Series indexed by ticker
df.groupby("ticker").agg(avg=("close", "mean"), n=("close", "size"))
df.groupby(["ticker", "month"])["volume"].sum()
df.groupby("ticker")["close"].pct_change()                 # per-group, keeps the original rows
df.groupby("ticker")["return"].idxmax()                    # row label of the max per group
df.groupby("default").mean()                               # compare classes
```

## Reshape & combine
```python
wide = df.pivot(index="date", columns="ticker", values="close")   # long -> wide
long = wide.reset_index().melt(id_vars="date", var_name="ticker", value_name="close")
pd.get_dummies(df, columns=["city"], drop_first=True, dtype=int)   # one-hot
pd.concat([df1, df2])                      # stack rows
df1.merge(df2, on="customer_id", how="left")   # SQL-style join
```

## Time series
```python
s.pct_change()            # simple returns
np.log(s).diff()          # log returns
s.shift(1)                # previous value (avoid look-ahead!)
s.rolling(20).mean(), s.rolling(20).std()
s.expanding().mean()
s.cummax(), s.cumsum(), (1 + r).cumprod()
wide.corr()
```

## To numpy (for your models)
```python
X = df[FEATURES].to_numpy(dtype=float)
y = df["target"].to_numpy()
```

## pandas 3 notes (you're on pandas 3.0)
- **Copy-on-write:** chained assignment `df["a"][mask] = 1` does nothing. Use `df.loc[mask, "a"] = 1`.
- Text columns have dtype `str` (it used to be `object`).
- `inplace=True` is discouraged: write `df = df.dropna()` instead.
