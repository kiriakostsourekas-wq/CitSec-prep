# scikit-learn cheatsheet (offline)

Every model has the same API: `model.fit(X_train, y_train)` → `model.predict(X)` → `model.score(X, y)`.
Docs offline: `help(LogisticRegression)` shows every parameter.

## Splitting & CV
```python
from sklearn.model_selection import train_test_split, cross_val_score, KFold, TimeSeriesSplit
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
scores = cross_val_score(model, X, y, cv=5, scoring="roc_auc")     # 5-fold CV
cv = TimeSeriesSplit(n_splits=5)                                   # walk-forward for time series
```

## Preprocessing (fit on TRAIN only)
```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
scaler = StandardScaler().fit(X_tr)
X_tr_s, X_te_s = scaler.transform(X_tr), scaler.transform(X_te)
SimpleImputer(strategy="median")
OneHotEncoder(handle_unknown="ignore")          # unseen test categories -> all zeros
```

## Pipelines (the leak-proof way)
```python
from sklearn.pipeline import make_pipeline
model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit(X_tr, y_tr)                  # scaler fitted on train only, also inside CV
```
Mixed column types:
```python
from sklearn.compose import ColumnTransformer
pre = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])
model = make_pipeline(pre, LogisticRegression())
```

## Models in this folder
```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
LinearRegression().fit(X, y)            # .coef_, .intercept_
Ridge(alpha=1.0), Lasso(alpha=0.1)      # alpha = λ
LogisticRegression(C=1.0, max_iter=1000)   # C = 1/λ (SMALLER C = MORE regularization), .predict_proba(X)[:, 1]
LogisticRegression(class_weight="balanced")

from sklearn.neighbors import KNeighborsClassifier
KNeighborsClassifier(n_neighbors=5)

from sklearn.naive_bayes import GaussianNB

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text
tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=0)
print(export_text(tree.fit(X, y), feature_names=FEATURES)); tree.feature_importances_

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
```

## Metrics
```python
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, classification_report, roc_auc_score, log_loss)
r2_score(y, y_hat); mean_squared_error(y, y_hat) ** 0.5     # RMSE
confusion_matrix(y, y_hat)            # rows = true, cols = predicted
print(classification_report(y, y_hat))
roc_auc_score(y, p)                   # p = predicted PROBABILITIES, not labels
```

## Hyper-parameter search
```python
from sklearn.model_selection import GridSearchCV
search = GridSearchCV(make_pipeline(StandardScaler(), KNeighborsClassifier()),
                      {"kneighborsclassifier__n_neighbors": [1, 3, 5, 9, 15]}, cv=5)
search.fit(X_tr, y_tr); search.best_params_, search.best_score_
```
